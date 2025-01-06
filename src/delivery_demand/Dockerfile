# app/Dockerfile

# pull python base image
FROM python:3.10

# copy application files
ADD /app /app

#specify working directory
WORKDIR /app

#installl dependencies
RUN pip install -r requirements.txt

EXPOSE 8503


CMD ["streamlit", "run", "demand_prediction.py", "--server.port=8503", "--server.address=0.0.0.0"]