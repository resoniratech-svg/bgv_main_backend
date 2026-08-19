FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
