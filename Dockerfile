FROM python:3.10.6-slim

# Install app
WORKDIR /usr/app
COPY . /usr/app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Battlesnake
CMD [ "python", "main.py" ]