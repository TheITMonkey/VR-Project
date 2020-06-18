import hashlib, datetime
import postgres as db

def validToken(token,name):
    if db.existsUser(name):
        print("USER EXISTS")
        if db.verify_token(name,token):
            print("VALID TOKEN")
            return True
        else:
            print("INVALID TOKEN")
    else:
        print("USER DOES NOT EXIST")
    return False


def getUser(name):
    return db.existsUser(name)

def deleteToken(name):
    print("Deleting token")
    return db.deleteToken(name)
        

def createToken(name,password):

    db.deleteToken(name)
    
    #criar token apartir do name e da password
    inputT = name + ":" + password + ":" + str(datetime.datetime.now())
    token = hashlib.sha256(inputT.encode()).hexdigest()
    db.saveToken(name,token)
    
    return token

def register(name,password, email):
    result =  {} 
    if not db.existsUser(name):
        result = db.register(name, password, email)
    else:
        result['error'] = "Existing-User"
    return result

    

def verifyPass(name,password):
    print("PASS:",db.getPassword(name), password)
    return db.getPassword(name) == password

