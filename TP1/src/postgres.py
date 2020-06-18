#!/usr/bin/python
import psycopg2, datetime
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return conn

"""
    Testar
"""
def existsUser(name):
    conn = connect()
    
    try:
        curr = conn.cursor()
        sql = """
            SELECT * 
            FROM "user"
            WHERE "user"."name" = '%s' """ % (name)
        curr.execute(sql)
        print(curr.fetchone())
        if curr.rowcount == 0:
            return False
        else:
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    


"""
    Testar
"""
def verify_token(name,token):
    conn = connect()
    try:
        curr = conn.cursor()
        sql = """
            SELECT *
            FROM "user"
            INNER JOIN "token" ON "token"."tokenID" = "user"."tokenID"
            WHERE "token"."desc" = '%s' AND
            "user"."name" = '%s' """ % (token,name)

        curr.execute(sql)
        if curr.rowcount == 0:
            return False
        else:
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        curr.close()
        if conn is not None:
            conn.close()

"""
    Se o utilizador tiver algum token, destroi
"""
def deleteToken(name):
    conn = connect()
    try:
        curr = conn.cursor()
        sql = """
            SELECT "token"."tokenID"
            FROM "user" u
            INNER JOIN "token" ON "token"."tokenID" = u."tokenID"
            WHERE u.name = '%s' """ % (name)

        curr.execute(sql)
        
        if curr.rowcount == 0:
            return
        #ir buscar o id do token
        row  = curr.fetchone()
        tokenID = row[0]        
        
        #sql para retirar o tokenID do user
        sql = """
                UPDATE "user"
                SET "tokenID" = NULL
                WHERE "user"."name" = '%s'
            """ % (name)
        curr.execute(sql)

        #sql para apagar o token
        sql = """
            DELETE FROM "token"
            WHERE "token"."tokenID" = %s """ % (tokenID)
    
        curr.execute(sql)
        conn.commit()
        curr.close()
        
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        conn.close()

"""
    Guarda o token passado

"""
def saveToken(name, token):
    conn = connect()
    #Tempo de expiração do token
    expiration = 50000
    print("TOKEN:",token)
    try:
        curr = conn.cursor()
        sql = """
            INSERT INTO "token" ("expires", "created", "desc")
            VALUES (%s,'%s','%s') RETURNING "tokenID"
        """ % (expiration, datetime.datetime.now().isoformat(),token)
        curr.execute(sql)
        tokenID = curr.fetchone()[0]
        print("tokenID:",tokenID)
        
        #update do tokenID do utilizador
        sql = """
            UPDATE "user"
            SET "tokenID" = %s
            WHERE "name" = '%s'
        """  % (tokenID,name)
        curr.execute(sql)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
"""
    Registar novo utilizador

    TODO: Alterar o return disto
"""
def register(name,password,email):
    conn = connect()
    try:
        curr = conn.cursor()
        sql = """INSERT INTO "user" ("name", "password","email")
            VALUES ('%s','%s', '%s') RETURNING name
        """ % (name, password, email)
        
        curr.execute(sql)
        conn.commit()
        return "ok"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

"""
    Obtem a password de um dado user, para verificar.
"""
def getPassword(name):
    conn = connect()
    try:
        curr = conn.cursor()
        sql = """
            SELECT password
            FROM "user"
            WHERE name = '%s'
        """ % (name)
        curr.execute(sql)
        return curr.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
