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

restrictions = Blueprint('restrictions', __name__, template_folder='templates')

# Get all restricted players in a list of dictionaries
@restrictions.route("/api/v1/getrestrictedplayers", methods=["POST"])
def getrestricted():
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

    cursor.execute("SELECT * FROM restricted_players")

    result = cursor.fetchall()
    
    restricted_players_array = []
    for x in result:
        cursor.execute(f"SELECT * FROM authentication WHERE id={x[0]}")
        y = cursor.fetchone()
        # print(x)
        
        restricted_players_array.append({
            "id": x[0],
            "message": x[1],
            "bannedat": x[2],
            "bannedto": x[3],
            "mcuuid": y[1],
            "class": y[2],
            "firstname": y[3],
            "surname": y[4],
            "email": y[5]
        })
    
    return Response(json.dumps(restricted_players_array), status=200, mimetype="application/json")

# Restrict a player eg. ban them
@restrictions.route("/api/v1/restrictplayer", methods=["POST"])
def restrictplayer():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestUsername = request.json.get("username") # WillemD
    requestClass = request.json.get("class") # TE22B
    requestMessage = request.json.get("message")
    requestBannedto = request.json.get("bannedto")
    
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    if requestUsername == None:
        return Response(json.dumps("No username was provided"), status=400, mimetype="application/json")

    if requestMessage == None:
        return Response(json.dumps("No message was provided"), status=400, mimetype="application/json")

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

    if(len(requestUsername) < 2):
        return Response(json.dumps("Invalid name length"), status=400, mimetype="application/json")
    
    cursor.execute(f"SELECT * FROM authentication WHERE firstname=\"{requestUsername[0:-1]}\" AND surname LIKE \"{requestUsername[-1]}%\"" + (f"AND class=\"{requestClass}\"" if requestClass != None and requestClass != "" else ""))

    user = cursor.fetchone()
    if(user == None):
        return Response(json.dumps("Invalid userid"), status=400, mimetype="application/json")
    
    cursor.execute(f"SELECT * FROM restricted_players WHERE userid=\"{user[0]}\"")

    restricteddict = cursor.fetchone()
    if(restricteddict != None):
        return Response(json.dumps("User already banned"), status=400, mimetype="application/json")
    
    curtime = int( time.time() )

    if(requestBannedto != None and requestBannedto != ""):
        cursor.execute(f"INSERT INTO restricted_players (userid, message, bannedat, bannedto) VALUES (\"{user[0]}\", \"{requestMessage}\", \"{curtime}\", \"{requestBannedto}\")")
    else:
        cursor.execute(f"INSERT INTO restricted_players (userid, message, bannedat) VALUES (\"{user[0]}\", \"{requestMessage}\", \"{curtime}\")")

    db.commit()
    
    return Response(f"Banned {requestUsername}", status=200, mimetype="application/json")

# Unban player
@restrictions.route("/api/v1/unbanplayer", methods=["POST"])
def unbanplayer():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestUserid = request.json.get("userid")
    
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    if requestUserid == None:
        return Response(json.dumps("No userid was provided"), status=400, mimetype="application/json")
    
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

    cursor.execute(f"DELETE FROM restricted_players WHERE userid=\"{requestUserid}\"")

    db.commit()
    
    return Response("Unbanned player", status=200, mimetype="application/json")