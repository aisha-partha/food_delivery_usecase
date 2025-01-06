# app/Dockerfile

# pull python base image
FROM python:3.10

# copy application files
ADD /app /app

#specify working directory
WORKDIR /app

#installl dependencies
RUN pip install -r requirements.txt

EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health

ENTRYPOINT ["streamlit", "run", "pandas_dataframe_agent.py", "--server.port=8502", "--server.address=0.0.0.0"]