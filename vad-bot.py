from requests import get, post
from dotenv import load_dotenv
from os import getenv

API_SETU_URL = 'https://cdn-api.co-vin.in/api/v2/'
APPOINTMENTS_AVAILABILITY = 'appointment/sessions/public/'
CALENDAR_DISTRICT = 'calendarByDistrict'

load_dotenv()
DISCORD_WEBHOOK_URL = getenv('DISCORD_WEBHOOK_URL')

params = {
    'district_id': '394',
    'date': '06-05-2021'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'
}
resp = get(url = API_SETU_URL+APPOINTMENTS_AVAILABILITY+CALENDAR_DISTRICT, params = params, headers= headers)
print(f'API response: {resp.status_code}')
data = resp.json()

available_centers = ''

for center in data['centers']:
    available = False
    for session in center['sessions']:
        if(session['available_capacity'] > 0):
            available = True
            break
    if(available):
        available_centers += f"{center['pincode']} - {center['name']}\n"

if(available_centers):
    body = {
        'content': '**Available centers:**\n' + available_centers
    }
    webhook_params = {
        'Content-Type': 'multipart/form-data' 
    }
    print('Discord Webhook: ', post(url=DISCORD_WEBHOOK_URL, json=body, params=webhook_params))
else:
    print('No centers found')
