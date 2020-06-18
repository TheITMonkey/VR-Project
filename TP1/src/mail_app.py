#!usr/bin/env python
from flask import Flask, request, send_from_directory, render_template, redirect, json, url_for, flash
import requests
import smtpEmail

app = Flask(__name__)
app.secret_key = b'mailServERAAPPPPP'
linkAuth = 'http://auth:5000'

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/sendMail',methods=['GET','POST'])
def sendMail():
    if request.method == 'GET':
        if request.args.get('token') is None:
            return redirect(url_for('index'))
        
        #verificar se o token é valido
        data={'token': request.args.get('token'), 'name': request.args.get('name')}
        print(data)
        response = requests.post(linkAuth + '/sendMail',data=data)
        if response.status_code == 200:
            return render_template('email.html', token=request.args.get('token'), name=request.args.get('name'))
        else:
            return redirect(url_for('index'))

    elif request.method == 'POST':
        #tratar de enviar email
        print("POST SEND MAIL:",request.form.to_dict())
        if request.form.get('token') is None:
            return redirect(url_for('index'))

        #verificar token
        data={'token': request.form.get('token'), 'name':request.form.get('name')}
        response = requests.post(linkAuth + '/sendMail', data=data)
        if response.status_code == 200:
            #enviar email
            smtpEmail.sendEmail(request.form.get('sender_email'),\
                                request.form.get('destination_email'),\
                                request.form.get('subject'),\
                                request.form.get('message'))
            flash("Email enviado com sucesso")
            #redirect para a pagina de email com o token e o nome
            return redirect(url_for('sendMail',token=request.form.get('token'), name=request.form.get('name')))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
                            
@app.route('/logout',methods=['POST'])
def logout():
    data = request.form.to_dict()
    response = requests.post(linkAuth + '/logout', data=data)
    
    return redirect(url_for('index'))
    

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        dic = request.form.to_dict()
        print(dic)
        #Pedido a API presente no authentication server que trata do processo de login
        response = requests.post(linkAuth + '/login', data=dic)
        if response.status_code == 200:
            res = json.loads(response.content)

            flash('Login concluido') 
            return redirect(url_for('sendMail',token=str(res['token']), name=request.form.get('nickname')))
            print("POST RESTURN")
        elif response.status_code == 404:
            error = "Wrong username"
        elif response.status_code == 400:
            error = "Wrong password"
        else:
            error = "Internal error, please contact support"

    return render_template('login.html',error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    
    if request.method == 'POST':
        dic = request.form.to_dict()
        #redirect para o registo da auth_server com as infos do registo
        response = requests.post(linkAuth + '/register',data = dic)
        if response.status_code == 200:
            flash("Registo efetuado")
            return redirect('/login')
        elif response.status_code == 400:
            error = "Name already taken"
        else:
            error = "Server error, please contact support"
    
    return render_template('registar.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
