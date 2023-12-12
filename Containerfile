FROM registry.access.redhat.com/ubi9/python-311
WORKDIR /edge_src/
COPY edge_client.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV CLIENT_ID=
ENV CLIENT_SECRET=

EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "edge_client.py", "run", "--host=0.0.0.0", "--port=5000"]