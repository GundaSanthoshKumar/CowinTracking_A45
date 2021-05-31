from datetime import datetime
import requests
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

def is_fourtyfive_plus(session):
    return session["age_limit"] == 45

def is_eighteen_plus(session):
    return session["age_limit"] == 18

def get_for_seven_days(start_date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    params = {"pincode": 508207, "date": start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_sessions(data) if is_fourtyfive_plus(session) and is_available(session)],[session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]

def create_output(session_info):
    return f"{session_info['date']} \n {session_info['name']} \n {session_info['vaccine']} - Dose 1: {session_info['dose_1']} || Dose 2: {session_info['dose_2']} available - {session_info['fee']} \n"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
domain_Url="https://api.telegram.org/bot"
method="sendMessage"
chat_id=["-523622434","-233775793"]
api_key=["1830209817:AAEygMG_lYMKNYI54ESxXP9UnTBfwmOMDIg/","1854734036:AAGedBgAyC8t3Ayp10Knos4Sj7xHNKroiQo/"]

while(1) :

    for i in range(len(api_key)) :
        content1 = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today())[i]])
        welcome = f"{domain_Url}{api_key[i]}{method}?chat_id={chat_id[i]}&text=Tracking%20Started"
        requests.get(welcome)

        if not content1:
            x=requests.get(f"{domain_Url}{api_key[i]}{method}?chat_id={chat_id[i]}&text=Not%20Available%20in%20your%20Pincode")
            print(x)
            print("No availability")
        else:
            x=requests.get(f"{domain_Url}{api_key[i]}{method}?chat_id={chat_id[i]}&text="+content1)
            print(x)
            print(content1)

    time.sleep(60*60*1)