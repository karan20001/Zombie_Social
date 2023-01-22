from rest_framework.status import *
from django.shortcuts import render
from rest_framework.views import APIView

from user.controller import UserController

from .serializers import UserSerializer, UserLocationSerializer, UserTradingSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import User
import jwt, datetime
from django.contrib.auth.models import update_last_login

from .libs.redis.redis import MasterRedis
from .libs.constants.constants import UserConstant

from .libs.authentication.auth import authentication
from django.forms.models import model_to_dict


# Create your views here.    

class UserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data.get("user_details"))
        serializer.is_valid(raise_exception=True)

        serializer.save()
        print(serializer.data)

        err = UserController().register_user_inventory(request.data.get("inventory_details"),serializer.data.get("id"))

        if(err):
            return Response({"status" : 1,"message" : err}, status = HTTP_400_BAD_REQUEST)

        return Response({"status" : 1,"message" : "Success", "data" : serializer.data}, status = HTTP_200_OK)


    @authentication
    def get(self, request):

        headers = request.headers
        response = Response()
        token = headers.get("Authorization")
        payload = jwt.decode(token, "secret", algorithms=['HS256'])


        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        if user:
            response.data = {
                "message": serializer.data,
                "status": status.HTTP_200_OK
            }
            return response
        else:

            response.data = {
                "message": UserConstant.USER_DATA_NOT_FOUND,
                "status": status.HTTP_400_BAD_REQUEST
            }
            return response


class UserLocationView(APIView):
    
    @authentication
    def patch (self,request, user_id):
        print("aaya")
        serializer = UserLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = request.headers
        token = headers.get("Authorization")
        payload = jwt.decode(token, "secret", algorithms=['HS256'])
        print(serializer)
        res = UserController().update_user_location(user_id, payload['id'], serializer.validated_data)
        return Response({"status" : 1,"message" : "Success", "data" : res}, status = HTTP_200_OK)
        

class UserReportingView(APIView):
    
    @authentication
    def patch (self,request, user_id):
        headers = request.headers
        token = headers.get("Authorization")
        payload = jwt.decode(token, "secret", algorithms=['HS256'])
        try:
            res = UserController().mark_user(user_id, payload['id'])
        except Exception as e:
            print(e)
        return Response({"status" : 1,"message" : "Success", "data" : res}, status = HTTP_200_OK)


class UserTradingingView(APIView):

    @authentication
    def patch(self, request, user_id):
        try:
            headers = request.headers
            token = headers.get("Authorization")
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
            try:

                requested_goods = UserTradingSerializer(data = request.data.get("requested_goods"))
                requested_goods.is_valid(raise_exception=True)
                requested_goods = requested_goods.validated_data
            except Exception as e:
                print(e)

            offered_goods = UserTradingSerializer(data = request.data.get("offered_goods"))
            offered_goods.is_valid(raise_exception=True)
            offered_goods = offered_goods.validated_data
            try:
                res = UserController().trade_inventory(user_id, payload['id'], requested_goods, offered_goods)
            except Exception as e:
                print(e)
            return Response({"status" : 1,"message" : "Success", "data" : res}, status = HTTP_200_OK)
        except Exception as e:
            print(e)

class LoginView(APIView):
    def post(self, request):
        redis = MasterRedis()

        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, "secret", algorithm='HS256')
        update_last_login(None, user)
        key = str(user.id) + UserConstant.REDIS_USER_KEY

        redis.set_keys(key, token)
        response = Response()
        response.data = {'message': 'Successfully Logged In',
                         'jwt': token
                         }
        return response


class LogoutView(APIView):
    @authentication
    def post(self, request):
        headers = request.headers
        token = headers.get("Authorization")
        response = Response()
        redis = MasterRedis()
        if token:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).first()
            if not user:
                response.data = {
                    "message": "Unauthorized",
                }
                return response

            if redis.get_keys(str(user.id) + UserConstant.REDIS_USER_KEY):
                redis.delete_keys(str(user.id) + UserConstant.REDIS_USER_KEY)
                response.data = {
                    "message": "Logged Out",
                    "status": status.HTTP_204_NO_CONTENT,
                }
                return Response(response.data, status=status.HTTP_204_NO_CONTENT)
            else:
                response.data = {
                    "message": "Already Logged Out",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response.data, status=status.HTTP_400_BAD_REQUEST)
        response.data = {
            "message": "Logged Out",
            "status": status.HTTP_204_NO_CONTENT,
        }
        return Response(response.data, status=status.HTTP_204_NO_CONTENT)


class ReportsView(APIView):
    @authentication
    def get(self,request):
        
        res = UserController().generate_report()

        return Response({"status" : 1,"message" : "Success", "data" : res}, status = HTTP_200_OK)
