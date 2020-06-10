from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from core.database import get_db, query_db, upsert_query
# from api.whatsapp import send

import datetime, json
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

bp = Blueprint('scheduler', __name__, url_prefix='/scheduler')


def set_session():
    query = """SELECT 
    dl.dog_id
    , name
    , dl.last_loo_break
    , dl.last_fed
    , dl.last_weighed
    , dh.loo_intervals
    , dh.food_intervals
FROM dog_last AS dl
    JOIN dogs AS d on dl.dog_id=d.id 
    LEFT JOIN dog_habbits AS dh on d.id=dh.dog_id
WHERE dl.dog_id IN (SELECT dog_owners.dog_id FROM dog_owners WHERE user_id=?)"""



    for dog in query_db(query, [session.get('user_id'), ]):
        tom_index = next((index for (index, d) in enumerate(session['dogs']) if dog["dog_id"] == d['id']), None)
        #print(dog['last_loo_break'], dog['loo_intervals'])
        if None not in [dog['last_loo_break'], dog['loo_intervals']]:
            next_loo = dog['last_loo_break'] + datetime.timedelta(minutes=dog['loo_intervals'])
        if None not in [dog['last_loo_break'], dog['loo_intervals']]:
            next_loo = dog['last_loo_break'] + datetime.timedelta(minutes=dog['loo_intervals'])

        #next_feed = datetime.datetime(dog['last_loo_break']) + datetime.timedelta(minutes=dog['food_intervals'])
        session['dogs'][tom_index].update(
            dict(
                name=dog['name'],
                last_fed=dog['last_fed'],
                last_weighed=dog['last_weighed'],
                last_loo_break=dog['last_loo_break'],
                scheduled_loo=next_loo
            )
        )
        #scheduler = BackgroundScheduler()
        #scheduler.add_job(func=send_msg("Hello from fnction"), trigger="interval", seconds=10)
        #scheduler.start()

        #atexit.register(lambda: scheduler.shutdown())

# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

def send_msg(msg):
    from twilio.rest import Client
    from os import environ
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    TWILIO_ACCOUNT_SID = environ.get('PS_TWILIO_SID')
    AUTH_TOKEN = environ.get('PS_TWILIO_AUTH_TOKEN')

    client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = 'whatsapp'.join([environ.get('PS_PHONE_NUM')])
    message = client.messages.create(body=msg,
                                     from_=from_whatsapp_number,
                                     to=to_whatsapp_number)
    print(message.sid)
    return