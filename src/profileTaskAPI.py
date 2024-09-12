import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, profilesCollection
from classificationAPI import procces_classification_profile_api
from pymongo.errors import PyMongoError

# Define las credenciales de la aplicación
client_key = 'awoy8doraswxa914'
client_secret = 'C1Fq10WTwgYygDlteNj8KDWLZTK5EaRe'

access_token = ''

def sortVideos(results):
    # Ordena primero por 'create_time' y luego por 'id' convertido a entero para que la comparación sea numérica
    sorted_results = sorted(results, key=lambda video: (video['create_time'], int(video['id'])))
    return sorted_results

def dateFormat(results):   
    for video in results:
        if 'create_time' in video and isinstance(video['create_time'], int):
            fecha = datetime.utcfromtimestamp(video['create_time'])
            video['create_time'] = fecha.strftime('%Y%m%d')
        else:
            print(f"El video {video.get('id', 'sin ID')} no tiene 'create_time' válido.")
    return results

def videosWithVoiceToText(response, results, taskCollection):
    for video in response["data"]["videos"]:
        if "voice_to_text" in video:
            results.append(video)
    print("Cantidad de videos: ", len(results))
    try:
        # Intentar insertar el documento en la colección
        tasksCollection.update_one(
            {'_id': taskCollection['_id']},
            {'$set': {'recoveredVideos': len(results)}}
        )

    except PyMongoError as e:
        # Si ocurre un error, imprimir el mensaje de error
        print(f"Error al actualizar el documento: {e}")

def videosWithoutVoiceToText(response, results2):
    for video in response["data"]["videos"]:
        if not "voice_to_text" in video:
            results2.append(video)

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

def getFormatDate(date):
    # Eliminar los guiones "-" de la fecha original
    return date.replace("-", "")

def getTimeList(startDate, endDate):
    # Convertir las fechas del formato "YYYYMMDD" a objetos datetime.date
    fecha_inicio = datetime.strptime(startDate, "%Y%m%d").date()
    fecha_final = datetime.strptime(endDate, "%Y%m%d").date()
    
    # Lista para almacenar los intervalos
    time_list = []
    
    # Inicializar la fecha actual al inicio
    fecha_actual = fecha_inicio
    
    # Iterar desde la fecha de inicio hasta la fecha final
    while fecha_actual <= fecha_final:
        # Calcular la fecha de final del intervalo actual
        fecha_intervalo_final = fecha_actual + timedelta(days=29)
        if fecha_intervalo_final > fecha_final:
            fecha_intervalo_final = fecha_final
        
        # Agregar el intervalo a la lista en formato string
        time_list.append((fecha_actual.strftime("%Y%m%d"), fecha_intervalo_final.strftime("%Y%m%d")))
        
        # Actualizar la fecha actual para el próximo intervalo
        fecha_actual = fecha_intervalo_final + timedelta(days=1)
    
    return time_list

def add_user_profile(username, headers, taskCollection, current_user):
    # Definimos las dos url que utilizaremos
    url = 'https://open.tiktokapis.com/v2/research/user/info/?fields=display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count'
    
    # Primera request para sacar la informacion del perfil
    dataProfile = {
        "username": username
    }

    # Realizamos la solicitud POST para recuperar la informacion del perfil
    profile_response = requests.post(url, json=dataProfile, headers=headers)

    if profile_response.status_code == 200:
        response_data = profile_response.json()
        
        # Creamos nuestro documento a insertar en la base de datos
        profile_document = {
            'username': username,
            'taskId': taskCollection['_id'],
            'userId': current_user,
            'data': response_data['data']
        }

        # Insertar el documento en la colección de videos
        result = profilesCollection.insert_one(profile_document)

        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Profile Founded', 'state_message': 'Searching videos of the user'}}
            )
            return True
        else:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'Error adding de user profile to the database'}}
            )
            return False
    else:
        print('Error al realizar la solicitud:', profile_response.status_code)
        print(profile_response.text)
        # Convertir el texto de la respuesta a un objeto JSON
        profile_response_json = json.loads(profile_response.text)
        if 'is private' in profile_response_json["error"]["message"]:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Private', 'state_message': 'Error the username of this profile is a private account, please try again in a public account'}}
            )
            return False
        elif 'cannot find the user' in profile_response_json["error"]["message"]:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'Error searching for the user profile on TikTok, make sure you have typed the "username" correctly'}}
            )
            return False
        else:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'Error when making the first request, please try again later, or try the task again'}}
            )
            return False


async def process_profile_task(taskCollection, current_user):
    
    access_token = getAccessToken(taskCollection)

    # Define los encabezados de la solicitud
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    username = taskCollection['userProfile']

    profileCheck = add_user_profile(username, headers, taskCollection, current_user)

    if profileCheck:
        # Definimos las dos url que utilizaremos
        url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,video_description,create_time,voice_to_text,hashtag_names,username,music_id'

        startDate = getFormatDate(taskCollection['startDate'])
        endDate = getFormatDate(taskCollection['endDate'])
        time_list = getTimeList(startDate, endDate)

        results = []
        results2 = []

        for start_date, end_date in time_list:
            data = {
                "query": {
                    "and": [
                        { "operation": "EQ", "field_name": "username", "field_values": [username] }
                    ]
                },
                "max_count": 100,
                "start_date": start_date,
                "end_date": end_date
                
            }
            print(start_date)
            print(end_date)
            time.sleep(5)
            goodRequest = False
            count = 0

            while goodRequest == False:

                # Realiza la solicitud POST
                first_response = requests.post(url, json=data, headers=headers)

                if first_response.status_code == 200:
                    goodRequest = True
                count += 1
                if count == 40:
                    break
                print(count)

            # Procesa la respuesta
            if first_response.status_code == 200:

                response_data = first_response.json()

                videosWithVoiceToText(response_data, results, taskCollection)
                videosWithoutVoiceToText(response_data, results2)
                
                # Condicion para el caso en el que encuentre menos de 100 videos en el rango de fechas establecido
                if response_data["data"]["cursor"] < 100 and response_data["data"]["has_more"] == False:
                    print("No se encontraron mas de 100 videos")
                else:
                    time.sleep(5)

                    # Variable para saber cuando la request ha fallado y realizar la peticion otra vez
                    request_again = False

                    # Variable para saber si es la primera iteracion del loop
                    first_iteration = True

                    # Cursor condicion
                    data["cursor"] = response_data["data"]["cursor"]
                    data["search_id"] = response_data["data"]["search_id"]

                    while data["cursor"] < 1000 and data["cursor"] % 100 == 0:
                        
                        print("Empezamos bucle")
                        
                        if request_again == False:
                            if not first_iteration:
                                data["cursor"] = loop_response_data["data"]["cursor"]
                                data["search_id"] = loop_response_data["data"]["search_id"]
                                # Comprobamos si se puede seguir realizando paginacion
                                if loop_response_data["data"]["has_more"] == False:
                                    print("No hay mas videos")
                                    print(loop_response_data["data"]["has_more"])
                                    break
                            else:
                                first_iteration = False

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
                            videosWithVoiceToText(loop_response_data, results, taskCollection)
                            videosWithoutVoiceToText(loop_response_data, results2)
                            print("Cantidad de videos: ", len(results))
                        else:
                            if loop_response.status_code == 500:
                                print("Mala peticion")
                                request_again = True
                                print("Cantidad de videos: ", len(results))
                                print(loop_response.text)

                            else:
                                loop_response_data2 = loop_response.json()
                                if loop_response_data2["error"]["message"] == "Invalid count or cursor":
                                    print("Mala peticion")
                                    request_again = True
                                    print("Cantidad de videos: ", len(results))
                                    print(loop_response.text)
                                else:
                                    print('Error al realizar la solicitud:', loop_response.status_code)
                                    print(loop_response.text)
                                    print("Cursor: ", data["cursor"])
                                    print("Search_id: ", data["search_id"])
                                    break

            else:
                print('Error al realizar la solicitud:', first_response.status_code)
                print(first_response.text)
                tasksCollection.update_one(
                    {'_id': taskCollection['_id']},
                    {'$set': {'state': 'Stopped', 'state_message': 'Error when making the first request, please try again later, or try the task again'}}
            )
     
        # Convertimos la variable create_time al formato "YYYYMMDD"
        results = dateFormat(results)

        # Ordenamos los videos por la fecha de subida
        results = sortVideos(results)

        # Convertimos los id de los videos a string
        for video in results:
            video['id'] = str(video['id'])  

        # Creamos nuestro documento a insertar en la base de datos
        video_document = {
            'taskId': taskCollection['_id'],
            'userId': current_user,
            'username': username,
            'total_videos_with_voice': len(results),
            'total_videos_without_voice': len(results2),
            'list_videos_with_voice': results,
            'list_videos_without_voice': results2,
            'cursor': response_data["data"].get('cursor', 0),
            'search_id': response_data["data"].get('search_id', 0)
        }
        # Insertar el documento en la colección de videos
        result = videosCollection.insert_one(video_document)

        print("Insertamos los videos en la base de datos")  

        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state_message': 'The classification is being carried out'}}
            )
            if len(results) == 0:
                tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'No videos were found for this assignment, videos are probably not in region code ES'}}
            )
            else:
                print("nos vamos a clasificar")
                procces_classification_profile_api(taskCollection, current_user)
                tasksCollection.update_one(
                    {'_id': taskCollection['_id']},
                    {'$set': {'state': 'Finished', 'state_message': 'The task has been completed successfully'}}
                )
        else:
            tasksCollection.update_one(
                {'_id': taskCollection['_id']},
                {'$set': {'state': 'Stopped', 'state_message': 'Error adding videos to the database'}}
            )

    