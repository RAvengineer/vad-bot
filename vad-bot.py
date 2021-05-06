from requests import get, post
from dotenv import load_dotenv
from os import getenv

API_SETU_URL = 'https://cdn-api.co-vin.in/api/v2/'
APPOINTMENTS_AVAILABILITY = 'appointment/sessions/public/'
CALENDAR_DISTRICT = 'calendarByDistrict'

load_dotenv()
DISCORD_WEBHOOK_URL = getenv('DISCORD_WEBHOOK_URL')

def fetchData(district_id: int, date: str) -> dict:
    params = {
        'district_id': str(district_id),
        'date': date
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'
    }
    resp = get(url = API_SETU_URL+APPOINTMENTS_AVAILABILITY+CALENDAR_DISTRICT, params = params, headers= headers)
    print(f'API response: {resp.status_code}')
    return resp.json()


def get_available_centers(data: dict) -> list:
    available_centers = list()

    for center in data['centers']:
        for session in center['sessions']:
            if(session['available_capacity'] > 0):
                available_centers.append(f"{center['pincode']} - {center['name']}")
                break
    
    return available_centers


def notifyOnDiscord(available_centers: list) -> None:
    body = {
        'content': '**Available centers:**\n' + available_centers
    }
    webhook_params = {
        'Content-Type': 'multipart/form-data' 
    }
    print('Discord Webhook: ', post(url=DISCORD_WEBHOOK_URL, json=body, params=webhook_params))
