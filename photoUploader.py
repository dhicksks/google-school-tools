def app():
    return replaceKeywords(getFile("photoUploader/index.html"), {"HEADER":getFile("header.html"),"SESSIONTOKEN":""})
