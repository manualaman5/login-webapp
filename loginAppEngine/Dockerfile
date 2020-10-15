FROM ubuntu:latest
RUN apt update -y
RUN apt upgrade -y
RUN apt install python3-pip -y
RUN pip3 install --upgrade setuptools pip
RUN pip3 install --upgrade pip
COPY index.html index.html
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY main.py main.py
COPY app.yaml app.yaml
EXPOSE 80
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
