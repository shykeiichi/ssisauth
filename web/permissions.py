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

permissions = Blueprint('permissions', __name__, template_folder='templates')


# Get the permissions of a user by their sessionid
@permissions.route("/api/v1/getpermissions", methods=["POST"])
def getpermissions():
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

    cursor.execute("SELECT * FROM permissions")

    result = cursor.fetchall()
    
    permissions_array = []
    for x in result:
        cursor.execute(f"SELECT * FROM authentication WHERE id={x[0]}")
        y = cursor.fetchone()
        # print(x)
        # print(y)
        if(y == None):
            y = ["error", "error", "error", "error", "error", "error"]

        permissions_array.append({
            "id": x[0],
            "mcuuid": y[1],
            "class": y[2],
            "firstname": y[3],
            "surname": y[4],
            "email": y[5],
            "permission": x[1]
        })
    
    return Response(json.dumps(permissions_array), status=200, mimetype="application/json")

# Modify permission level of a user
@permissions.route("/api/v1/promoteplayer", methods=["POST"])
def promoteplayer():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestUsername = request.json.get("username") # WillemD
    requestClass = request.json.get("class") # TE22B
    requestPermission = request.json.get("permission")
    
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    if requestUsername == None:
        return Response(json.dumps("No username was provided"), status=400, mimetype="application/json")

    if requestPermission == None:
        return Response(json.dumps("No permission was provided"), status=400, mimetype="application/json")

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
    
    curtime = int( time.time() )

    cursor.execute(f"INSERT INTO permissions (userid, permission) VALUES (\"{user[0]}\", \"{requestPermission}\")")

    db.commit()
    
    return Response(f"Promoted {requestUsername} to {requestPermission}", status=200, mimetype="application/json")

# Reset a users permission level to default
@permissions.route("/api/v1/demoteplayer", methods=["POST"])
def demoteplayer():
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

    cursor.execute(f"DELETE FROM permissions WHERE userid=\"{requestUserid}\"")

    db.commit()
    
    return Response("Unpromoted player", status=200, mimetype="application/json")