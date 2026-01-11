FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install discord.py
RUN pip install icalendar
RUN pip install pytz 
RUN pip install aiohttp
CMD ["python", "main.py"]
