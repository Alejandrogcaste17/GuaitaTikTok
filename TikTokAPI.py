import requests
import json
import time

def videosWithVoiceToText(response):
    for video in response["data"]["videos"]:
        if "voice_to_text" in video:
            results.append(video)

# Define las credenciales de la aplicación
client_key = 'awoy8doraswxa914'
client_secret = 'C1Fq10WTwgYygDlteNj8KDWLZTK5EaRe'

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
    access_token = auth_data['access_token']
    expires_in = auth_data['expires_in']  # Tiempo de expiración en segundos
    token_type = auth_data['token_type']  # Debería ser 'Bearer'
    print(json.dumps(auth_data, indent=4))
    
    print("Token de acceso:", access_token)
    print("Expira en (segundos):", expires_in)
    print("Tipo de token:", token_type)
else:
    print('Error al obtener el token de acceso:', auth_response.status_code)

#access_token = "clt.HnTWjtoT2b7kMs5ozRCJkhTC9vFkrGPbEvTmZnbX8ul3fdqvZa3s9KmAyKal"
# Define la URL de la solicitud
url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,video_description,create_time,voice_to_text'

data = {
    "query": {
        "and": [
            { "operation": "IN", "field_name": "region_code", "field_values": ["ES"] },
            { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["politica"] }
        ]
    },
    "max_count": 100,
    "start_date": "20240401",
    "end_date": "20240430"
    
}

# Define los encabezados de la solicitud
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Realiza la solicitud POST
response = requests.post(url, json=data, headers=headers)
results = []
# Procesa la respuesta
if response.status_code == 200:

    response_data = response.json()
    videosWithVoiceToText(response_data)
    #print(json.dumps(response_data, indent=4))
    print('Esperamos 8 segundos...')
    time.sleep(8)
    while response_data["data"]["cursor"] < 1000:

        data["cursor"] = response_data["data"]["cursor"]
        data["search_id"] = response_data["data"]["search_id"]
        print(response_data["data"]["search_id"])
        print(json.dumps(data, indent=4))

        # Realiza la solicitud POST
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            videosWithVoiceToText(response_data)
        else:
            print('Error al realizar la solicitud:', response.status_code)
            print(response.text)
            break
    
    for video in results:
            print(json.dumps(video, indent=4))
    print("El tamaño de results es: ", len(results))
else:
    print('Error al realizar la solicitud:', response.status_code)
    print(response.text)

