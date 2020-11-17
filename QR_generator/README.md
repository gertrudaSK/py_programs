# QR Code Generator

This is simple program that generates QR Code for registration form. This is useful for business controlling the risk of COVID-19.

## Run with virtualenv
- Create a virtualenv folder `virtualenv -p python3 venv`
- Activate `source venv/bin/activate`
- Install the requirements `pip install -r requirements.txt`
- Run the program `python -m run`
- Go to `http://127.0.0.1:8000/`

## Run with Docker
- Activate app.run docker line in run.py and comment another unnecessary one
- Build with docker-compose `docker-compose build`
- Run with docker-compose `docker-compose up -d`
- Go to `http://localhost:5000`
- Stop and remove container `docker-compose down`
