FROM python:3.10-slim
WORKDIR /app
COPY entrypoint.py ./
COPY vless.url ./
RUN pip install urllib3
CMD ["python", "entrypoint.py"]