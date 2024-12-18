# # 베이스 이미지 설정 (Python 3.11.4 버전 사용)
# FROM python:3.11.4

# # 업데이트 및 필요한 패키지 설치
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     default-libmysqlclient-dev \
#     pkg-config

# # 작업 디렉토리 설정
# WORKDIR /countfit

# # 의존성 파일 복사 및 설치
# COPY requirements.txt /countfit/
# RUN pip install --no-cache-dir -r requirements.txt

# # 소스 코드 복사
# COPY . /countfit/

# # 환경 변수 설정 (Django 설정에서 디버그 모드를 비활성화)
# ENV DJANGO_ENV=production
# ENV PYTHONUNBUFFERED=1

# WORKDIR /countfit/account_server
# # Collect static files
# # RUN python manage.py collectstatic --noinput

# # 8000 포트 노출 (Django의 기본 포트)
# EXPOSE 8000

# # Django 애플리케이션 실행 명령어
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# # CMD ["gunicorn", "account_server.wsgi:application", "--bind", "0.0.0.0:8000"]


# 베이스 이미지로 Python 3.12 slim 버전 사용
FROM python:3.12-slim

# 필요한 패키지를 미리 설치
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y python3-pip pkg-config libmysqlclient-dev git nginx

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    nginx

# 작업 디렉토리 설정
WORKDIR /countfit

# 소스 코드 복사
COPY . /countfit/

# 프로젝트 의존성 설치
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# 백엔드 서버 디렉토리로 이동
WORKDIR /countfit/account_server

# uWSGI 설치
RUN pip3 install uwsgi

# uWSGI 설정 파일 복사 (로컬에서 준비된 uwsgi.ini를 컨테이너로 복사)
COPY uwsgi.ini /countfit/account_server/uwsgi.ini

# Nginx 설정 파일 복사 (로컬에서 준비된 nginx.conf를 복사하여 Nginx 설정)
COPY nginx.conf /etc/nginx/nginx.conf
COPY default /etc/nginx/sites-enabled/default

# Nginx 포트 오픈
EXPOSE 80

# uWSGI와 Nginx 시작
# CMD uwsgi --ini uwsgi.ini && service nginx start
# CMD ["sh", "-c", "uwsgi --ini uwsgi.ini & nginx -g 'daemon off;'"]
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && uwsgi --ini uwsgi.ini & nginx -g 'daemon off;'"]