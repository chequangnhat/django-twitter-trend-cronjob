from django.contrib.auth import get_user_model
from celery import shared_task
from django_celery_project import settings
from trend_app.models import Trend
from trend_app.models import Favorite
from trend_app.models import Location
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import requests

load_dotenv()

def save_trend_to_db(dict_trend, location_instance):
    current_datetime = datetime.now()
    for trend in dict_trend:
        trend_item = Trend(trend_name = trend["name"], tweet_volume = int(trend["tweet_volume"]) if trend["tweet_volume"] != None else 9999 , \
                        day = current_datetime.strftime('%Y-%m-%d'), hour = current_datetime.strftime('%H'), \
                        location_id = location_instance)
        # trend_item.save()

@shared_task(bind=True)
def get_hourly_trend(self):
    endpoint = "https://api.twitter.com/1.1/trends/place.json?id="
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAGCIjwEAAAAAu%2FyPAplXAQl%2F9YZcj9Rg%2FOyJYBY%3DYWBqPDEl5vhHutWme759g1XFZGNFLKrHO6Jb2KNUFvCBtInRkq"}
    
    response_world_data = json.loads(json.dumps(requests.get(endpoint+"1", headers=headers).json())) #transform response data to json
    response_vietnam_data = json.loads(json.dumps(requests.get(endpoint+"23424984", headers=headers).json())) #transform response data to json
    response_japan_data = json.loads(json.dumps(requests.get(endpoint+"23424856", headers=headers).json())) #transform response data to json
    
    dict_world_trend = response_world_data[0]["trends"]
    dict_vietnam_trend = response_vietnam_data[0]["trends"]
    dict_japan_trend = response_japan_data[0]["trends"]
    
    print("cronjob get data world: ",dict_world_trend[0])
    # print("cronjob get data vietnam: ",dict_vietnam_trend[0])
    # print("cronjob get data japan: ",dict_japan_trend[0])
   
    location_world = Location.objects.get(location_code = "1")
    location_vietnam = Location.objects.get(location_code = "23424984")
    location_japan = Location.objects.get(location_code = "23424856")

    # save_trend_to_db(dict_world_trend, location_world)
    # save_trend_to_db(dict_vietnam_trend, location_vietnam)
    # save_trend_to_db(dict_japan_trend, location_japan)

    current_datetime = datetime.now()

    for trend in dict_world_trend:
        trend_item = Trend(trend_name = trend["name"], tweet_volume = int(trend["tweet_volume"]) if trend["tweet_volume"] != None else 9999 , \
                        day = current_datetime.strftime('%Y-%m-%d'), hour = current_datetime.strftime('%H'), \
                        location_id = location_world)
        print(trend_item.trend_name)
        trend_item.save()
    for trend in dict_vietnam_trend:
        trend_item = Trend(trend_name = trend["name"], tweet_volume = int(trend["tweet_volume"]) if trend["tweet_volume"] != None else 9999 , \
                        day = current_datetime.strftime('%Y-%m-%d'), hour = current_datetime.strftime('%H'), \
                        location_id = location_vietnam)
        trend_item.save()
    for trend in dict_japan_trend:
        trend_item = Trend(trend_name = trend["name"], tweet_volume = int(trend["tweet_volume"]) if trend["tweet_volume"] != None else 9999 , \
                        day = current_datetime.strftime('%Y-%m-%d'), hour = current_datetime.strftime('%H'), \
                        location_id = location_japan)
        trend_item.save()


    return "Get Hourly trend done"