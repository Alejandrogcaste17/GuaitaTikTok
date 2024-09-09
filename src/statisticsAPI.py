import requests
import json
import time
import asyncio
import sys
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, classificationCollection, statisticsCollection
from pymongo.errors import PyMongoError

def process_statistics_profile_api(taskCollection, current_user):

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

    statistic_document = {
        'taskId': taskCollection['_id'],
        'gender': genderStatistics(video_data),
        'age': ageStatistics(video_data),
        'bot': botStatistics(video_data),
        'personality': personalityStatistics(video_data),
        'sentiments': sentimentsStatistics(video_data, taskCollection),
        'offensiveness': offensiveStatistics(video_data),
        'hate': hateStatistics(video_data),
        'stereotypes': stereotypeStatistics(video_data),
        'intolerance': intoleranceStatistics(video_data),
        'insult': insultStatistics(video_data),
        'irony': ironyStatistics(video_data),
        'humor': humorStatistics(video_data, taskCollection),
        'constructive': constructiveStatistics(video_data),
        'improperLanguage': improperLanguageStatistics(video_data),
        'toxicity': toxicityStatistics(video_data),
        'sarcasm': sarcarsmStatistics(video_data),
        'aggressive': aggressiveStatistics(video_data),
        'mockery': mockeryStatistics(video_data),
        'argumentative': argumentativeStatistics(video_data),
        'emotion': emotionStatistics(video_data, taskCollection)
    }
    
    try:
        # Intentar insertar el documento en la colección
        result = statisticsCollection.insert_one(statistic_document)
        print(f"Documento insertado con ID: {result.inserted_id}")

    except PyMongoError as e:
        # Si ocurre un error, imprimir el mensaje de error
        print(f"Error al insertar el documento: {e}")

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

    statistic_document = {
        'taskId': taskCollection['_id'],
        'sentiments': sentimentsStatistics(video_data, taskCollection),
        'offensiveness': offensiveStatistics(video_data),
        'hate': hateStatistics(video_data),
        'stereotypes': stereotypeStatistics(video_data),
        'intolerance': intoleranceStatistics(video_data),
        'insult': insultStatistics(video_data),
        'irony': ironyStatistics(video_data),
        'humor': humorStatistics(video_data, taskCollection),
        'constructive': constructiveStatistics(video_data),
        'improperLanguage': improperLanguageStatistics(video_data),
        'toxicity': toxicityStatistics(video_data),
        'sarcasm': sarcarsmStatistics(video_data),
        'aggressive': aggressiveStatistics(video_data),
        'mockery': mockeryStatistics(video_data),
        'argumentative': argumentativeStatistics(video_data),
        'emotion': emotionStatistics(video_data, taskCollection)
    }
    
    try:
        # Intentar insertar el documento en la colección
        result = statisticsCollection.insert_one(statistic_document)
        print(f"Documento insertado con ID: {result.inserted_id}")

    except PyMongoError as e:
        # Si ocurre un error, imprimir el mensaje de error
        print(f"Error al insertar el documento: {e}")
    

def searchVideo(id, taskCollection):

    result = []

    task_videos = videosCollection.find_one({'taskId': taskCollection['_id']})

    if taskCollection['taskType'] == 'profile':
        # Verificamos que task_videos y list_videos_with_voice existan
        if task_videos and 'list_videos_with_voice' in task_videos:
            # Iteramos sobre cada video dentro de list_videos_with_voice
            for video in task_videos['list_videos_with_voice']:
                if video.get('id') == id:
                    result = video
                    break
    else:
        # Verificamos que task_videos y list_videos existan
        if task_videos and 'list_videos' in task_videos:
            # Iteramos sobre cada video dentro de list_videos
            for video in task_videos['list_videos']:
                if video.get('id') == id:
                    result = video
                    break
    
    return result

def botStatistics(video_data):

    botCount = 0
    humanCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})
        if classification and 'bot' in classification:
            if classification['bot'].get('bot', None) == 1.0:
                botCount += 1
            else:
                humanCount += 1
    if botCount > humanCount:
        bot = 'bot'
    else: 
        bot = 'human'
    
    result = {
        'bot': bot
    }

    return result

def ageStatistics(video_data):

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})
        if classification and 'age' in classification:
            # Obtenemos valores anger
            if classification['age'].get('18-24', None) == 1.0:
                count1 += 1
            elif classification['age'].get('25-34', None) == 1.0:
                count2 += 1
            elif classification['age'].get('35-49', None) == 1.0:
                count3 += 1
            else:
                count4 += 1
    
     # Encontrar el valor máximo y el grupo de edad correspondiente
    max_count = max(count1, count2, count3, count4)
    
    if max_count == count1:
        age_group = '18-24'
    elif max_count == count2:
        age_group = '25-34'
    elif max_count == count3:
        age_group = '35-49'
    else:
        age_group = '50-xx'

    result = {
        'age': age_group
    }

    return result

def genderStatistics(video_data):

    maleCount = 0
    femaleCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})
        if classification and 'gender' in classification:
            # Obtenemos valores anger
            if classification['gender'].get('Male', None) == 1.0:
                maleCount += 1
            else:
                femaleCount += 1
    if maleCount > femaleCount:
        gender = 'male'
    else:
        gender = 'female'

    result = {
        'gender': gender
    }

    return result

def personalityStatistics(video_data):

    averageAgreeable = 0
    averageConscientious = 0
    averageExtroverted = 0
    averageOpen = 0
    averageStable = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'personality' in classification:
            # Obtenemos valores Agreeable
            agreeableValue = classification['personality'].get('Agreeable', None)
            averageAgreeable += agreeableValue

            # Obtenemos valores disgust
            conscientiousValue = classification['personality'].get('Conscientious', None)
            averageConscientious += conscientiousValue

            # Obtenemos valores fear
            extrovertedValue = classification['personality'].get('Extroverted', None)
            averageExtroverted += extrovertedValue

            # Obtenemos valores joy
            openValue = classification['personality'].get('Open', None)
            averageOpen += openValue

            # Obtenemos valores sadness
            stableValue = classification['personality'].get('Stable', None)
            averageStable += stableValue

    # Calculamos los promedios
    averageAgreeable /= numVideos
    averageConscientious /= numVideos
    averageExtroverted /= numVideos
    averageOpen /= numVideos
    averageStable /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageAgreeable + averageConscientious + averageExtroverted + averageOpen + averageStable)

    # Evitar la división por cero
    if total > 0:
        normalizedAgreeable = (averageAgreeable / total) * 100
        normalizedConscientious = (averageConscientious / total) * 100
        normalizedExtroverted = (averageExtroverted / total) * 100
        normalizedOpen = (averageOpen / total) * 100
        normalizedStable = (averageStable / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedAgreeable = normalizedConscientious = normalizedExtroverted = normalizedOpen = normalizedStable = 0

    result = {
        'averageAgreeable': normalizedAgreeable,
        'averageConscientious': normalizedConscientious,
        'averageExtroverted': normalizedExtroverted,
        'averageOpen': normalizedOpen,
        'averageStable': normalizedStable
    }

    return result

def emotionStatistics(video_data, taskCollection):

    averageAnger = 0
    averageDisgust = 0
    averageFear = 0
    averageJoy = 0
    averageSadness = 0
    averageSurprise = 0
    averageOthers = 0

    bestAnger = -float('inf')
    bestDisgust = -float('inf')
    bestFear = -float('inf')
    bestJoy = -float('inf')
    bestSadness = -float('inf')
    bestSurprise = -float('inf')
    bestOthers = -float('inf')

    angerId = None
    disgustId = None
    fearId = None
    joyId = None
    sadnessId = None
    surpriseId = None
    othersId = None

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'emotion' in classification:
            # Obtenemos valores anger
            angerValue = classification['emotion'].get('Anger', None)
            if bestAnger < angerValue:
                bestAnger = angerValue
                angerId = video['id']
            averageAnger += angerValue

            # Obtenemos valores disgust
            disgustValue = classification['emotion'].get('Disgust', None)
            if bestDisgust < disgustValue:
                bestDisgust = disgustValue
                disgustId = video['id']
            averageDisgust += disgustValue

            # Obtenemos valores fear
            fearValue = classification['emotion'].get('Fear', None)
            if bestFear < fearValue:
                bestFear = fearValue
                fearId = video['id']
            averageFear += fearValue

            # Obtenemos valores joy
            joyValue = classification['emotion'].get('Joy', None)
            if bestJoy < joyValue:
                bestJoy = joyValue
                joyId = video['id']
            averageJoy += joyValue

            # Obtenemos valores sadness
            sadnessValue = classification['emotion'].get('Sadness', None)
            if bestSadness < sadnessValue:
                bestSadness = sadnessValue
                sadnessId = video['id']
            averageSadness += sadnessValue

            # Obtenemos valores surprise
            surpriseValue = classification['emotion'].get('Surprise', None)
            if bestSurprise < surpriseValue:
                bestSurprise = surpriseValue
                surpriseId = video['id']
            averageSurprise += surpriseValue

            # Obtenemos valores others
            othersValue = classification['emotion'].get('Others', None)
            if bestOthers < othersValue:
                bestOthers = othersValue
                othersId = video['id']
            averageOthers+= othersValue

    # Calculamos los promedios
    averageAnger /= numVideos
    averageDisgust /= numVideos
    averageFear /= numVideos
    averageJoy /= numVideos
    averageSadness /= numVideos
    averageSurprise /= numVideos
    averageOthers /= numVideos

    result = {
        'averageAnger': averageAnger,
        'bestAnger': bestAnger,
        'angerId': searchVideo(angerId, taskCollection),
        'averageDisgust': averageDisgust,
        'bestDisgust': bestDisgust,
        'disgustId': searchVideo(disgustId, taskCollection),
        'averageFear': averageFear,
        'bestFear': bestFear,
        'fearId': searchVideo(fearId, taskCollection),
        'averageJoy': averageJoy,
        'bestJoy': bestJoy,
        'joyId': searchVideo(joyId, taskCollection),
        'averageSadness': averageSadness,
        'bestSadness': bestSadness,
        'sadnessId': searchVideo(sadnessId, taskCollection),
        'averageSurprise': averageSurprise,
        'bestSurprise': bestSurprise,
        'surpriseId': searchVideo(surpriseId, taskCollection),
        'averageOthers': averageOthers,
        'bestOthers': bestOthers,
        'othersId': searchVideo(othersId, taskCollection)
    }

    return result

def argumentativeStatistics(video_data):

    averageNotArgumentative = 0
    averageArgumentative = 0
    mostArgumentative = -1
    mostArgumentativeVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'argumentation' in classification:
            # Obtenemos el valor de agressive
            argumentativeValue = classification['argumentation'].get('Argumentative', None)

            averageArgumentative += argumentativeValue

            # Obtenemos el valor de not agressive
            notArgumentativeValue = classification['argumentation'].get('Not argumentative', None)

            averageNotArgumentative +=  notArgumentativeValue

            if mostArgumentative < argumentativeValue:
                mostArgumentative = argumentativeValue
                mostArgumentativeVideo = video['id']

    averageArgumentative /= len(video_data)
    averageNotArgumentative /= len(video_data)

    result = {
        'averageArgumentative': averageArgumentative,
        'averageNotArgumentative': averageNotArgumentative,
        'mostArgumentative': mostArgumentative,
        'mostArgumentativeVideo': mostArgumentativeVideo
    }

    return result

def mockeryStatistics(video_data):

    averageNotMockery = 0
    averageMockery = 0
    mostMockery = -1
    mostMockeryVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'mockery' in classification:
            # Obtenemos el valor de agressive
            mockeryValue = classification['mockery'].get('Mockery', None)

            averageMockery += mockeryValue

            # Obtenemos el valor de not agressive
            notMockeryValue = classification['mockery'].get('Not mockery', None)

            averageNotMockery +=  notMockeryValue

            if mostMockery < mockeryValue:
                mostMockery = mockeryValue
                mostMockeryVideo = video['id']

    averageMockery /= len(video_data)
    averageNotMockery /= len(video_data)

    result = {
        'averageMockery': averageMockery,
        'averageNotMockery': averageNotMockery,
        'mostMockery': mostMockery,
        'mostMockeryVideo': mostMockeryVideo
    }

    return result

def aggressiveStatistics(video_data):

    averageNotAggressive = 0
    averageAggressive = 0
    mostAggressive = -1
    mostAggressiveVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'aggressiveness' in classification:
            # Obtenemos el valor de agressive
            aggressiveValue = classification['aggressiveness'].get('Aggressive', None)

            averageAggressive += aggressiveValue

            # Obtenemos el valor de not agressive
            notAggressiveValue = classification['aggressiveness'].get('Not aggressive', None)

            averageNotAggressive +=  notAggressiveValue

            if mostAggressive < aggressiveValue:
                mostAggressive = aggressiveValue
                mostAggressiveVideo = video['id']

    averageAggressive /= len(video_data)
    averageNotAggressive /= len(video_data)

    result = {
        'averageAggressive': averageAggressive,
        'averageNotAggressive': averageNotAggressive,
        'mostAggressive': mostAggressive,
        'mostAggressiveVideo': mostAggressiveVideo
    }

    return result

def toxicityStatistics(video_data):

    toxicityLevel0 = 0
    toxicityLevel1 = 0
    toxicityLevel2 = 0
    toxicityLevel3 = 0

    mostToxicVideo = None
    highestToxicityLevel = -1

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'toxicity' in classification:
            # Obtenemos los valores binarios (0 o 1) para cada nivel de toxicidad
            toxicity_level_0 = classification['toxicity'].get('Toxicity level: 0 (between 0 and 3)', 0)
            toxicity_level_1 = classification['toxicity'].get('Toxicity level: 1 (between 0 and 3)', 0)
            toxicity_level_2 = classification['toxicity'].get('Toxicity level: 2 (between 0 and 3)', 0)
            toxicity_level_3 = classification['toxicity'].get('Toxicity level: 3 (between 0 and 3)', 0)

            # Contar cuántos videos tienen toxicidad en cada nivel
            toxicityLevel0 += toxicity_level_0
            toxicityLevel1 += toxicity_level_1
            toxicityLevel2 += toxicity_level_2
            toxicityLevel3 += toxicity_level_3

            # Calcular el nivel más alto de toxicidad para este video
            maxToxicityForVideo = max([toxicity_level_0 * 0, toxicity_level_1 * 1, toxicity_level_2 * 2, toxicity_level_3 * 3])

            # Si este video tiene un nivel de toxicidad más alto que el actual, lo actualizamos
            if maxToxicityForVideo > highestToxicityLevel:
                highestToxicityLevel = maxToxicityForVideo
                mostToxicVideo = video['id']

    result = {
        'toxicityLevel0': toxicityLevel0,
        'toxicityLevel1': toxicityLevel1,
        'toxicityLevel2': toxicityLevel2,
        'toxicityLevel3': toxicityLevel3,
        'mostToxicVideo': mostToxicVideo,
        'highestToxicityLevel': highestToxicityLevel
    }

    return result

def sarcarsmStatistics(video_data):

    averageSarcastic = 0
    averageNotSarcastic = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'sarcasm' in classification:
            # Obtenemos valores sarcastic
            sarcasticValue = classification['sarcasm'].get('Sarcastic', None)
            averageSarcastic += sarcasticValue

            # Obtenemos valores not sarcastic
            notSarcasticValue = classification['sarcasm'].get('Not sarcastic', None)
            averageNotSarcastic += notSarcasticValue

    # Calculamos los promedios
    averageSarcastic /= numVideos
    averageNotSarcastic /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageSarcastic + averageNotSarcastic)

    # Evitar la división por cero
    if total > 0:
        normalizedSarcastic = (averageSarcastic / total) * 100
        normalizedNotSarcastic = (averageNotSarcastic / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedSarcastic = normalizedNotSarcastic = 0

    result = {
        'averageSarcastic': normalizedSarcastic,
        'averageNotSarcastic': normalizedNotSarcastic
    }

    return result

def offensiveStatistics(video_data):

    offensiveCount = 0
    notOffensiveCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'offensiveness' in classification:
            if classification['offensiveness'].get('Offensive', None) == 1:
                offensiveCount += 1
            else:
                notOffensiveCount += 1

    result = {
        'offensive': offensiveCount,
        'notOffensive': notOffensiveCount
    }

    return result

def insultStatistics(video_data):

    insultCount = 0
    notInsult = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'insult' in classification:
            if classification['insult'].get('With insults', None) == 1:
                insultCount += 1
            else:
                notInsult += 1

    result = {
        'insult': insultCount,
        'notInsult': notInsult
    }

    return result

def improperLanguageStatistics(video_data):

    improperCount = 0
    withoutImproperCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'improper_language' in classification:
            if classification['improper_language'].get('With improper language', None) == 1:
                improperCount += 1
            else:
                withoutImproperCount += 1

    result = {
        'improperLanguage': improperCount,
        'withoutimproperLanguage': withoutImproperCount
    }

    return result

def ironyStatistics(video_data):

    averageIronic = 0
    averageNotIronic = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'irony' in classification:
            # Obtenemos valores ironic
            ironicValue = classification['irony'].get('Ironic', None)
            averageIronic += ironicValue

            # Obtenemos valores not ironic
            notIronicValue = classification['irony'].get('Not ironic', None)
            averageNotIronic += notIronicValue

    # Calculamos los promedios
    averageIronic /= numVideos
    averageNotIronic /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageIronic + averageNotIronic)

    # Evitar la división por cero
    if total > 0:
        normalizedIronic = (averageIronic / total) * 100
        normalizedNotIronic = (averageNotIronic / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedIronic = normalizedNotIronic = 0

    result = {
        'averageIronic': normalizedIronic,
        'averageNotIronic': normalizedNotIronic
    }

    return result

def humorStatistics(video_data, taskCollection):

    humorCount = 0
    notHumorCount = 0

    averageHumor = 0
    averageNoHumor = 0

    bestHumor = -float('inf')
    bestNotHumor = -float('inf')

    humorId = None
    notHumorId = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'humor' in classification:
            humorValue = classification['humor'].get('Humor', None)
            notHumorValue = classification['humor'].get('Not humor', None)

            if humorValue > 0.49:
                humorCount += 1
            else:      
                notHumorCount += 1

            if bestHumor < humorValue:
                bestHumor = humorValue
                humorId = video['id']
            
            if bestNotHumor < notHumorValue:
                bestNotHumor = notHumorValue
                notHumorId = video['id']

            averageHumor += humorValue
            averageHumor += notHumorValue

    averageHumor /= len(video_data)
    averageNoHumor /= len(video_data)

    result = {
        'averageHumor': averageHumor,
        'bestHumor': bestHumor,
        'humorId': searchVideo(humorId, taskCollection),
        'averageNoHumor': averageNoHumor,
        'bestNotHumor': bestNotHumor,
        'notHumorId': searchVideo(notHumorId, taskCollection),
        'videosWithHumor': humorCount,
        'videosWithoutHumor': notHumorCount
    }

    return result

def constructiveStatistics(video_data):

    constructiveCount = 0
    notConstructiveCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'constructiveness' in classification:
            if classification['constructiveness'].get('Constructive', None) == 1:
                constructiveCount += 1
            else:
                notConstructiveCount += 1

    result = {
        'Constructive': constructiveCount,
        'notConstructive': notConstructiveCount
    }

    return result

def intoleranceStatistics(video_data):

    intoleranceCount = 0
    toleranceCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'intolerance' in classification:
            if classification['intolerance'].get('Tolerant', None) == 1:
                toleranceCount += 1
            else:
                intoleranceCount += 1

    result = {
        'tolerance': toleranceCount,
        'intolerance': intoleranceCount
    }

    return result

def hateStatistics(video_data):

    averageHate = 0
    averageNotHate = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'hate' in classification:
            # Obtenemos valores ironic
            hateValue = classification['hate'].get('Hate', None)
            averageHate += hateValue

            # Obtenemos valores not ironic
            notHateValue = classification['hate'].get('Not hate', None)
            averageNotHate += notHateValue

    # Calculamos los promedios
    averageHate /= numVideos
    averageNotHate /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageHate + averageNotHate)

    # Evitar la división por cero
    if total > 0:
        normalizedHate = (averageHate / total) * 100
        normalizedNotHate = (averageNotHate / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedHate = normalizedNotHate = 0

    result = {
        'averageHate': normalizedHate,
        'averageNotHate': normalizedNotHate
    }

    return result

def stereotypeStatistics(video_data):

    withStereotypeCount = 0
    withoutStereotypeCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'stereotype' in classification:
            if classification['stereotype'].get('With stereotypes', None) == 1:
                withStereotypeCount += 1
            else:
                withoutStereotypeCount += 1

    result = {
        'withStereotypes': withStereotypeCount,
        'withoutStereotypes': withoutStereotypeCount
    }

    return result

def sentimentsStatistics(video_data, taskCollection):

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
        'positiveId': searchVideo(positiveId, taskCollection),
        'averageNegative': averageNegative,
        'bestNegative': bestNegative,
        'negativeId': searchVideo(negativeId, taskCollection),
        'averageNeutral': averageNeutral,
        'bestNeutral': bestNeutral,
        'neutralId': searchVideo(neutralId, taskCollection),
        'averageNone': averageNone,
        'bestNone': bestNone,
        'noneId': searchVideo(noneId, taskCollection)
    }

    return result
