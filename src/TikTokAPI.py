import requests
import json
import time
from celeryConfiguration import celery
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection

# Define las credenciales de la aplicación
client_key = 'awoy8doraswxa914'
client_secret = 'C1Fq10WTwgYygDlteNj8KDWLZTK5EaRe'

access_token = ''

def videosWithVoiceToText(response):
    results = []
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
        raise Ignore()

def getRegionCode(taskCollection):
    if taskCollection['language'] == 'Spanish':
        return "ES"
    else: 
        return "EN"

def getFormatDate(date):
    # Eliminar los guiones "-" de la fecha original
    return date.replace("-", "")

@celery.task
def process_task(taskCollection, current_user):

    print("llego aqui x2")
    access_token = getAccessToken(taskCollection)

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

    # Define los encabezados de la solicitud
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    results = []

    # Realiza la solicitud POST
    response = requests.post(url, json=data, headers=headers)

    # Procesa la respuesta
    if response.status_code == 200:

        response_data = response.json()
        results += videosWithVoiceToText(response_data)

        time.sleep(8)
        while response_data["data"]["cursor"] < 1000:

            data["cursor"] = response_data["data"]["cursor"]
            data["search_id"] = response_data["data"]["search_id"]

            # Realiza la solicitud POST
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                results += videosWithVoiceToText(response_data)
            else:
                print('Error al realizar la solicitud:', response.status_code)
                print(response.text)
                break
        
        # Creamos nuestro documento a insertar en la base de datos
        video_document = {
            'taskId': taskCollection['_id'],
            'userId': current_user,
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
        print('Error al realizar la solicitud:', response.status_code)
        print(response.text)
        tasksCollection.update_one(
            {'_id': taskCollection['_id']},
            {'$set': {'state': 'Stopped', 'state_message': 'Error when making the first request, please try again later, or try the task again'}}
        )
        raise Ignore()

