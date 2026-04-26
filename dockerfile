FROM python:3.9-slim
WORKDIR /app
COPY python_script/ .
CMD ["python", "hello.py"]
