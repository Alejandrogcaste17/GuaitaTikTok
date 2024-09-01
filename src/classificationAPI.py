import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, classificationCollection

api_url = "http://boso.dsic.upv.es:5008/tweet_classification"

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

def process_classification_api(taskCollection, current_user):

    print("llegamos a clasificador")
    # Headers para indicar que se está enviando un payload JSON
    headers = {
        'Content-Type': 'application/json'
    }

    task_videos = videosCollection.find_one({'taskId': taskCollection['_id']})

    if task_videos:
        print("Encontrado")

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
    
    print("llegamos aqui x2")
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
        print(json.dumps(response_data, indent=4))

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
        print(num_videos)

        for i in range(num_videos):
            print(video_data[i]['id'])
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

    else:
        print('Error al realizar la solicitud:', response.status_code)
        print(response.text)
    
    return True