FROM python:3.7
ENV PROJECT_ROOT /usr/src/app
RUN mkdir $PROJECT_ROOT
COPY requirements.txt $PROJECT_ROOT

WORKDIR $PROJECT_ROOT
RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]
