from flask import Flask, render_template, request, Response, send_file, Blueprint
import mysql.connector
import json, time, uuid, ldap
from markupsafe import escape
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import requests as req

from validation import isValidSession

helpop = Blueprint('helpop', __name__, template_folder='templates')

# A simple admin help system 
@helpop.route("/api/v1/helpop/add", methods=["GET"])
def helpopadd():
    requestMessage = escape(request.args.get("message"))
    requestUsername = escape(request.args.get("username")) # WillemD
    requestClass = escape(request.args.get("class")) # TE22B

    if requestMessage == None:
        return Response(json.dumps("No message was provided"), status=400, mimetype="application/json")

    if requestUsername == None:
        return Response(json.dumps("No username was provided"), status=400, mimetype="application/json")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )
    
    cursor = db.cursor()
    
    cursor.execute(f"SELECT id FROM authentication WHERE firstname=\"{requestUsername[0:-1]}\" AND surname LIKE \"{requestUsername[-1]}%\"" + (f"AND class=\"{requestClass}\"" if str(requestClass) != "null" and requestClass != "" else ""))
    
    result = cursor.fetchall()
    
    if(result == None):
        return Response("No user found", status=400)
    
    if(len(result) > 1):
        return Response("Multiple users found. Please send a class too", status=300)

    # print(result)
    curtime = int( time.time() )
    cursor.execute(f"INSERT INTO helpop (userid, message, timestamp) VALUES (\"{result[0][0]}\", \"{requestMessage}\", \"{curtime}\")")

    db.commit()

    return Response(json.dumps("Comitted"), status=200, mimetype="application/json")

# Get all current helpop tickets
@helpop.route("/api/v1/helpop/getall", methods=["POST"])
def gethelpop():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    sessiondict = isValidSession(requestSessionid)
    if(sessiondict == False or sessiondict == None):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")

    if(sessiondict["permission"] != 1):
        return Response(json.dumps("You're not admin nerd"), status=400, mimetype="application/json")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT * FROM helpop")

    result = cursor.fetchall()
    
    permissions_array = []
    for x in result:
        cursor.execute(f"SELECT * FROM authentication WHERE id={x[1]}")
        y = cursor.fetchone()
        # print(x)
        # print(y)
        if(y == None):
            y = ["error", "error", "error", "error", "error", "error"]

        permissions_array.append({
            "id": x[0],
            "userid": x[1],
            "mcuuid": y[1],
            "class": y[2],
            "firstname": y[3],
            "surname": y[4],
            "email": y[5],
            "message": x[2],
            "timestamp": x[3]
        })
    
    return Response(json.dumps(permissions_array), status=200, mimetype="application/json")

# Resolve helpop ticket eg. removing it
@helpop.route("/api/v1/helpop/markresolved", methods=["POST"])
def markresolved():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestHelpopID = request.json.get("id")
    
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    if requestHelpopID == None:
        return Response(json.dumps("No helpop id was provided"), status=400, mimetype="application/json")
    
    sessiondict = isValidSession(requestSessionid)
    if(sessiondict == False or sessiondict == None):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")

    if(sessiondict["permission"] != 1):
        return Response(json.dumps("You're not admin nerd"), status=400, mimetype="application/json")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute(f"DELETE FROM helpop WHERE id=\"{requestHelpopID}\"")

    db.commit()
    
    return Response("Marked as resolved", status=200, mimetype="application/json")
