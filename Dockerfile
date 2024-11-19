FROM python:3.9

WORKDIR /ChatApp

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
COPY src /ChatApp/src
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "src.chat_app:app", "--host", "0.0.0.0", "--port", "8000"]