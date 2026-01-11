FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install discord.py
CMD ["python", "main.py"]
