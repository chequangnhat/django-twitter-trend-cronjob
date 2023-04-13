from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from trend_app.models import Favorite
from trend_app.models import Trend
from trend_app.models import Location
import json
import requests
# Create your views here.

class TestAPIView(APIView):
  def get(self, request):
    return Response('oke')
  
class NotAuthen (APIView):
  permission_classes = (AllowAny,)
  def get(self, request):
    return Response('oke')
  

endpoint = "https://api.twitter.com/1.1/trends/place.json?id="
endpoint_world = "https://api.twitter.com/1.1/trends/place.json?id=1"
endpoint_vn = "https://api.twitter.com/1.1/trends/place.json?id=23424984"
endpoint_jp = "https://api.twitter.com/1.1/trends/place.json?id=23424856"
headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAGCIjwEAAAAAu%2FyPAplXAQl%2F9YZcj9Rg%2FOyJYBY%3DYWBqPDEl5vhHutWme759g1XFZGNFLKrHO6Jb2KNUFvCBtInRkq"}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
  print("request: ", request.data['username'])
  users = User.objects.get(username=request.data['username'])  
  print("users_id found: ",users.id)
  return Response({"id_user": users.id})
  # return Response({"id_user": request})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_something(request, woeid):
  response_data = json.dumps(requests.get(endpoint+woeid, headers=headers).json()) #transform response data to json
  response_to_dict = json.loads(response_data) 
  # print(response_to_dict)

  return Response({"result": response_to_dict[0]})

@api_view(['GET'])
def auth_get_data(request, woeid):
  response_data = json.dumps(requests.get(endpoint+woeid, headers=headers).json()) #transform response data to json
  response_to_dict = json.loads(response_data) 
  print(response_to_dict)
  return Response({"result": response_to_dict[0]})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_trend(request, woeid):
 
  try:
      location = Location.objects.get(location_code=woeid)
      # location = Location.objects.get(id=1)
      trends = location.trend_set.all().order_by('hour')[:50]
      print("trends: ", trends, "\n")
      print("location: ", location)
      trends_list = []
      # trends = Trend.objects.all()
      for trend in trends:
        new_item = { 
          "id": trend.id,
          "name": trend.trend_name,
          "day": trend.day,
          "hour": trend.hour,
          "tweet_volume": trend.tweet_volume,
        }
        # campaign_list[campaign_index] = new_item
        trends_list.append(new_item)
      return Response({"result": trends_list},status=200)
      
  except Trend.DoesNotExist:
      return Response({"result": "campaign does not exist"},status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_trend(request):
  user_id = request.data['user_id']
  trend_id = request.data['trend_id']
  # day = request.data['day']
  # hour = request.data['hour']

  user_instance = User.objects.get(id=user_id)
  trend_instace = Trend.objects.get(id=trend_id)

  favorite_item = Favorite(trend_id=trend_instace, user_id=user_instance)
  favorite_item.save()
  return Response({ "result": "oke"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_trend(request, user_id):
  # user_id = request.data['user_id']
  user_instance = User.objects.get(id=user_id)
  favorite_list = []
  favorites = user_instance.favorite_set.all()
  for favorite in favorites:
            new_item = {
                "id": favorite.trend_id.id,
                "name": favorite.trend_id.trend_name,
                "day": favorite.trend_id.day,
                "hour": favorite.trend_id.hour,
                "tweet_volume": favorite.trend_id.tweet_volume,
            }
            # campaign_list[campaign_index] = new_item
            favorite_list.append(new_item)
  return Response({ "result": favorite_list})