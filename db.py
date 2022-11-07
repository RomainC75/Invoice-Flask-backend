from flask_sqlalchemy import SQLAlchemy
import app 

db = SQLAlchemy()

#=====================================

from sqlalchemy import create_engine
from dotenv import load_dotenv

engine = create_engine("sqlite:///instance/data.db")
