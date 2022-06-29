FROM python:3.10
RUN apt-get update \
	&& apt-get install -y

WORKDIR /django-website
COPY . .
RUN pip install -r requirements.txt


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]