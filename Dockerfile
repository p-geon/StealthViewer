FROM python:3.7
LABEL version="0.1"
LABEL purpose="python3.7-base"

ENV DIR_DOCKER=.
ENV DEBCONF_NOWARNINGS yes
ENV WORKDIR=/work

COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y --quiet --no-install-recommends \
	vim \
	wget
# for lycon
RUN apt-get install -y -q \
	cmake \
	build-essential \
	libjpeg-dev \
	libpng-dev

RUN pip install -q --upgrade pip
RUN pip install -r requirements.txt -q

RUN pip install lycon

WORKDIR ${WORKDIR}
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["python3", "./test.py"]