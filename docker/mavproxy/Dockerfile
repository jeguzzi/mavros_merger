FROM ubuntu
MAINTAINER Jerome Guzzi "jerome@idsia.ch"

RUN apt-get update && apt-get install -y \
   python-dev python-pip python-lxml

RUN pip install MAVProxy

ENTRYPOINT ["mavproxy.py"]
