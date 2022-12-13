# Standard Python libraries.
import os
import uuid

# The Flask library, a lightweight web application framework.
import flask

# Flask-Caching, used to store session tokens.
import flask_caching

# The Requests library, for handling HTTP(S) calls.
import requests



# Instantiate the Flask app, set configuration values.
app = flask.Flask(__name__)
app.config.from_mapping({
    # Set values for the Flask-Caching module.
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "C:\Program Files\GoogleSchoolTools\cache",
    "CACHE_DEFAULT_TIMEOUT": 1800
})
# Instantiate the session cache object.
sessionTokenCache = flask_caching.Cache(app)



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

# Generate and cache a session token for a validated user, returning the session token.
def generateSessionToken(userData):
    sessionToken = str(uuid.uuid4())
    sessionTokenCache.set(sessionToken, userData)
    return(sessionToken)

@app.route("/", methods=['GET'])
def photoUpload():
    return "User interface goes here."

@app.route("/api/mystartLogin", methods=['GET', 'POST'])
def mystartLogin():
    if flask.request.method == 'POST':
        loginToken = flask.request.form.get("loginToken")
        loginTokenValidationRequest = requests.get("https://dev.mystart.online/api/validateToken?loginToken=" + loginToken + "&pageName=" + "0000000000000002")
        if loginTokenValidationRequest.status_code == 200:
            loginResult = json.loads(loginTokenValidationRequest.json())
            # '{"login":"valid","emailHash":"' + hashEmailAddress(emailAddress, salt) + '","emailDomain":"' + emailAddress.split("@")[1] + '","loginType":"' + loginType + '"}'
            print(loginResult)
            sessionToken = generateSessionToken({"userID":"userIDGoesHere"})
            return "This should be an HTML page with replaced session token: " + sessionToken
        else:
            return "Login error."
    else:
        return "Was a GET."

        #userData = sessionTokenCache.get(loginToken)
        #if userData:
            #userData["login"] = "valid"
            #return userData


    # /home/dhicks6345789/gamadv-xtd3/gam select knightsbridgeschool info domain

if __name__ == "__main__":
    app.run()
