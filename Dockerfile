FROM python:3.12
ADD . /opt/app
WORKDIR /opt/app
RUN apt update && apt install -y ffmpeg
RUN pip install .
ENTRYPOINT ["python", "app.py"]