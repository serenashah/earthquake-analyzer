FROM centos:7.9.2009

RUN yum update -y && \
    yum install -y python3

RUN pip3 install --user Flask==2.0.3
RUN pip3 install --user redis


RUN mkdir /app
WORKDIR /app
COPY all_month.csv /app
COPY app.py /app

ENTRYPOINT ["python3"]
CMD ["app.py"]