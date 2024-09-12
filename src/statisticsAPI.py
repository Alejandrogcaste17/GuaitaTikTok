import requests
import json
import time
import asyncio
import sys
import calendar
from datetime import datetime, timedelta
from celery.exceptions import Ignore
from mongoConfiguration import tasksCollection, videosCollection, classificationCollection, statisticsCollection
from pymongo.errors import PyMongoError

def process_statistics_profile_api(taskCollection, current_user):

    print('Empezamos analisis')
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
            create_time = video.get('create_time')
            
            # Añadimos el par (id, voice_to_text) al array
            video_data.append({'id': video_id, 'voice_to_text': voice_to_text, 'create_time': create_time})

    # Buscamos el documento de clasificación que contiene todos los videos
    classification_document = classificationCollection.find_one({'taskId': taskCollection['_id']})

    if classification_document and 'video_classifications' in classification_document:
        video_classifications = classification_document['video_classifications']

    statistic_document = {
        'taskId': taskCollection['_id'],
        'gender': genderStatistics(video_data, video_classifications),
        'age': ageStatistics(video_data, video_classifications),
        'bot': botStatistics(video_data, video_classifications),
        'personality': personalityStatistics(video_data, video_classifications),
        'sentiments': sentimentsStatistics(video_data, video_classifications, taskCollection),
        'offensiveness': offensiveStatistics(video_data, video_classifications),
        'hate': hateStatistics(video_data, video_classifications),
        'stereotypes': stereotypeStatistics(video_data, video_classifications),
        'intolerance': intoleranceStatistics(video_data, video_classifications),
        'insult': insultStatistics(video_data, video_classifications, taskCollection),
        'irony': ironyStatistics(video_data, video_classifications),
        'humor': humorStatistics(video_data, video_classifications, taskCollection),
        'constructive': constructiveStatistics(video_data, video_classifications),
        'improperLanguage': improperLanguageStatistics(video_data, video_classifications, taskCollection),
        'toxicity': toxicityStatistics(video_data, video_classifications),
        'sarcasm': sarcasmStatistics(video_data, video_classifications),
        'aggressive': aggressiveStatistics(video_data, video_classifications),
        'mockery': mockeryStatistics(video_data, video_classifications),
        'argumentative': argumentativeStatistics(video_data, video_classifications),
        'emotion': emotionStatistics(video_data, video_classifications, taskCollection),
        'dateDivision': splitDates(video_data, taskCollection, video_classifications)
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
            create_time = video.get('create_time')
            
            # Añadimos el par (id, voice_to_text) al array
            video_data.append({'id': video_id, 'voice_to_text': voice_to_text, 'create_time': create_time})

    # Buscamos el documento de clasificación que contiene todos los videos
    classification_document = classificationCollection.find_one({'taskId': taskCollection['_id']})

    if classification_document and 'video_classifications' in classification_document:
        video_classifications = classification_document['video_classifications']

    statistic_document = {
        'taskId': taskCollection['_id'],
        'sentiments': sentimentsStatistics(video_data, video_classifications, taskCollection),
        'offensiveness': offensiveStatistics(video_data, video_classifications),
        'hate': hateStatistics(video_data, video_classifications),
        'stereotypes': stereotypeStatistics(video_data, video_classifications),
        'intolerance': intoleranceStatistics(video_data, video_classifications),
        'insult': insultStatistics(video_data, video_classifications, taskCollection),
        'irony': ironyStatistics(video_data, video_classifications),
        'humor': humorStatistics(video_data, video_classifications, taskCollection),
        'constructive': constructiveStatistics(video_data, video_classifications),
        'improperLanguage': improperLanguageStatistics(video_data, video_classifications, taskCollection),
        'toxicity': toxicityStatistics(video_data, video_classifications),
        'sarcasm': sarcasmStatistics(video_data, video_classifications),
        'aggressive': aggressiveStatistics(video_data, video_classifications),
        'mockery': mockeryStatistics(video_data, video_classifications),
        'argumentative': argumentativeStatistics(video_data, video_classifications),
        'emotion': emotionStatistics(video_data, video_classifications, taskCollection),
        'dateDivision': splitDates(video_data, taskCollection, video_classifications)
    }

    
    try:
        # Intentar insertar el documento en la colección
        result = statisticsCollection.insert_one(statistic_document)
        print(f"Documento insertado con ID: {result.inserted_id}")

    except PyMongoError as e:
        # Si ocurre un error, imprimir el mensaje de error
        print(f"Error al insertar el documento: {e}")

def getFormatDate(date):
    # Eliminar los guiones "-" de la fecha original
    result = date.replace("-", "")
    result = datetime.strptime(result, '%Y%m%d')
    return result

def splitDates(video_data, taskCollection, video_classifications):
    print("Empiezan la division por fechas")
    daysDivision = []
    weeksDivision = []
    monthsDivision = []

    startDate = getFormatDate(taskCollection['startDate'])
    endDate = getFormatDate(taskCollection['endDate'])

    currentDate = startDate
    while currentDate <= endDate:
        daysDivision.append({'day': currentDate.strftime('%Y-%m-%d')})
        currentDate +=  timedelta(days=1)
    currentDate = startDate
     # Mueve la fecha al lunes más cercano o al mismo lunes
    currentDate += timedelta(days=(7 - currentDate.weekday()) % 7)

    while currentDate <= endDate:
        weeksDivision.append({
            'week_start': currentDate.strftime('%Y-%m-%d')  # Guardamos solo el lunes de cada semana
        })
        currentDate += timedelta(weeks=1)  # Avanzamos una semana
    # Para las divisiones por meses
    currentDate = startDate
    while currentDate <= endDate:
        monthsDivision.append({
            'month': currentDate.strftime('%Y-%m')  # Solo el mes en formato YYYY-MM
        })
        # Ir al próximo mes
        next_month = currentDate.month % 12 + 1
        next_year = currentDate.year + (currentDate.month // 12)
        currentDate = currentDate.replace(year=next_year, month=next_month, day=1)
    result = {
        'days': daysDivision,
        'weeks': weeksDivision,
        'months': monthsDivision
    }
    print("Acaba la division por fechas")
    return assignVideos(result, video_data, video_classifications)

def assignVideos(divisions, video_data, video_classifications):
    print("Empieza la asignación por fechas")
    
    for video in video_data: 
        
        if video and 'create_time' in video:
            # Convertir el create_time del video en un objeto datetime
            videoDate = getFormatDate(video['create_time'])
            videoDate = videoDate.date()
            # Asignar el video a la división por días
            for day_division in divisions['days']:
                day_date = datetime.strptime(day_division['day'], '%Y-%m-%d').date()
                # Inicializar 'list_videos' como una lista si no existe
                if 'list_videos' not in day_division:
                    day_division['list_videos'] = []
                if day_date == videoDate:
                    day_division['list_videos'].append(video)
                    break

            # Asignar el video a la división por semanas (solo lunes)
            for week_division in divisions['weeks']:
                
                week_start_date = datetime.strptime(week_division['week_start'], '%Y-%m-%d').date()
                week_end_date = week_start_date + timedelta(days=6)

                # Inicializar 'list_videos' como una lista si no existe
                if 'list_videos' not in week_division:
                    week_division['list_videos'] = []
                if week_start_date <= videoDate <= week_end_date:
                    week_division['list_videos'].append(video)
                    break
        
            # Asignar el video a la división por meses
            for month_division in divisions['months']:
                
                month_date = datetime.strptime(month_division['month'], '%Y-%m').date()
                
                # Inicializar 'list_videos' como una lista si no existe
                if 'list_videos' not in month_division:
                    month_division['list_videos'] = []
                if month_date.year == videoDate.year and month_date.month == videoDate.month:
                    month_division['list_videos'].append(video)
                    break
    # Comprobamos si hay dias, semanas o meses vacios, para eliminarlos
    divisions['days'] = [entry for entry in divisions['days'] if len(entry.get('list_videos', [])) > 0]
    divisions['weeks'] = [entry for entry in divisions['weeks'] if len(entry.get('list_videos', [])) > 0]
    divisions['months'] = [entry for entry in divisions['months'] if len(entry.get('list_videos', [])) > 0]


    for day_division in divisions['days']:
        # Calculamos algunas estadisticas por dia
        day_division['aggressiveness'] = []
        day_division['aggressiveness'].append(aggressiveStatistics(day_division['list_videos'], video_classifications))  
        day_division['argumentative'] = []
        day_division['argumentative'].append(argumentativeStatistics(day_division['list_videos'], video_classifications))    
        day_division['offensiveness'] = []
        day_division['offensiveness'].append(offensiveStatistics(day_division['list_videos'], video_classifications))   
        day_division['constructiveness'] = []
        day_division['constructiveness'].append(constructiveStatistics(day_division['list_videos'], video_classifications))
        day_division['intolerance'] = []
        day_division['intolerance'].append(intoleranceStatistics(day_division['list_videos'], video_classifications))
        day_division['stereotype'] = []
        day_division['stereotype'].append(stereotypeStatistics(day_division['list_videos'], video_classifications))

    for week_division in divisions['weeks']:
        # Calculamos algunas estadisticas por semana
        week_division['aggressiveness'] = []
        week_division['aggressiveness'].append(aggressiveStatistics(week_division['list_videos'], video_classifications))
        week_division['argumentative'] = []
        week_division['argumentative'].append(argumentativeStatistics(week_division['list_videos'], video_classifications))
        week_division['offensiveness'] = []
        week_division['offensiveness'].append(offensiveStatistics(week_division['list_videos'], video_classifications))
        week_division['constructiveness'] = []
        week_division['constructiveness'].append(constructiveStatistics(week_division['list_videos'], video_classifications))
        week_division['intolerance'] = []
        week_division['intolerance'].append(intoleranceStatistics(week_division['list_videos'], video_classifications))
        week_division['stereotype'] = []
        week_division['stereotype'].append(stereotypeStatistics(week_division['list_videos'], video_classifications))

    for month_division in divisions['months']:
        # Calculamos algunas estadisticas por mes
        month_division['aggressiveness'] = []
        month_division['aggressiveness'].append(aggressiveStatistics(month_division['list_videos'], video_classifications))
        month_division['argumentative'] = []
        month_division['argumentative'].append(argumentativeStatistics(month_division['list_videos'], video_classifications))
        month_division['offensiveness'] = []
        month_division['offensiveness'].append(offensiveStatistics(month_division['list_videos'], video_classifications))
        month_division['constructiveness'] = []
        month_division['constructiveness'].append(constructiveStatistics(month_division['list_videos'], video_classifications))
        month_division['intolerance'] = []
        month_division['intolerance'].append(intoleranceStatistics(month_division['list_videos'], video_classifications))
        month_division['stereotype'] = []
        month_division['stereotype'].append(stereotypeStatistics(month_division['list_videos'], video_classifications))

    print("Acaba la asignación por fechas")
    return divisions

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

def botStatistics(video_data, video_classifications):

    botCount = 0
    humanCount = 0

    for video in video_data:
        # Buscamos el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'bot' in classification:
            if classification['bot'].get('bot', None) == 1:
                botCount += 1
            else:
                humanCount += 1

    # Decidimos si hay más bots o humanos
    if botCount > humanCount:
        bot = 'bot'
    else:
        bot = 'human'

    result = {
        'bot': bot
    }

    return result

def ageStatistics(video_data, video_classifications):
    # Inicializamos un diccionario para los conteos por grupo de edad
    age_groups = {
        '18-24': 0,
        '25-34': 0,
        '35-49': 0,
        '50-xx': 0
    }

    # Recorremos los videos y obtenemos las clasificaciones de edad
    for video in video_data:
        # Buscamos el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'age' in classification:
            age_classification = classification['age']
            # Aumentamos el conteo para el grupo de edad correspondiente
            if age_classification.get('18-24', 0) == 1:
                age_groups['18-24'] += 1
            elif age_classification.get('25-34', 0) == 1:
                age_groups['25-34'] += 1
            elif age_classification.get('35-49', 0) == 1:
                age_groups['35-49'] += 1
            else:
                age_groups['50-xx'] += 1

    # Encontrar el grupo de edad con el valor máximo
    age_group = max(age_groups, key=age_groups.get)

    # Devolver el resultado con el grupo de edad más frecuente
    result = {
        'age': age_group
    }

    return result

def genderStatistics(video_data, video_classifications):
    maleCount = 0
    femaleCount = 0

    for video in video_data:
        # Buscamos el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)
        
        if classification and 'gender' in classification:
            # Verificamos si es 'male' o 'female'
            if classification['gender'].get('male', None) == 1:
                maleCount += 1
            else:
                femaleCount += 1

    # Determinar el género predominante
    if maleCount > femaleCount:
        gender = 'male'
    else:
        gender = 'female'

    result = {
        'gender': gender
    }

    return result

def personalityStatistics(video_data, video_classifications):
    # Inicializamos las variables para sumar las características
    averageAgreeable = 0
    averageConscientious = 0
    averageExtroverted = 0
    averageOpen = 0
    averageStable = 0

    numVideos = len(video_data)

    for video in video_data:
        # Buscamos el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'personality' in classification:
            # Obtenemos los valores de cada característica y los sumamos
            agreeableValue = classification['personality'].get('Agreeable', 0)
            averageAgreeable += agreeableValue

            conscientiousValue = classification['personality'].get('Conscientious', 0)
            averageConscientious += conscientiousValue

            extrovertedValue = classification['personality'].get('Extroverted', 0)
            averageExtroverted += extrovertedValue

            openValue = classification['personality'].get('Open', 0)
            averageOpen += openValue

            stableValue = classification['personality'].get('Stable', 0)
            averageStable += stableValue

    # Calculamos los promedios
    averageAgreeable /= numVideos
    averageConscientious /= numVideos
    averageExtroverted /= numVideos
    averageOpen /= numVideos
    averageStable /= numVideos

    # Normalizamos los valores para que estén entre 0 y 100
    normalizedAgreeable = ((averageAgreeable + 0.5) / 1) * 100
    normalizedConscientious = ((averageConscientious + 0.5) / 1) * 100
    normalizedExtroverted = ((averageExtroverted + 0.5) / 1) * 100
    normalizedOpen = ((averageOpen + 0.5) / 1) * 100
    normalizedStable = ((averageStable + 0.5) / 1) * 100

    # Devolvemos los resultados como un diccionario
    result = {
        'averageAgreeable': normalizedAgreeable,
        'averageConscientious': normalizedConscientious,
        'averageExtroverted': normalizedExtroverted,
        'averageOpen': normalizedOpen,
        'averageStable': normalizedStable
    }

    return result

def emotionStatistics(video_data, video_classifications, taskCollection):

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
        # Buscamos la clasificación en la lista video_classifications
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'emotion' in classification:
            # Obtenemos valores anger
            angerValue = classification['emotion'].get('Anger', 0)
            if bestAnger < angerValue:
                bestAnger = angerValue
                angerId = video['id']
            averageAnger += angerValue

            # Obtenemos valores disgust
            disgustValue = classification['emotion'].get('Disgust', 0)
            if bestDisgust < disgustValue:
                bestDisgust = disgustValue
                disgustId = video['id']
            averageDisgust += disgustValue

            # Obtenemos valores fear
            fearValue = classification['emotion'].get('Fear', 0)
            if bestFear < fearValue:
                bestFear = fearValue
                fearId = video['id']
            averageFear += fearValue

            # Obtenemos valores joy
            joyValue = classification['emotion'].get('Joy', 0)
            if bestJoy < joyValue:
                bestJoy = joyValue
                joyId = video['id']
            averageJoy += joyValue

            # Obtenemos valores sadness
            sadnessValue = classification['emotion'].get('Sadness', 0)
            if bestSadness < sadnessValue:
                bestSadness = sadnessValue
                sadnessId = video['id']
            averageSadness += sadnessValue

            # Obtenemos valores surprise
            surpriseValue = classification['emotion'].get('Surprise', 0)
            if bestSurprise < surpriseValue:
                bestSurprise = surpriseValue
                surpriseId = video['id']
            averageSurprise += surpriseValue

            # Obtenemos valores others
            othersValue = classification['emotion'].get('Others', 0)
            if bestOthers < othersValue:
                bestOthers = othersValue
                othersId = video['id']
            averageOthers += othersValue

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

def argumentativeStatistics(video_data, video_classifications):

    averageNotArgumentative = 0
    averageArgumentative = 0
    mostArgumentative = -1
    mostArgumentativeVideo = None

    for video in video_data:
        # Buscar el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'argumentation' in classification:
            # Obtenemos el valor de argumentative
            argumentativeValue = classification['argumentation'].get('Argumentative', 0)
            averageArgumentative += argumentativeValue

            # Obtenemos el valor de not argumentative
            notArgumentativeValue = classification['argumentation'].get('Not argumentative', 0)
            averageNotArgumentative += notArgumentativeValue

            if mostArgumentative < argumentativeValue:
                mostArgumentative = argumentativeValue
                mostArgumentativeVideo = video['id']

    averageArgumentative /= len(video_data)
    averageNotArgumentative /= len(video_data)

    # Normalizamos los valores para que sumen 1
    total = (averageArgumentative + averageNotArgumentative)
    if total > 0:
        normalizedArgumentative = (averageArgumentative / total) * 100
        normalizedNotArgumentative = (averageNotArgumentative / total) * 100
    else:
        normalizedArgumentative = normalizedNotArgumentative = 0

    result = {
        'averageArgumentative': normalizedArgumentative,
        'averageNotArgumentative': normalizedNotArgumentative,
        'mostArgumentative': mostArgumentative,
        'mostArgumentativeVideo': mostArgumentativeVideo
    }

    return result

def mockeryStatistics(video_data, video_classifications):

    averageMockery = 0
    averageNotMockery = 0

    numVideos = len(video_data)
    for video in video_data:
        # Buscar el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'mockery' in classification:
            # Obtenemos valores mockery
            mockeryValue = classification['mockery'].get('Mockery', 0)
            averageMockery += mockeryValue

            # Obtenemos valores not mockery
            notMockeryValue = classification['mockery'].get('Not mockery', 0)
            averageNotMockery += notMockeryValue

    # Calculamos los promedios
    averageMockery /= numVideos
    averageNotMockery /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageMockery + averageNotMockery)
    if total > 0:
        normalizedMockery = (averageMockery / total) * 100
        normalizedNotMockery = (averageNotMockery / total) * 100
    else:
        normalizedMockery = normalizedNotMockery = 0

    result = {
        'averageMockery': normalizedMockery,
        'averageNotMockery': normalizedNotMockery
    }

    return result

def aggressiveStatistics(video_data, video_classifications):

    averageNotAggressive = 0
    averageAggressive = 0
    mostAggressive = -1
    mostAggressiveVideo = None

    for video in video_data:
        # Buscar el video correspondiente en la lista de clasificaciones
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'aggressiveness' in classification:
            # Obtenemos el valor de aggressive
            aggressiveValue = classification['aggressiveness'].get('Aggressive', 0)
            averageAggressive += aggressiveValue

            # Obtenemos el valor de not aggressive
            notAggressiveValue = classification['aggressiveness'].get('Not aggressive', 0)
            averageNotAggressive += notAggressiveValue

            if mostAggressive < aggressiveValue:
                mostAggressive = aggressiveValue
                mostAggressiveVideo = video['id']

    averageAggressive /= len(video_data)
    averageNotAggressive /= len(video_data)

    # Normalizamos los valores para que sumen 1
    total = (averageAggressive + averageNotAggressive)
    if total > 0:
        normalizedAggressive = (averageAggressive / total) * 100
        normalizedNotAggressive = (averageNotAggressive / total) * 100
    else:
        normalizedAggressive = normalizedNotAggressive = 0

    result = {
        'averageAggressive': normalizedAggressive,
        'averageNotAggressive': normalizedNotAggressive,
        'mostAggressive': mostAggressive,
        'mostAggressiveVideo': mostAggressiveVideo
    }

    return result

def toxicityStatistics(video_data, video_classifications):

    toxicityLevel0 = 0
    toxicityLevel1 = 0
    toxicityLevel2 = 0
    toxicityLevel3 = 0

    mostToxicVideo = None
    highestToxicityLevel = -1

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'toxicity' in classification:
            toxicity_level_0 = classification['toxicity'].get('Toxicity level: 0 (between 0 and 3)', 0)
            toxicity_level_1 = classification['toxicity'].get('Toxicity level: 1 (between 0 and 3)', 0)
            toxicity_level_2 = classification['toxicity'].get('Toxicity level: 2 (between 0 and 3)', 0)
            toxicity_level_3 = classification['toxicity'].get('Toxicity level: 3 (between 0 and 3)', 0)

            maxToxicityLevel = max(toxicity_level_0, toxicity_level_1, toxicity_level_2, toxicity_level_3)

            if maxToxicityLevel == toxicity_level_0:
                toxicityLevel0 += 1
            elif maxToxicityLevel == toxicity_level_1:
                toxicityLevel1 += 1
            elif maxToxicityLevel == toxicity_level_2:
                toxicityLevel2 += 1
            elif maxToxicityLevel == toxicity_level_3:
                toxicityLevel3 += 1

            if maxToxicityLevel > highestToxicityLevel:
                highestToxicityLevel = maxToxicityLevel
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

def sarcasmStatistics(video_data, video_classifications):

    averageSarcastic = 0
    averageNotSarcastic = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'sarcasm' in classification:
            sarcasticValue = classification['sarcasm'].get('Sarcastic', 0)
            averageSarcastic += sarcasticValue

            notSarcasticValue = classification['sarcasm'].get('Not sarcastic', 0)
            averageNotSarcastic += notSarcasticValue

    averageSarcastic /= numVideos
    averageNotSarcastic /= numVideos

    total = (averageSarcastic + averageNotSarcastic)
    if total > 0:
        normalizedSarcastic = (averageSarcastic / total) * 100
        normalizedNotSarcastic = (averageNotSarcastic / total) * 100
    else:
        normalizedSarcastic = normalizedNotSarcastic = 0

    result = {
        'averageSarcastic': normalizedSarcastic,
        'averageNotSarcastic': normalizedNotSarcastic
    }

    return result

def offensiveStatistics(video_data, video_classifications):

    averageNotOffensive = 0
    averageOffensive = 0
    mostOffensive = -1
    mostOffensiveVideo = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'offensiveness' in classification:
            offensiveValue = classification['offensiveness'].get('Offensive', 0)
            averageOffensive += offensiveValue

            notOffensiveValue = classification['offensiveness'].get('Not offensive', 0)
            averageNotOffensive += notOffensiveValue

            if mostOffensive < offensiveValue:
                mostOffensive = offensiveValue
                mostOffensiveVideo = video['id']

    averageOffensive /= len(video_data)
    averageNotOffensive /= len(video_data)

    total = (averageOffensive + averageNotOffensive)
    if total > 0:
        normalizedOffensive = (averageOffensive / total) * 100
        normalizedNotOffensive = (averageNotOffensive / total) * 100
    else:
        normalizedOffensive = normalizedNotOffensive = 0

    result = {
        'averageOffensive': normalizedOffensive,
        'averageNotOffensive': normalizedNotOffensive,
        'mostOffensive': mostOffensive,
        'mostOffensiveVideo': mostOffensiveVideo
    }

    return result

def insultStatistics(video_data, video_classifications, taskCollection):

    insultCount = 0
    notInsultCount = 0

    averageInsult = 0
    averageNotInsult = 0

    bestInsult = -float('inf')
    bestNotInsult = -float('inf')

    insultId = None
    notInsultId = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'insult' in classification:
            insultValue = classification['insult'].get('With insults', 0)
            notInsultValue = classification['insult'].get('Without insults', 0)

            if insultValue > 0.49:
                insultCount += 1
            else:
                notInsultCount += 1

            if bestInsult < insultValue:
                bestInsult = insultValue
                insultId = video['id']

            if bestNotInsult < notInsultValue:
                bestNotInsult = notInsultValue
                notInsultId = video['id']

            averageInsult += insultValue
            averageNotInsult += notInsultValue

    averageInsult /= len(video_data)
    averageNotInsult /= len(video_data)

    result = {
        'averageInsult': averageInsult,
        'bestInsult': bestInsult,
        'insultId': searchVideo(insultId, taskCollection),
        'averageNotInsult': averageNotInsult,
        'bestNotInsult': bestNotInsult,
        'notInsultId': searchVideo(notInsultId, taskCollection),
        'videosWithInsult': insultCount,
        'videosWithoutInsult': notInsultCount
    }

    return result

def improperLanguageStatistics(video_data, video_classifications, taskCollection):

    improperCount = 0
    withoutImproperCount = 0

    averageImproper = 0
    averageWithoutImproper = 0

    bestImproper = -float('inf')
    bestWithoutImproper = -float('inf')

    improperId = None
    withoutImproperId = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'improper_language' in classification:
            improperValue = classification['improper_language'].get('With improper language', 0)
            withoutImproperValue = classification['improper_language'].get('Without improper language', 0)

            if improperValue > 0.49:
                improperCount += 1
            else:
                withoutImproperCount += 1

            if bestImproper < improperValue:
                bestImproper = improperValue
                improperId = video['id']

            if bestWithoutImproper < withoutImproperValue:
                bestWithoutImproper = withoutImproperValue
                withoutImproperId = video['id']

            averageImproper += improperValue
            averageWithoutImproper += withoutImproperValue

    averageImproper /= len(video_data)
    averageWithoutImproper /= len(video_data)

    result = {
        'averageImproper': averageImproper,
        'bestImproper': bestImproper,
        'improperId': searchVideo(improperId, taskCollection),
        'averageWithoutImproper': averageWithoutImproper,
        'bestWithoutImproper': bestWithoutImproper,
        'withoutImproperId': searchVideo(withoutImproperId, taskCollection),
        'videosWithImproper': improperCount,
        'videosWithoutImproper': withoutImproperCount
    }

    return result

def ironyStatistics(video_data, video_classifications):
    averageIronic = 0
    averageNotIronic = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'irony' in classification:
            ironicValue = classification['irony'].get('Ironic', 0)
            averageIronic += ironicValue

            notIronicValue = classification['irony'].get('Not ironic', 0)
            averageNotIronic += notIronicValue

    averageIronic /= numVideos
    averageNotIronic /= numVideos

    total = (averageIronic + averageNotIronic)
    if total > 0:
        normalizedIronic = (averageIronic / total) * 100
        normalizedNotIronic = (averageNotIronic / total) * 100
    else:
        normalizedIronic = normalizedNotIronic = 0

    result = {
        'averageIronic': normalizedIronic,
        'averageNotIronic': normalizedNotIronic
    }

    return result

def humorStatistics(video_data, video_classifications, taskCollection):

    humorCount = 0
    notHumorCount = 0

    averageHumor = 0
    averageNoHumor = 0

    bestHumor = -float('inf')
    bestNotHumor = -float('inf')

    humorId = None
    notHumorId = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'humor' in classification:
            humorValue = classification['humor'].get('Humor', 0)
            notHumorValue = classification['humor'].get('Not humor', 0)

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
            averageNoHumor += notHumorValue

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

def constructiveStatistics(video_data, video_classifications):

    averageNotConstructive = 0
    averageConstructive = 0
    mostConstructive = -1
    mostConstructiveVideo = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'constructiveness' in classification:
            constructiveValue = classification['constructiveness'].get('Constructive', 0)
            averageConstructive += constructiveValue

            notConstructiveValue = classification['constructiveness'].get('Not constructive', 0)
            averageNotConstructive += notConstructiveValue

            if mostConstructive < constructiveValue:
                mostConstructive = constructiveValue
                mostConstructiveVideo = video['id']

    averageConstructive /= len(video_data)
    averageNotConstructive /= len(video_data)

    total = (averageConstructive + averageNotConstructive)
    if total > 0:
        normalizedConstructive = (averageConstructive / total) * 100
        normalizedNotConstructive = (averageNotConstructive / total) * 100
    else:
        normalizedConstructive = normalizedNotConstructive = 0

    result = {
        'averageConstructive': normalizedConstructive,
        'averageNotConstructive': normalizedNotConstructive,
        'mostConstructive': mostConstructive,
        'mostConstructiveVideo': mostConstructiveVideo
    }

    return result

def intoleranceStatistics(video_data, video_classifications):

    averageIntolerant = 0
    averageTolerant = 0
    mostTolerant = -1
    mostTolerantVideo = None

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'intolerance' in classification:
            tolerantValue = classification['intolerance'].get('Tolerant', 0)
            averageTolerant += tolerantValue

            intolerantValue = classification['intolerance'].get('Intolerant', 0)
            averageIntolerant += intolerantValue

            if mostTolerant < tolerantValue:
                mostTolerant = tolerantValue
                mostTolerantVideo = video['id']

    averageTolerant /= len(video_data)
    averageIntolerant /= len(video_data)

    total = (averageTolerant + averageIntolerant)
    if total > 0:
        normalizedTolerant = (averageTolerant / total) * 100
        normalizedIntolerant = (averageIntolerant / total) * 100
    else:
        normalizedTolerant = normalizedIntolerant = 0

    result = {
        'averageTolerant': normalizedTolerant,
        'averageIntolerant': normalizedIntolerant,
        'mostTolerant': mostTolerant,
        'mostTolerantVideo': mostTolerantVideo
    }

    return result

def hateStatistics(video_data, video_classifications):

    averageHate = 0
    averageNotHate = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'hate' in classification:
            hateValue = classification['hate'].get('Hate', 0)
            averageHate += hateValue

            notHateValue = classification['hate'].get('Not hate', 0)
            averageNotHate += notHateValue

    averageHate /= numVideos
    averageNotHate /= numVideos

    total = (averageHate + averageNotHate)
    if total > 0:
        normalizedHate = (averageHate / total) * 100
        normalizedNotHate = (averageNotHate / total) * 100
    else:
        normalizedHate = normalizedNotHate = 0

    result = {
        'averageHate': normalizedHate,
        'averageNotHate': normalizedNotHate
    }

    return result

def stereotypeStatistics(video_data, video_classifications):

    stereotypesCount = 0
    notStereotypesCount = 0

    totalStereotypes = 0
    totalNotStereotypes = 0

    for video in video_data:
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'stereotype' in classification:
            stereotypesValue = classification['stereotype'].get('With stereotypes', 0)
            notStereotypesValue = classification['stereotype'].get('Without stereotypes', 0)

            totalStereotypes += stereotypesValue
            totalNotStereotypes += notStereotypesValue

            if stereotypesValue > 0.5:
                stereotypesCount += 1
            else:
                notStereotypesCount += 1

    averageStereotypes = totalStereotypes / len(video_data)
    averageNotStereotypes = totalNotStereotypes / len(video_data)

    result = {
        'averageStereotypes': averageStereotypes,
        'averageNotStereotypes': averageNotStereotypes,
        'videosWithStereotypes': stereotypesCount,
        'videosWithoutStereotypes': notStereotypesCount
    }

    return result

def sentimentsStatistics(video_data, video_classifications, taskCollection):

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
        classification = next((item for item in video_classifications if item['videoId'] == video['id']), None)

        if classification and 'sentiment' in classification:
            negativeValue = classification['sentiment'].get('Negative', 0)
            if bestNegative < negativeValue:
                bestNegative = negativeValue
                negativeId = video['id']
            averageNegative += negativeValue

            PositiveValue = classification['sentiment'].get('Positive', 0)
            if bestPositive < PositiveValue:
                bestPositive = PositiveValue
                positiveId = video['id']
            averagePositive += PositiveValue

            NeutralValue = classification['sentiment'].get('Neutral', 0)
            if bestNeutral < NeutralValue:
                bestNeutral = NeutralValue
                neutralId = video['id']
            averageNeutral += NeutralValue

            NoneValue = classification['sentiment'].get('None', 0)
            if bestNone < NoneValue:
                bestNone = NoneValue
                noneId = video['id']
            averageNone += NoneValue

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
