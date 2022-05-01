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

ENV LC_CTYPE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8  
ENV LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8  