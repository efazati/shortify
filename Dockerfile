FROM python:3.8
ENV PYTHONPATH "${PYTHONPATH}:/project"
WORKDIR /project/app

COPY ./app /project/app
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]