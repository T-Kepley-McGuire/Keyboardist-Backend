
import os
from dotenv import load_dotenv
from flask import Flask, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy import create_engine, text
from app.utils import logWithTime
from app.config import Config
from app.errorHandlers import registerErrorHandlers

app = Flask("typing-backend")
# print("Loading dotenv")
# load_dotenv()
# print(os.getenv("POSTGRES_PW"))

app.config.from_object(Config)
db: SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

# from app.models import *

registerErrorHandlers(app)


from app.models import *


@app.before_request
def trackRequest():
    logWithTime("request initiated")
    if "request_count" not in session:
        session["request_count"] = 0
    session["request_count"] += 1

    try:
        client = db.session.execute(db.select(Client).filter_by(ip=request.remote_addr)).scalar_one()
        client.connection_count += 1
        db.session.commit()
    except:
        newClient = Client(request.remote_addr)
        db.session.add(newClient)
        db.session.commit()

    logWithTime("request acknowledged")
    # if "client_data" not in session:
    #     session["client_data"] = []
    # print(request.json)
    # print(request.args.to_dict())
    # print(request.json or request.args.to_dict())
    # if request.is_json:
    #     session["client_data"] = [request.json]
    # else:
    #     session["client_data"] = [request.args.to_dict() or request.remote_addr]
        

@app.after_request
def logSession(request):
    
    logWithTime("finished request")
    return request

from app import routes, models

if __name__ == "__main__":
    app.run()
