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
        'insult': insultStatistics(video_data, taskCollection),
        'irony': ironyStatistics(video_data),
        'humor': humorStatistics(video_data, taskCollection),
        'constructive': constructiveStatistics(video_data),
        'improperLanguage': improperLanguageStatistics(video_data, taskCollection),
        'toxicity': toxicityStatistics(video_data),
        'sarcasm': sarcarsmStatistics(video_data),
        'aggressive': aggressiveStatistics(video_data),
        'mockery': mockeryStatistics(video_data),
        'argumentative': argumentativeStatistics(video_data),
        'emotion': emotionStatistics(video_data, taskCollection),
        'dateDivision': splitDates(video_data, taskCollection)
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

    statistic_document = {
        'taskId': taskCollection['_id'],
        'sentiments': sentimentsStatistics(video_data, taskCollection),
        'offensiveness': offensiveStatistics(video_data),
        'hate': hateStatistics(video_data),
        'stereotypes': stereotypeStatistics(video_data),
        'intolerance': intoleranceStatistics(video_data),
        'insult': insultStatistics(video_data, taskCollection),
        'irony': ironyStatistics(video_data),
        'humor': humorStatistics(video_data, taskCollection),
        'constructive': constructiveStatistics(video_data),
        'improperLanguage': improperLanguageStatistics(video_data, taskCollection),
        'toxicity': toxicityStatistics(video_data),
        'sarcasm': sarcarsmStatistics(video_data),
        'aggressive': aggressiveStatistics(video_data),
        'mockery': mockeryStatistics(video_data),
        'argumentative': argumentativeStatistics(video_data),
        'emotion': emotionStatistics(video_data, taskCollection),
        'dateDivision': splitDates(video_data, taskCollection)
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

def splitDates(video_data, taskCollection):
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
    return assignVideos(result, video_data)

def assignVideos(divisions, video_data):
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
        day_division['aggressiveness'].append(aggressiveStatistics(day_division['list_videos']))  
        day_division['argumentative'] = []
        day_division['argumentative'].append(argumentativeStatistics(day_division['list_videos']))    
        day_division['offensiveness'] = []
        day_division['offensiveness'].append(offensiveStatistics(day_division['list_videos']))   
        day_division['constructiveness'] = []
        day_division['constructiveness'].append(constructiveStatistics(day_division['list_videos']))
        day_division['intolerance'] = []
        day_division['intolerance'].append(intoleranceStatistics(day_division['list_videos']))

    for week_division in divisions['weeks']:
        # Calculamos algunas estadisticas por semana
        week_division['aggressiveness'] = []
        week_division['aggressiveness'].append(aggressiveStatistics(week_division['list_videos']))
        week_division['argumentative'] = []
        week_division['argumentative'].append(argumentativeStatistics(week_division['list_videos']))
        week_division['offensiveness'] = []
        week_division['offensiveness'].append(offensiveStatistics(week_division['list_videos']))
        week_division['constructiveness'] = []
        week_division['constructiveness'].append(constructiveStatistics(week_division['list_videos']))
        week_division['intolerance'] = []
        week_division['intolerance'].append(intoleranceStatistics(week_division['list_videos']))

    for month_division in divisions['months']:
        # Calculamos algunas estadisticas por mes
        month_division['aggressiveness'] = []
        month_division['aggressiveness'].append(aggressiveStatistics(month_division['list_videos']))
        month_division['argumentative'] = []
        month_division['argumentative'].append(argumentativeStatistics(month_division['list_videos']))
        month_division['offensiveness'] = []
        month_division['offensiveness'].append(offensiveStatistics(month_division['list_videos']))
        month_division['constructiveness'] = []
        month_division['constructiveness'].append(constructiveStatistics(month_division['list_videos']))
        month_division['intolerance'] = []
        month_division['intolerance'].append(intoleranceStatistics(month_division['list_videos']))

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

def botStatistics(video_data):

    botCount = 0
    humanCount = 0

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})
        if classification and 'bot' in classification:
            if classification['bot'].get('bot', None) == 1:
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
            if classification['age'].get('18-24', None) == 1:
                count1 += 1
            elif classification['age'].get('25-34', None) == 1:
                count2 += 1
            elif classification['age'].get('35-49', None) == 1:
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
            if classification['gender'].get('male', None) == 1:
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
    # Inicializamos las variables para sumar las características
    averageAgreeable = 0
    averageConscientious = 0
    averageExtroverted = 0
    averageOpen = 0
    averageStable = 0

    numVideos = len(video_data)

    for video in video_data:
        # Buscamos la clasificación en la colección
        classification = classificationCollection.find_one({'videoId': video['id']})

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

    # Normalizamos los valores para que sumen 1
    total = (averageArgumentative + averageNotArgumentative)

    # Evitar la división por cero
    if total > 0:
        normalizedArgumentative = (averageArgumentative / total) * 100
        normalizedNotArgumentative = (averageNotArgumentative / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedArgumentative = normalizedNotArgumentative = 0

    result = {
        'averageArgumentative': normalizedArgumentative,
        'averageNotArgumentative': normalizedNotArgumentative,
        'mostArgumentative': mostArgumentative,
        'mostArgumentativeVideo': mostArgumentativeVideo
    }

    return result

def mockeryStatistics(video_data):

    averageMockery = 0
    averageNotMockery = 0

    numVideos = len(video_data)
    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'mockery' in classification:
            # Obtenemos valores mockery
            mockeryValue = classification['mockery'].get('Mockery', None)
            averageMockery += mockeryValue

            # Obtenemos valores not mockery
            notMockeryValue = classification['mockery'].get('Not mockery', None)
            averageNotMockery += notMockeryValue

    # Calculamos los promedios
    averageMockery /= numVideos
    averageNotMockery /= numVideos

    # Normalizamos los valores para que sumen 1
    total = (averageMockery + averageNotMockery)

    # Evitar la división por cero
    if total > 0:
        normalizedMockery = (averageMockery / total) * 100
        normalizedNotMockery = (averageNotMockery / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedMockery = normalizedNotMockery = 0

    result = {
        'averageMockery': normalizedMockery,
        'averageNotMockery': normalizedNotMockery
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

    # Normalizamos los valores para que sumen 1
    total = (averageAggressive + averageNotAggressive)

    # Evitar la división por cero
    if total > 0:
        normalizedAgressive = (averageAggressive / total) * 100
        normalizedNotAgressive = (averageNotAggressive / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedAgressive = normalizedNotAgressive = 0

    result = {
        'averageAggressive': normalizedAgressive,
        'averageNotAggressive': normalizedNotAgressive,
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
            # Obtenemos los valores de toxicidad para cada nivel
            toxicity_level_0 = classification['toxicity'].get('Toxicity level: 0 (between 0 and 3)', 0)
            toxicity_level_1 = classification['toxicity'].get('Toxicity level: 1 (between 0 and 3)', 0)
            toxicity_level_2 = classification['toxicity'].get('Toxicity level: 2 (between 0 and 3)', 0)
            toxicity_level_3 = classification['toxicity'].get('Toxicity level: 3 (between 0 and 3)', 0)

            # Identificar el nivel de toxicidad más alto para este video
            maxToxicityLevel = max(toxicity_level_0, toxicity_level_1, toxicity_level_2, toxicity_level_3)

            # Determinar cuál nivel tiene el valor más alto y sumar al contador correspondiente
            if maxToxicityLevel == toxicity_level_0:
                toxicityLevel0 += 1
            elif maxToxicityLevel == toxicity_level_1:
                toxicityLevel1 += 1
            elif maxToxicityLevel == toxicity_level_2:
                toxicityLevel2 += 1
            elif maxToxicityLevel == toxicity_level_3:
                toxicityLevel3 += 1

            # Si este video tiene un nivel de toxicidad más alto que el actual, lo actualizamos
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

    averageNotOffensive = 0
    averageOffensive = 0
    mostOffensive = -1
    mostOffensiveVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'offensiveness' in classification:
            # Obtenemos el valor de agressive
            offensiveValue = classification['offensiveness'].get('Offensive', None)

            averageOffensive += offensiveValue

            # Obtenemos el valor de not agressive
            notOffensiveValue = classification['offensiveness'].get('Not offensive', None)

            averageNotOffensive +=  notOffensiveValue

            if mostOffensive < offensiveValue:
                mostOffensive = offensiveValue
                mostOffensiveVideo = video['id']

    averageOffensive /= len(video_data)
    averageNotOffensive /= len(video_data)

    # Normalizamos los valores para que sumen 1
    total = (averageOffensive + averageNotOffensive)

    # Evitar la división por cero
    if total > 0:
        normalizedOffensive = (averageOffensive / total) * 100
        normalizedNotOffensive = (averageNotOffensive / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedOffensive = normalizedNotOffensive = 0

    result = {
        'averageOffensive': normalizedOffensive,
        'averageNotOffensive': normalizedNotOffensive,
        'mostOffensive': mostOffensive,
        'mostOffensiveVideo': mostOffensiveVideo
    }

    return result

def insultStatistics(video_data, taskCollection):

    print("empezamos insult")
    insultCount = 0
    notInsultCount = 0

    averageInsult = 0
    averageNotInsult = 0

    bestInsult = -float('inf')
    bestNotInsult = -float('inf')

    insultId = None
    notInsultId = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'insult' in classification:
            insultValue = classification['insult'].get('With insults', None)
            notInsultValue = classification['insult'].get('Without insults', None)

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
    print("acabamos insult")
    return result

def improperLanguageStatistics(video_data, taskCollection):
    print("empezamos improper")

    improperCount = 0
    withoutImproperCount = 0

    averageImproper = 0
    averageWithoutImproper = 0

    bestImproper = -float('inf')
    bestWithoutImproper = -float('inf')

    improperId = None
    withoutImproperId = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'improper_language' in classification:
            improperValue = classification['improper_language'].get('With improper language', None)
            withoutImproperValue = classification['improper_language'].get('Without improper language', None)

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
    print("acabamos improper")
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

    averageNotConstructive = 0
    averageConstructive = 0
    mostConstructive = -1
    mostConstructiveVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'constructiveness' in classification:
            # Obtenemos el valor de constructive
            constructiveValue = classification['constructiveness'].get('Constructive', None)

            averageConstructive += constructiveValue

            # Obtenemos el valor de not constructive
            notConstructiveValue = classification['constructiveness'].get('Not constructive', None)

            averageNotConstructive += notConstructiveValue

            if mostConstructive < constructiveValue:
                mostConstructive = constructiveValue
                mostConstructiveVideo = video['id']

        averageConstructive /= len(video_data)
        averageNotConstructive /= len(video_data)

        # Normalizamos los valores para que sumen 1
        total = (averageConstructive + averageNotConstructive)

        # Evitar la división por cero
        if total > 0:
            normalizedConstructive = (averageConstructive / total) * 100
            normalizedNotConstructive = (averageNotConstructive / total) * 100
        else:
            # Si no hay datos válidos, todos son cero
            normalizedConstructive = normalizedNotConstructive = 0

        result = {
            'averageConstructive': normalizedConstructive,
            'averageNotConstructive': normalizedNotConstructive,
            'mostConstructive': mostConstructive,
            'mostConstructiveVideo': mostConstructiveVideo
        }

        return result

def intoleranceStatistics(video_data):

    averageIntolerant = 0
    averageTolerant = 0
    mostTolerant = -1
    mostTolerantVideo = None

    for video in video_data:
        classification = classificationCollection.find_one({'videoId': video['id']})

        if classification and 'intolerance' in classification:
            # Obtenemos el valor de tolerant
            tolerantValue = classification['intolerance'].get('Tolerant', None)

            averageTolerant += tolerantValue

            # Obtenemos el valor de intolerant
            intolerantValue = classification['intolerance'].get('Intolerant', None)

            averageIntolerant += intolerantValue

            if mostTolerant < tolerantValue:
                mostTolerant = tolerantValue
                mostTolerantVideo = video['id']

    averageTolerant /= len(video_data)
    averageIntolerant /= len(video_data)

    # Normalizamos los valores para que sumen 1
    total = (averageTolerant + averageIntolerant)

    # Evitar la división por cero
    if total > 0:
        normalizedTolerant = (averageTolerant / total) * 100
        normalizedIntolerant = (averageIntolerant / total) * 100
    else:
        # Si no hay datos válidos, todos son cero
        normalizedTolerant = normalizedIntolerant = 0

    result = {
        'averageTolerant': normalizedTolerant,
        'averageIntolerant': normalizedIntolerant,
        'mostTolerant': mostTolerant,
        'mostTolerantVideo': mostTolerantVideo
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
