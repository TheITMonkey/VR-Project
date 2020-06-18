FROM python:latest

RUN pip3 install flask

RUN pip3 install requests

WORKDIR /home/mail_app

COPY src/createDB.py src/postgres.py src/auth_server.py src/database.ini src/config.py .
RUN ls -la && pwd
EXPOSE 5000/tcp

RUN python3 createDB.py

CMD [ "python3","auth_server.py" ]
#RUN python3 mail_app.py
