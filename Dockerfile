# nudenet-service/Dockerfile

# 1. Start with an official Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the Python libraries
# --no-cache-dir makes the final container smaller
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our application code (app.py) into the container
COPY . .

# 6. Tell the container what command to run when it starts
# This starts the Gunicorn web server to run our Flask app
# It listens on port 10000, which is what Render.com expects
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:10000", "app:app"]