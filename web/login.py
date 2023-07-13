from flask import Flask, render_template, request, Response, send_file, Blueprint
import mysql.connector
import json, time, uuid, ldap
from markupsafe import escape
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import requests as req

CLIENT_ID = "496641110476-irlpvhj9aprq30dq8ff59dpddlfctu3q.apps.googleusercontent.com"

login = Blueprint('login', __name__, template_folder='templates')

# Handle google login from index.html and if the email doesn't exist in the database then send them to the login page
@login.route("/api/v1/googlelogin", methods=["POST"])
def googlelogin():
    token = request.form.get("credential")
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    
    if("stockholmscience.se" not in idinfo["email"]):
        return render_template("invalidemail.html", email=idinfo["email"])
    
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute(f"SELECT * FROM authentication WHERE email=\"{idinfo['email']}\"")

    result = cursor.fetchone()
    
    curtime = int( time.time() )
    sessionid = str(uuid.uuid4())
    if(result != None):
        cursor.execute(f"INSERT INTO sessions (sessionid, userid, timestamp) VALUES (\"{sessionid}\", \"{result[0]}\", {curtime})")

    db.commit()

    if(result != None):
        return render_template("existingaccount.html", session=sessionid)

    return render_template("login.html", firstname=idinfo["given_name"], surname=idinfo["family_name"] ,email=idinfo["email"], session=sessionid)

@login.route("/api/v1/registeruser", methods=["POST"])
def registeruser():
    mcdata = request.json.get("mcdata")
    firstname = request.json.get("firstname")
    surname = request.json.get("surname")
    email = request.json.get("email")

    if mcdata == None:
        return Response(json.dumps("Invalid mcdata"), status=400, mimetype="application/json")
    if firstname == None:
        return Response(json.dumps("Invalid firstname"), status=400, mimetype="application/json")
    if surname == None:
        return Response(json.dumps("Invalid surname"), status=400, mimetype="application/json")
    if email == None:
        return Response(json.dumps("Invalid email"), status=400, mimetype="application/json")
    
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="temppass",
        database="mcdb"
    )

    cursor = db.cursor(buffered=True)

    cursor.execute(f"SELECT * FROM authentication WHERE email=\"{email}\"")

    result = cursor.fetchone()
    if(result != None):
        return render_template("existingaccount.html")

    #password = open("pass", "r").read().split("\n")[0]
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize("ldaps://ad.ssis.nu")
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.bind_s("22widi@ad.ssis.nu", "Dinkel2006!")
    res = l.search_s("OU=Elever,DC=ad,DC=ssis,DC=nu", ldap.SCOPE_ONELEVEL, f"(sAMAccountName={email.split('@')[0]})", ["cn", "givenName", "sn", "memberOf"])
    userclass = ""
    for dn,entry in res:
        # print('Processing',repr(dn))
        userclass = entry["memberOf"][1].decode("UTF-8").split(",")[0].split("=")[1]
 
    l.unbind()

    cursor.execute(f"INSERT INTO authentication (mcuuid, class, firstname, surname, email) VALUES (\"{mcdata['data']['player']['id']}\", \"{userclass}\", \"{firstname}\", \"{surname}\", \"{email}\")")

    db.commit()

    return mcdata