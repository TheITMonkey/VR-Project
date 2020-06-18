#!usr/bin/python
from flask import Flask, request, render_template, redirect, jsonify
import authentication


app = Flask(__name__)
linkMailApp = "http://mailService:5001"

@app.route('/')
def index():
   return redirect(linkMailApp)

"""
    Rota para verificação dos tokens
"""
@app.route('/sendMail',methods=['POST'])
def mail_sender():
    token = request.form.get('token')
    name = request.form.get('name')
    if token:
        #verificar request token
        if authentication.validToken(token, name):
            #redirect para pagina de email:
                return jsonify({'res':'OK'}), 200
        else:
            #redirect para index
            return jsonify({'res':'Bad Token'}), 400
    else:
        return jsonify({'res':'Bad Request'}), 401

"""
    Rota para login
    
    O redirect da mail_app pede a esta rota para realizar o login, criando o token associado ao utilizador.
    Verifica se password é correspondente, e se o utilizador existe
"""
@app.route('/login',methods=['POST'])
def login():
    name = request.form.get('nickname')
    password = request.form.get('password')
    
    if not name or not password:
        return redirect(linkMailApp, code=400)

    if not authentication.getUser(name):
        return jsonify({"res":"NO USER"}), 404
    
    if not authentication.verifyPass(name,password): #retorna true caso seja igual
        return jsonify({"res":"wrong password"}), 400
    token = authentication.createToken(name,password)

    data = {'token':token }
    #return do token para o mail_app, verificar return
    return jsonify(data), 200

@app.route('/register',methods=['POST'])
def register():
    #verificar existencia dos campos
    name = request.form.get('nickname')
    password = request.form.get('password')
    email = request.form.get('email')

    #encriptar password?
    result = authentication.register(name,password, email)

    if result == "ok":
        print("Registo funcionou")
        return jsonify({"res":"OK"}), 200
    elif result is not None:
        if result['error'] == "Existing-User":
            return jsonify({"res":"EXISTING USER"}), 400
        elif result['error'] == "Server-Error":
            return jsonify({"res":"SERVER ERROR"}), 500
    else:
        return jsonify({"res":"INTERNAL SERVER ERROR"}),  500

@app.route('/logout', methods=['POST'])
def logout():
    name = request.form.get('name')
    token = request.form.get('token')
    
    #verificar se o gajo que pediu para apagar o token tem o token
    if authentication.validToken(token,name):
        #apagar o token
        if authentication.deleteToken(name):
            return jsonify({"res":"Token deleted"}), 200
        else:
            return jsonify({"res":"Could not delete token"}), 400
    else:
        return jsonify({"res":"Bad token"}), 401
    
        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
