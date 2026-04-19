FROM python:3.11

WORKDIR /app

COPY car_rental/requirements.txt .
RUN pip install -r requirements.txt

COPY car_rental/ .

EXPOSE 8080

CMD python manage.py migrate && gunicorn car_rental.wsgi:application --bind 0.0.0.0:$PORT