from datetime import datetime
import pandas
import random
import smtplib
import os
import json
from twilio.rest import Client

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
FROM_NUMBER = os.environ.get("MY_TWILIO")
TO_NUMBER = os.environ.get("MY_PHONE")
OWN_ENDPOINT = os.environ.get("OWN_ENDPOINT")
API_KEY = os.environ.get("API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]",birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )

weather_params = {
    "lat": 25.442188,
    "lon": 81.840920,
    "appid": API_KEY,
    "cnt":4,
}

response = requests.get(OWN_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = True
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int (condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body= "sms_event_notifications",
        from_= FROM_NUMBER,
        to= TO_NUMBER,
    )

    #print(message.status)
