import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.join(os.path.dirname(__file__), "../data/")

# load_dotenv()
# print(os.getenv("POSTGRES_PW"))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "CHANGE-ME-LATER-PLEASE"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:" +
        f"{os.getenv("POSTGRES_PW")}@" +
        f"{os.getenv("POSTGRES_HOST")}/" +
        f"{os.getenv("POSTGRES_DB")}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)