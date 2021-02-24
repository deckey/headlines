FROM python:3.7-alpine
RUN apk update && apk add bash
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "headlines/headlines.py" ]