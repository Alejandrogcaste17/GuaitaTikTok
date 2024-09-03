import requests
import json
import time
import asyncio
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, classificationCollection, statisticsCollection

def process_statistics_api(taskCollection, current_user):

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

    sentiments = sentimentsStatistics(video_data)
    
    toxicity = toxicityStatistics(video_data)

    offensiveness = offensiveStatistics(video_data)

    intolerance =  intoleranceStatistics(video_data)

    hate =  hateStatistics(video_data)

    stereotypes = stereotypeStatistics(video_data)

    statistic_document = {
        'taskId': taskCollection['_id'],
        'sentiments': sentiments,
        'offensiveness': offensiveness,
        'hate': hate,
        'stereotypes': stereotypes,
        'intolerance': intolerance
    }

    # Insertar el documento en la colección de classification
    result = statisticsCollection.insert_one(statistic_document)

def offensiveStatistics(video_data):

    offensiveCount = 0
    notOffensiveCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sentiment' in classification:
            if classification['sentiment'].get('Offensive', None) == 1:
                offensiveCount += 1
            else:
                notOffensiveCount += 1

    result = {
        'offensive': offensiveCount,
        'notOffensive': notOffensiveCount
    }

    return result

def intoleranceStatistics(video_data):

    intoleranceCount = 0
    toleranceCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sentiment' in classification:
            if classification['sentiment'].get('Tolerant', None) == 1:
                toleranceCount += 1
            else:
                intoleranceCount += 1

    result = {
        'tolerance': toleranceCount,
        'intolerance': intoleranceCount
    }

    return result

def hateStatistics(video_data):

    notHateCount = 0
    hateCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sentiment' in classification:
            if classification['sentiment'].get('Hate', None) == 1:
                hateCount += 1
            else:
                notHateCount += 1

    result = {
        'hate': hateCount,
        'not hate': notHateCount
    }

    return result

def stereotypeStatistics(video_data):

    withStereotypeCount = 0
    withoutStereotypeCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sentiment' in classification:
            if classification['sentiment'].get('With stereotypes', None) == 1:
                withStereotypeCount += 1
            else:
                withoutStereotypeCount += 1

    result = {
        'withStereotypes': withStereotypeCount,
        'withoutStereotypes': withoutStereotypeCount
    }

    return result

def sentimentsStatistics(video_data):

    averagePositive = 0
    averageNegative = 0
    averageNone = 0
    averageNeutral = 0

    bestPositive = -float('inf')
    bestNegative = -float('inf')
    bestNone = -float('inf')
    bestNeutral = -float('inf')

    positiveId = None
    negativeId = None
    neutralId = None
    noneId = None

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sentiment' in classification:
            # Obtenemos valores negative
            negativeValue = classification['sentiment'].get('Negative', None)
            if bestNegative < negativeValue:
                bestNegative = negativeValue
                negativeId = video['id']
            averageNegative += negativeValue

            # Obtenemos valores positive
            PositiveValue = classification['sentiment'].get('Positive', None)
            if bestPositive < PositiveValue:
                bestPositive = PositiveValue
                positiveId = video['id']
            averagePositive += PositiveValue

            NeutralValue = classification['sentiment'].get('Neutral', None)
            if bestNeutral < NeutralValue:
                bestNeutral = NeutralValue
                neutralId = video['id']
            averageNeutral += NeutralValue

            # Obtenemos valores none
            NoneValue = classification['sentiment'].get('None', None)
            if bestNone < NoneValue:
                bestNone = NoneValue
                noneId = video['id']
            averageNone+= NoneValue

    # Calculamos los promedios
    averageNegative /= numVideos
    averagePositive /= numVideos
    averageNeutral /= numVideos
    averageNone /= numVideos

    result = {
        'averagePositive': averagePositive,
        'bestPositive': bestPositive,
        'positiveId': positiveId,
        'averageNegative': averageNegative,
        'bestNegative': bestNegative,
        'negativeId': negativeId,
        'averageNeutral': averageNeutral,
        'bestNeutral': bestNeutral,
        'neutralId': neutralId,
        'averageNone': averageNone,
        'bestNone': bestNone,
        'noneId': noneId
    }
    return result

def toxicityStatistics(video_data):
    return True