# Standard Python libraries.
import os
import cgi
import hashlib
import sqlite3

# The Flask library, a lightweight web application framework.
import flask

# The Flask-Caching in-memory store, used to store values (i.e. login tokens) between executions of this script.
import flask_caching

# The Requests library, for handling HTTP(S) calls.
import requests



# Instantiate the Flask app, set configuration values.
app = flask.Flask(__name__)
app.config.from_mapping({
    # Set values for the Flask-Caching module.
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "tmp",
    "CACHE_DEFAULT_TIMEOUT": 1800
})
# Instantiate the cache object.
loginTokenCache = flask_caching.Cache(app)



def getFile(theFilename):
    fileDataHandle = open(theFilename, encoding="latin-1")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

def putFile(theFilename, theData):
    fileDataHandle = open(theFilename, "w", encoding="latin-1")
    fileDataHandle.write(fileData)
    fileDataHandle.close()

def runCommand(theCommand):
    commandHandle = os.popen(theCommand)
    result = commandHandle.read()
    commandHandle.close()
    return(result)

@app.route("/", methods=['GET'])
def photoUpload():
    return "User interface goes here."

@app.route("/api/mystartLogin", methods=['GET', 'POST'])
def mystartLogin():
    if flask.request.method == 'POST':
        loginToken = flask.request.form.get("loginToken")
        loginTokenValidationRequest = requests.get("https://dev.mystart.online/api/validateToken?loginToken=" + loginToken + "&pageName=" + "0000000000000002")
        if loginTokenValidationRequest.status_code == 200:
            return "Session validated! Token: " + loginToken
        else:
            return "Login error."
    else:
        return "Was a GET."

        #userData = loginTokenCache.get(loginToken)
        #if userData:
            #userData["login"] = "valid"
            #return userData

    #dbCon = sqlite3.connect("sessions.db")
    #dbCur = dbCon.cursor()

    # /home/dhicks6345789/gamadv-xtd3/gam select knightsbridgeschool info domain

if __name__ == "__main__":
    app.run()
