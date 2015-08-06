# Any suggestions to switch this to FROM ubuntu will be taken out back and
# lectured on copyright and free software licenses.
#
# http://blog.dustinkirkland.com/2015/07/appellation-of-origin-from-ubuntu.html

FROM fedora


# uwsgi is installed because gunicorn fedora container + debian host = sads
RUN mkdir /srv/app && \
    dnf install -y python-pip gcc python-devel && \
    pip install honcho uwsgi && \
    dnf erase -y gcc python-devel

WORKDIR /srv/app


# Add requirements.txt separately to cache those before the more frequently
# out-of-date ADD later on

COPY requirements.txt /srv/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /srv/app

ENV PORT 3000
EXPOSE 3000

CMD ["honcho", "start"]
