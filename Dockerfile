FROM python:3.6.7

RUN pip3 install -U \
  python-dotenv==0.1.5 \
  requests==2.7.0

COPY ./ /root/mandiberg-painting

WORKDIR /root/mandiberg-painting

CMD python getYoutube.py
