from datetime import datetime
import requests
import urllib.parse
import json 
import time

def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "address": center["address"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"],
            "vaccine": session["vaccine"],
            "fee": center["fee_type"],
            "dose_1": session["available_capacity_dose1"],
            "dose_2": session["available_capacity_dose2"]}

def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)

def is_available(session):
    return session["capacity"] > 0

def is_eighteen_plus(session):
    return session["age_limit"] == 45

def get_for_seven_days(start_date):
    # url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    # params = {"district_id": 141, "date": start_date.strftime("%d-%m-%Y")}
    params = {"pincode": 110001, "date": start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]

def create_output(session_info):
    return f"{session_info['date']} \n {session_info['name']} \n {session_info['vaccine']} - Dose 1: {session_info['dose_1']} || Dose 2: {session_info['dose_2']} available - {session_info['fee']} \n"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

# while(1) :
welcome = "https://api.telegram.org/bot1830209817:AAEygMG_lYMKNYI54ESxXP9UnTBfwmOMDIg/sendMessage?chat_id=-523622434&text=Tracking%20Started"
requests.get(welcome)
# print(get_for_seven_days(datetime.today()))
content = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today())])

if not content:
    out_url = "https://api.telegram.org/bot1830209817:AAEygMG_lYMKNYI54ESxXP9UnTBfwmOMDIg/sendMessage?chat_id=-523622434&text=Not%20Available%20in%20your%20Pincode"
    x=requests.get(out_url)
    print(x)
    print("No availability")
else:
    out_url = "https://api.telegram.org/bot1830209817:AAEygMG_lYMKNYI54ESxXP9UnTBfwmOMDIg/sendMessage?chat_id=-523622434&text="+content
    x=requests.get(out_url)
    print(x)
    print(content)
    # time.sleep(60)