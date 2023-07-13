from flask import Flask, render_template, request, Response, send_file, Blueprint
import mysql.connector
import json, time, uuid, ldap
from markupsafe import escape
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import requests as req

validation = Blueprint('validation', __name__, template_folder='templates')

# Check if the given sessionID is a valid session 
def isValidSession(sessionid):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )
    
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sessionid}\"")

    result = cursor.fetchone()
    
    if result == None:
        return False
    
    # Delete the session if it's yonger than a month to keep some security
    if(int(time.time() - int(result[2])) > 2419200):
        cursor.execute(f"DELETE FROM sessions WHERE sessionid={sessionid}")
        return False
    
    # Get the permission level of the user in the database eg User or Staff
    cursor.execute("SELECT * FROM permissions WHERE userid=\"" + str(result[1]) + "\"")

    permission = cursor.fetchone()
    
    # Get the users information like email, name and school class
    cursor.execute("SELECT * FROM authentication WHERE id=\"" + str(result[1]) + "\"")

    result = cursor.fetchone()
   
    if(result == None):
        return False


    # Parse the users information into a dictionary for ease of use
    result = {
        "id": result[0],
        "mcuuid": result[1],
        "class": result[2],
        "firstname": result[3],
        "surname": result[4],
        "email": result[5],
        "permission": 0 if permission == None else permission[1]
    }
    return result;
    
# The endpoint for the server to check if the user is valid 
# This code is horrid because of javas lack of good json support so i just send a formatted sring and parse it in java 
# This function is agony
@validation.route("/api/v1/checkuserjava", methods=["GET"])
def checkuserjava():    
    mcuuid = escape(request.args.get("uuid"))

    if(mcuuid == None):
        return Response("No uuid provided", status=400)

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute(f"SELECT * FROM authentication WHERE mcuuid=\"{mcuuid}\"")

    result = cursor.fetchone()

    if(result == None):
        return Response("Registrera konto på https://mc.ssis.nu", status=400)

    cursor.execute(f"SELECT * FROM restricted_players WHERE userid=\"{result[0]}\"")

    restricted = cursor.fetchone()
    # print(restricted)
    if(restricted != None):
        restrictedmessage = f"Du är bannlyst!\n{restricted[1]}"
        if(restricted[3] != None):
            restrictedmessage = "\nTills: " + datetime.utcfromtimestamp(restricted[3]).strftime('%Y-%m-%d %H:%M:%S')
        restrictedmessage += "\nKontakta #keii för frågor"
            
        return Response(restrictedmessage, status=400)

    cursor.execute("SELECT * FROM permissions WHERE userid=\"" + str(result[0]) + "\"")

    permission = cursor.fetchone()

    return Response(f"{result[0]},{result[1]},{result[2]},{result[3]},{result[4]},{permission[1] if permission != None else 0}", status=200)

# Get the minecraft username of a player by their firstname + first letter of surname eg. if you input "WillemD" you would get "ReasonsToLive"
@validation.route("/api/v1/whouser", methods=["GET"])
def whouser():
    username = escape(request.args.get("username")) # WillemD
    userclass = escape(request.args.get("class")) # TE22B
    # print(username)
    
    if("None" in str(username)):
        return Response("No user provided", status=400)
    
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute(f"SELECT * FROM authentication WHERE firstname=\"{username[0:-1]}\" AND surname LIKE \"{username[-1]}%\"" + (f"AND class=\"{userclass}\"" if "None" not in str(userclass) else ""))

    result = cursor.fetchall()
    
    if(result == None):
        return Response("No user found", status=400)
    
    if(len(result) > 1):
        return Response("Multiple users found. Please send a class too", status=300)
    
    try:
        response =  req.get(f"https://playerdb.co/api/player/minecraft/{result[0][1]}");
    except:
        return Response("Invalid user", status=400)
    
    return json.loads(response.text)["data"]["player"]["username"]

# Check if a session is valid
@validation.route("/api/v1/validatesession", methods=["POST"])
def validatesession():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")

    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )
    
    cursor = db.cursor()

    sessiondict = isValidSession(requestSessionid) 
    if(sessiondict == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")

    return Response(json.dumps(sessiondict), status=200, mimetype="application/json")