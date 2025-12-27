FROM python:3.13

WORKDIR /app

COPY Gud_habit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Gud_habit .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]