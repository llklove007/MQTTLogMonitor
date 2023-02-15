# 建立 python3.9 环境
FROM python:3.9

# 镜像作者
MAINTAINER lv

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置pip源为国内源
COPY pip.conf /root/.pip/pip.conf


RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .


EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]






