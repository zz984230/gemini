FROM python:3.8

WORKDIR /

RUN git clone https://github.com/AntonVanke/JDBrandMember.git
RUN pip install -r /JDBrandMember/requirements.txt

CMD ["python", "/JDBrandMember/main.py"]