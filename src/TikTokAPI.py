import requests
import json
import time
import asyncio
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection

# Define las credenciales de la aplicación
client_key = 'awoy8doraswxa914'
client_secret = 'C1Fq10WTwgYygDlteNj8KDWLZTK5EaRe'

access_token = ''

def videosWithVoiceToText(response, results):
    for video in response["data"]["videos"]:
        if "voice_to_text" in video:
            results.append(video)

def getAccessToken(taskCollection):

    # Define la URL de autorización y obtén el token de acceso
    auth_url = 'https://open.tiktokapis.com/v2/oauth/token/'
    auth_data = {
        'client_key': client_key,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }
    auth_response = requests.post(auth_url, headers=headers, data=auth_data)

    # Procesa la respuesta de autorización
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        return auth_data['access_token']
    else:
        print('Error al obtener el token de acceso:', auth_response.status_code)
        tasksCollection.update_one(
            {'_id': taskCollection['_id']},
            {'$set': {'state': 'Stopped', 'state_message': 'Something wrong happened when obtaining access token'}}
        )

def getRegionCode(taskCollection):
    if taskCollection['language'] == "spanish":
        return "ES"
    else: 
        return "EN"

def getFormatDate(date):
    # Eliminar los guiones "-" de la fecha original
    return date.replace("-", "")

async def process_task(taskCollection, current_user):

    access_token = getAccessToken(taskCollection)
    print(access_token)

    # Define la URL de la solicitud
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,video_description,create_time,voice_to_text'

    tags_list = taskCollection['tags_list']
    regionCode = getRegionCode(taskCollection)
    startDate = getFormatDate(taskCollection['startDate'])
    endDate = getFormatDate(taskCollection['endDate'])

    data = {
        "query": {
            "and": [
                { "operation": "IN", "field_name": "region_code", "field_values": [regionCode] },
                { "operation": "EQ", "field_name": "hashtag_name", "field_values": tags_list }
            ]
        },
        "max_count": 100,
        "start_date": startDate,
        "end_date": endDate
        
    }
    print(data)

    # Define los encabezados de la solicitud
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    results = []

    # Realiza la solicitud POST
    first_response = requests.post(url, json=data, headers=headers)

    # Procesa la respuesta
    if first_response.status_code == 200:

        response_data = first_response.json()
        videosWithVoiceToText(response_data, results)

        time.sleep(5)

        # Variable para saber cuando la request ha fallado y realizar la peticion otra vez
        request_again = False

        # Variable para saber si es la primera iteracion del loop
        first_iteration = True

        while response_data["data"]["cursor"] < 1000:

            print("Empezamos bucle")
            
            if request_again == False:
                if first_iteration:
                    data["cursor"] = response_data["data"]["cursor"]
                    data["search_id"] = response_data["data"]["search_id"]
                    first_iteration = False
                else:
                    data["cursor"] = loop_response_data["data"]["cursor"]
                    data["search_id"] = loop_response_data["data"]["search_id"]

                # Realiza la solicitud POST
                print("realizamos peticion")
                print("Cursor: ", data["cursor"])
                print("Search_id: ", data["search_id"])
                time.sleep(5)
                loop_response = requests.post(url, json=data, headers=headers)
            else:
                # Realiza la solicitud POST
                print("realizamos peticion 2.0")
                print("Cursor: ", data["cursor"])
                print("Search_id: ", data["search_id"])
                time.sleep(5)
                loop_response = requests.post(url, json=data, headers=headers)
                request_again = False

            if loop_response.status_code == 200:
                print("Buena peticion")
                loop_response_data = loop_response.json()
                results.append(videosWithVoiceToText(loop_response_data, results))
                print("Cantidad de videos: ", len(results))
            else:
                if loop_response.status_code == 500:
                    print("Mala peticion")
                    request_again = True
                    print("Cantidad de videos: ", len(results))
                    print(loop_response.text)

                else:
                    print('Error al realizar la solicitud:', loop_response.status_code)
                    print(loop_response.text)
                    break

        # Creamos nuestro documento a insertar en la base de datos
        video_document = {
            'taskId': taskCollection['_id'],
            'userId': current_user,
            'tags': tags_list,
            'total_videos': len(results),
            'list_videos': results,
            'cursor': response_data["data"]["cursor"],
            'search_id': response_data["data"]["search_id"]
        }

        # Insertar el documento en la colección de videos
        result = videosCollection.insert_one(video_document)

        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Finished', 'state_message': 'The task has been completed successfully'}}
            )
        else:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'Error adding videos to the database'}}
            )
    else:
        print('Error al realizar la solicitud:', first_response.status_code)
        print(first_response.text)
        tasksCollection.update_one(
            {'_id': taskCollection['_id']},
            {'$set': {'state': 'Stopped', 'state_message': 'Error when making the first request, please try again later, or try the task again'}}
        )

