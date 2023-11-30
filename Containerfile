FROM registry.access.redhat.com/ubi9/python-311
RUN pip install requests
WORKDIR /edge_src/
COPY edge_client.py .

ENV CLIENT_ID=
ENV CLIENT_SECRET=

CMD [ "python", "./edge_client.py"]