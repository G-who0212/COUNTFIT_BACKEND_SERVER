from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token # access token & refresh token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer, UserRegisterSerializer, UserInfoListSerializer, UserSerializer, RecordSerializer
from .models import User, Record
from django_filters.rest_framework import DjangoFilterBackend

from django.utils import timezone


class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request: Request):
        token_serializer = TokenObtainPairSerializer(data=request.data) # 로그인 정보를 바탕으로 토큰 발급
        if token_serializer.is_valid():
            user = token_serializer.user
            serializer = UserLoginSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": token_serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request: Request):
        user = request.user  # 현재 토큰으로 인증된 사용자
        serializer = UserInfoListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        user = request.user  # 현재 인증된 사용자
        serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 유저 정보 업데이트
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        user = request.user  # 현재 인증된 사용자
        user.delete()  # 사용자 계정 삭제
        return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class RecordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        user = request.user
        sport_type = request.data.get('sport_type')
        aim_count = request.data.get('aim_count')
        done_count = request.data.get('done_count')
        
        if not sport_type or not aim_count or not done_count:
            return Response({"error": "필수 데이터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        record_data = {
            'sport_type': sport_type,
            'aim_count': aim_count,
            'done_count': done_count,
            'done_at': timezone.now(),
            'user': request.user.id
        }

        serializer = RecordSerializer(data=record_data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)