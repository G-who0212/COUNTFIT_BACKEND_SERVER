#!/bin/bash

# 애플리케이션 디렉토리로 이동
cd /home/ubuntu/COUNTFIT_BACKEND_SERVER

# 기존 컨테이너가 실행 중이면 중지하고 삭제
docker stop my-django-app-container || true
docker rm my-django-app-container || true

# Docker 이미지 빌드
docker build -t my-django-app .

# 컨테이너 실행 (백그라운드 모드)
docker run -d --name my-django-app-container -p 80:80 my-django-app