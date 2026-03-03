FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

# Use gunicorn with proper worker for Dash
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:server"]
