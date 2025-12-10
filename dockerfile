
FROM python:3.12
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /backend

RUN pip install torch==2.7.1+cu118 torchvision==0.22.1+cu118 torchaudio==2.7.1+cu118 --index-url https://download.pytorch.org/whl/cu118

#Pandoc
RUN apt-get update && apt-get install -y \
    pandoc \
    && rm -rf /var/lib/apt/lists/*
#Imagemagick
# RUN apt-get update && apt-get install -y \
#     imagemagick \
#     libmagickcore-dev \
#     libmagickwand-dev \
#     && rm -rf /var/lib/apt/lists/*

#inkscape
RUN apt-get update && apt-get install -y \
    inkscape \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . /backend
WORKDIR /backend

EXPOSE 8080
ENTRYPOINT ["uvicorn"]

