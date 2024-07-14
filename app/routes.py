import random as r
from flask import Flask, session, request, jsonify, abort, render_template
from sqlalchemy.sql.expression import func

from app import app, db
from app.utils import validateTypingData, logWithTime, completion_dict, Delta, isAscii
from typingInstructor.typing import processTypingSession, reconstructFinalString2
from typingInstructor.analytics import *


# from letterboxed.letterboxed import *

from app.models import *


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/text", methods=["GET", "POST"])
def textFunctionality():
    if request.method == "GET":
        allTextsFromDB: list[TextSection] = db.session.execute(db.select(TextSection)).scalars()

        return jsonify({"texts": [t.serializable() for t in allTextsFromDB]})

    if request.method == "POST":
        allTexts = request.get_json()["text"]
        
        for i in range(len(allTexts)):
            if not isAscii(allTexts[i]):
                abort(400, {"message": f"Characters in text {i} need to be ascii"})
            
        addedTexts: list[TextSection] = []
        for text in allTexts:
            newTextSection = TextSection(text, 1)
            addedTexts.append(newTextSection)
            db.session.add(newTextSection)
        db.session.commit()
        return jsonify({"message": "created texts", "texts": [str(t) for t in addedTexts]})


@app.route("/typing/session", methods=["GET", "POST", "PUT"])
def typingSession():

    if request.method == "GET":
        userRequestingNewSession = db.first_or_404(
            db.select(Client).filter_by(ip=request.remote_addr))
        randomText: TextSection = db.session.execute(db.select(TextSection).order_by(func.random())).scalar()
        # check if there is an open session
        sessionOfClient: TypingSession | None = db.session.execute(db.select(TypingSession).filter_by(
            client_id=userRequestingNewSession.id).filter_by(completion_status=0).order_by(TypingSession.id.desc())).scalar()
        
        message = "continuing opened session"

        if sessionOfClient is None:
            sessionOfClient = TypingSession(userRequestingNewSession.id, randomText.id)
            db.session.add(sessionOfClient)
            db.session.commit()
            message = "created new session"
        
        return jsonify({"message": message, "id": sessionOfClient.id, "text": randomText.text_section})


    sessionID = request.args.get("id")
    if sessionID is None:
        return abort(400, {"message": "id query parameter required"})
    typingSession: TypingSession = db.first_or_404(
        db.select(TypingSession).filter_by(id=sessionID))
    

    if request.method == "POST":
        typingSession.completion_status = completion_dict["closed"]
        db.session.commit()
        deltasFromDB: list[TypingSessionDeltas] = db.session.execute(db.select(
            TypingSessionDeltas).filter_by(typing_session_id=sessionID)).scalars()
        text: TextSection = db.session.execute(db.select(TextSection).filter_by(id=typingSession.text_id)).scalar_one()
        
        deltas = [Delta(d.is_addition, d.start, d.stop, d.characters) for d in deltasFromDB]
        
        finalString = reconstructFinalString2(deltas)
        wpm = getFinalWPM(deltas)
        accuracy = getFinalAccuracy(finalString, text)
        
        return jsonify({"message": "closed session", "final_string": finalString, "wpm": wpm, "accuracy": accuracy})


    if request.method == "PUT":
        if typingSession.completion_status == completion_dict["closed"]:
            return abort(423, {"message": "session closed for updates"})
        typingSession.completion_status = completion_dict["started"]
        typingJson = request.get_json()
        for entry in typingJson:
            sign = entry[0][0]
            allItems = entry[0][1:]
            for item in allItems:
                newDelta = TypingSessionDeltas(
                    typingSession.id, f"{sign}{item}", entry[1])
                db.session.add(newDelta)
        db.session.commit()
        return jsonify({"message": "added data to the archives"})
