from app import app, db, admin_create, insert_data

import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')  # Address of your .env file
load_dotenv(dotenv_path)

config_name = os.getenv('FLASK_CONFIG')
app.app_context().push()

if __name__ == "__main__":
    db.create_all()
    insert_data()
    admin_create()
    app.run(debug=True, host='0.0.0.0')

