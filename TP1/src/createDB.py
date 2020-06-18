import psycopg2
from config import config


def main():
    conn = None

    commands_create = (
        """
        CREATE TABLE "user" (
        "name" varchar(50) NOT NULL,
        "password" varchar(50) NOT NULL,
        "tokenID" bigint,
        "email" varchar(50) NOT NULL,
        CONSTRAINT User_pk PRIMARY KEY ("name")
    ) WITH (
        OIDS=FALSE
    );
        """,
        """
        CREATE TABLE "token" (
        "tokenID" serial NOT NULL,
        "expires" bigint NOT NULL,
        "created" TIMESTAMP NOT NULL,
        "desc" varchar(255) NOT NULL,
        CONSTRAINT Token_pk PRIMARY KEY ("tokenID")
    ) WITH (
        OIDS=FALSE
    );
        """,
        """ALTER TABLE "user" ADD CONSTRAINT "user_fk0" FOREIGN KEY ("tokenID") REFERENCES "token"("tokenID");""",
    )
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        #Executar cada comando de criação
        for command in commands_create:
            cur.execute(command)

        cur.close()
        conn.commit()
        print("Bd created")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Connection a BD fechada')



if __name__== '__main__':
    main()
