FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "headlines/headlines.py" ]