FROM python:latest 

WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . . 

#CMD [ "flask" , "run" , "-h" , "0.0.0.0" ] will be in compose file 
