# Standard Python libraries.
import os
import uuid

# The Flask library, a lightweight web application framework.
import flask

# Flask-Caching, used to store session tokens.
import flask_caching

# The Requests library, for handling HTTP(S) calls.
import requests

# The MyStart.Online page ID to use.
mystartLoginPage = "0000000000000002"



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

# Given a string, replaces all instances of each given keyword (enclosed in brackets, e.g. {{SOMETHING}}) with the matching value.
def replaceKeywords(theText, theKeywords):
    result = theText
    for keyword in theKeywords.keys():
        result = result.replace("{{"+keyword+"}}", theKeywords[keyword])
    return result

@app.route("/", methods=['GET', 'POST'])
def mystartLogin():
    if flask.request.method == 'POST':
        loginToken = flask.request.form.get("loginToken")
        loginTokenValidationRequest = requests.get("https://dev.mystart.online/api/validateToken?loginToken=" + loginToken + "&pageName=" + mystartLoginPage)
        if loginTokenValidationRequest.status_code == 200:
            # The user data supplied from MyStart.Online should be a JSON string reading: "login":"valid","emailHash", "emailDomain", "loginType".
            # We cache that with a newly-generated session key and return an HTML page to the user.
            return replaceKeywords(getFile("tools.html"), {"HEADER":getFile("header.html"),"SESSIONTOKEN":generateSessionToken(loginTokenValidationRequest.json())})
        else:
            # Return the error message page to the user.
            return replaceKeywords(getFile("error.html"), {"HEADER":getFile("header.html"),"ERRORMESSAGE":"Invalid login - MyStart.Online returned non-200 status code."})
    else:
        # Return the non-logged-in HTML page to the user.
        return replaceKeywords(getFile("tools.html"), {"HEADER":getFile("header.html"),"SESSIONTOKEN":""})

# /home/dhicks6345789/gamadv-xtd3/gam select knightsbridgeschool info domain
if __name__ == "__main__":
    for item in os.listdir("."):
        print(item)
    app.run()
