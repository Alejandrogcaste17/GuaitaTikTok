import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
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

async def process_profile_task(taskCollection, current_user):
    return True
