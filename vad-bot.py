from requests import get, post
from dotenv import load_dotenv
from os import getenv
from time import sleep
from datetime import datetime

API_SETU_URL = 'https://cdn-api.co-vin.in/api/v2/'
APPOINTMENTS_AVAILABILITY = 'appointment/sessions/public/'
CALENDAR_DISTRICT = 'calendarByDistrict'

load_dotenv()
DISCORD_WEBHOOK_URL = getenv('DISCORD_WEBHOOK_URL')

def fetchCalendarByDistrict(district_id: int, date: datetime) -> dict:
    params = {
        'district_id': str(district_id),
        'date': date.strftime("%d-%m-%Y")
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'
    }
    resp = get(url = API_SETU_URL+APPOINTMENTS_AVAILABILITY+CALENDAR_DISTRICT, params = params, headers= headers)

    print(f'{str(date)}\tAPI response: {resp.status_code}')
    if(resp.status_code != 200):
        return None
    return resp.json()


def getNewCenters(old_centers: list, new_centers: list) -> list: 
    x:set = set(old_centers)
    y:set = set(new_centers)
    return list(y.union(x).difference(x))


def getAvailableCenters(data: dict) -> list:
    available_centers = list()

    for center in data['centers']:
        for session in center['sessions']:
            if(session['available_capacity'] > 0):
                available_centers.append(f"{center['pincode']} - {center['name']}")
                break
    
    return available_centers


def notifyOnDiscord(available_centers: list) -> None:
    body = {
        'content': '**Available centers:**\n' + '\n'.join(available_centers)
    }
    webhook_params = {
        'Content-Type': 'multipart/form-data' 
    }
    print('Discord Webhook: ', post(url=DISCORD_WEBHOOK_URL, json=body, params=webhook_params))


if __name__ == "__main__":
    try:
        previous_centers = list()
        while(True):
            dt = datetime.now()
            data = fetchCalendarByDistrict(district_id=getenv('DISTRICT_ID'), date=dt)
            if(not data):
                raise Exception('API_Error: fetchCalendarByDistrict returned None')
            centers = getNewCenters(
                old_centers=previous_centers, 
                new_centers=getAvailableCenters(data)
            )
            previous_centers = centers
            if(centers):
                notifyOnDiscord(available_centers = centers)
            sleep(30)
    except Exception as e:
        print(str(e))
