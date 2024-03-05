FROM python:3.9

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Install any needed dependencies 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
