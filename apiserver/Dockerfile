FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY apiserver.py .
COPY wsgi.ini .
CMD ["uwsgi", "wsgi.ini"]