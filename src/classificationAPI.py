import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, classificationCollection
from statisticsAPI import process_statistics_api, process_statistics_profile_api

api_url = "http://boso.dsic.upv.es:5008/tweet_classification"
api_profile_url = "http://boso.dsic.upv.es:5008/user_profiling"

# Distintos clasificadores que vamos a emplear
tasks = [ "tass19_es_sentiment",
      "irosva19_es_irony",
      "emoevales21_emotion",
      "hateeval19_hate",
      "hateeval19_aggressiveness",
      "detoxis21_aggressiveness",
      "emoevales21_offensive",
      "haha19_humor",
      "detoxis21_argumentation",
      "detoxis21_constructiveness",
      "detoxis21_improper-language",
      "detoxis21_insult",
      "detoxis21_intolerance",
      "detoxis21_mockery",
      "detoxis21_sarcasm",
      "detoxis21_stereotype",
      "detoxis21_toxicity-level"]

tasksProfile = [
      "pan19_bot",
      "pan18_gender",
      "pan15_age",
      "pan15_personality"]

def procces_classification_profile_api(taskCollection, current_user):

    # Headers para indicar que se está enviando un payload JSON
    headers = {
        'Content-Type': 'application/json'
    }

    task_videos = videosCollection.find_one({'taskId': taskCollection['_id']})

    # Array para almacenar los valores id y voice_to_text de cada video en list_videos
    video_data = []

    # Verificamos que task_videos y list_videos existan
    if task_videos and 'list_videos_with_voice' in task_videos:
        # Iteramos sobre cada video dentro de list_videos
        for video in task_videos['list_videos_with_voice']:
            # Extraemos el id y el voice_to_text, si existen
            video_id = video.get('id')
            voice_to_text = video.get('voice_to_text')
            
            # Añadimos el par (id, voice_to_text) al array
            video_data.append({'id': video_id, 'voice_to_text': voice_to_text})
    
    # Extraemos todos los valores de 'voice_to_text' de 'video_data'
    texts = [video['voice_to_text'] for video in video_data]

    # Payload de la petición con los textos extraídos
    payload = {
        "samples": {
            "text": texts  # Aquí van todos los voice_to_text recogidos
        },
        "tasks": tasksProfile
    }

    # Payload de la petición con los textos extraídos
    payload2 = {
        "samples": {
            "text": texts  # Aquí van todos los voice_to_text recogidos
        },
        "tasks": tasks
    }

    # Realizamos la peticion POST para que clasifique todos los videos obtenidos en funcion del usuario
    response = requests.post(api_profile_url, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

         # Realizamos la peticion POST para que clasifique todos los videos obtenidos en funcion de distintas emociones
        response2 = requests.post(api_url, json=payload2, headers=headers)

        if response.status_code == 200:
            response_data2 = response2.json()

            #Extraemos todos los datos obtenidos de cada video

            age = response_data['Age']['pan15_age']

            gender = response_data['Gender']['pan18_gender']

            bot = response_data['Bot']['pan19_bot']

            personality = response_data['Personality']['pan15_personality']

            sentiment = response_data2['Sentiment']['tass19_es_sentiment']
            
            toxicity = response_data2['Toxicity']['detoxis21_toxicity-level']

            stereotype = response_data2['Stereotype']['detoxis21_stereotype']

            sarcasm = response_data2['Sarcasm']['detoxis21_sarcasm']

            offensiveness = response_data2['Offensiveness']['emoevales21_offensive']

            aggressiveness = response_data2['Aggressiveness']['hateeval19_aggressiveness']

            mockery = response_data2['Mockery']['detoxis21_mockery']

            intolerance = response_data2['Intolerance']['detoxis21_intolerance']

            argumentation = response_data2['Argumentation']['detoxis21_argumentation']

            constructiveness = response_data2['Constructiveness']['detoxis21_constructiveness']

            emotion = response_data2['Emotion']['emoevales21_emotion']

            hate = response_data2['Hate speech']['hateeval19_hate']

            humor = response_data2['Humor']['haha19_humor']

            improper_language = response_data2['Improper language']['detoxis21_improper-language']

            insult = response_data2['Insult']['detoxis21_insult']

            irony = response_data2['Irony']['irosva19_es_irony']

            num_videos = len(sentiment)

            for i in range(num_videos):
                classification_document = {
                    'videoId': video_data[i]['id'],
                    'taskId': taskCollection['_id'],
                    'voice_to_text': video_data[i]['voice_to_text'],
                    'age': age[i],
                    'bot': bot[i],
                    'gender': gender[i],
                    'personality': personality[i],
                    'sentiment': sentiment[i],
                    'toxicity': toxicity[i],
                    'sarcasm': sarcasm[i],
                    'offensiveness': offensiveness[i],
                    'aggressiveness': aggressiveness[i],
                    'mockery': mockery[i],
                    'intolerance': intolerance[i],
                    'argumentation': argumentation[i],
                    'constructiveness': constructiveness[i],
                    'emotion': emotion[i],
                    'hate': hate[i],
                    'humor': humor[i],
                    'improper_language': improper_language[i],
                    'insult': insult[i],
                    'irony': irony[i],
                    'stereotype': stereotype[i],
                }

                # Insertar el documento en la colección de classification
                result = classificationCollection.insert_one(classification_document)

            # Ahora generaremos las estadisticas que se visualizaran en la pagina

            process_statistics_profile_api(taskCollection, current_user)
        else:
            print('Error al realizar la solicitud:', response.status_code)
            print(response.text)
    else:
        print('Error al realizar la solicitud:', response.status_code)
        print(response.text)

def process_classification_api(taskCollection, current_user):

    # Headers para indicar que se está enviando un payload JSON
    headers = {
        'Content-Type': 'application/json'
    }

    task_videos = videosCollection.find_one({'taskId': taskCollection['_id']})

    # Array para almacenar los valores id y voice_to_text de cada video en list_videos
    video_data = []

    # Verificamos que task_videos y list_videos existan
    if task_videos and 'list_videos' in task_videos:
        # Iteramos sobre cada video dentro de list_videos
        for video in task_videos['list_videos']:
            # Extraemos el id y el voice_to_text, si existen
            video_id = video.get('id')
            voice_to_text = video.get('voice_to_text')
            
            # Añadimos el par (id, voice_to_text) al array
            video_data.append({'id': video_id, 'voice_to_text': voice_to_text})
    
    # Extraemos todos los valores de 'voice_to_text' de 'video_data'
    texts = [video['voice_to_text'] for video in video_data]

    # Payload de la petición con los textos extraídos
    payload = {
        "samples": {
            "text": texts  # Aquí van todos los voice_to_text recogidos
        },
        "tasks": tasks
    }

    # Realizamos la peticion POST para que clasifique todos los videos obtenidos en funcion de distintas emociones
    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        #Extraemos todos los datos obtenidos de cada video
        sentiment = response_data['Sentiment']['tass19_es_sentiment']
        
        toxicity = response_data['Toxicity']['detoxis21_toxicity-level']

        stereotype = response_data['Stereotype']['detoxis21_stereotype']

        sarcasm = response_data['Sarcasm']['detoxis21_sarcasm']

        offensiveness = response_data['Offensiveness']['emoevales21_offensive']

        aggressiveness = response_data['Aggressiveness']['hateeval19_aggressiveness']

        mockery = response_data['Mockery']['detoxis21_mockery']

        intolerance = response_data['Intolerance']['detoxis21_intolerance']

        argumentation = response_data['Argumentation']['detoxis21_argumentation']

        constructiveness = response_data['Constructiveness']['detoxis21_constructiveness']

        emotion = response_data['Emotion']['emoevales21_emotion']

        hate = response_data['Hate speech']['hateeval19_hate']

        humor = response_data['Humor']['haha19_humor']

        improper_language = response_data['Improper language']['detoxis21_improper-language']

        insult = response_data['Insult']['detoxis21_insult']

        irony = response_data['Irony']['irosva19_es_irony']

        num_videos = len(sentiment)

        for i in range(num_videos):
            classification_document = {
                'videoId': video_data[i]['id'],
                'voice_to_text': video_data[i]['voice_to_text'],
                'sentiment': sentiment[i],
                'toxicity': toxicity[i],
                'sarcasm': sarcasm[i],
                'offensiveness': offensiveness[i],
                'aggressiveness': aggressiveness[i],
                'mockery': mockery[i],
                'intolerance': intolerance[i],
                'argumentation': argumentation[i],
                'constructiveness': constructiveness[i],
                'emotion': emotion[i],
                'hate': hate[i],
                'humor': humor[i],
                'improper_language': improper_language[i],
                'insult': insult[i],
                'irony': irony[i],
                'stereotype': stereotype[i],
            }

            # Insertar el documento en la colección de classification
            result = classificationCollection.insert_one(classification_document)

        # Ahora generaremos las estadisticas que se visualizaran en la pagina
        print("nos vamos a analizar")
        process_statistics_api(taskCollection, current_user)
    else:
        print('Error al realizar la solicitud:', response.status_code)
        print(response.text)
