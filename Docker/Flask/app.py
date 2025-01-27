#必要なライブラリをインポート

from flask import Flask, render_template, request, redirect,url_for, flash, session, about
#アプリケーション開発に必要なモジュールをインストール

from datetime import timedelta  #日時を扱うモジュール

import hashlib  #ハッシュ関数のモジュール
import uuid #uuidを生成・操作するモジュール
import re #reモジュール 
import os #osモジュール

from flask_socketio import SocketIO,  emit  #soket通信を管理

from models import User,channel,Message

from  flask_login import  LoginManager,login_user,logout_user,login_required,current_user
#ログイン情報などを管理

from werkzeug.security import generate_password_hash, check_password_hash
#パスワードを安全に扱う為の関数

from flask_mysqldb import MYSQL


EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#メールアドレスの形式を検証する

session_days=30
#有効期限30日

app = Flask(__name__) #Flaskアプリケーションのインスタンスを作成
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=session_days)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400
#静的ファイルに対するキャッシュ有効期限：31日(2678400秒）


#MYSQLの設定
app.config[''MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] ='your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] ='your_database'


mysql = MYSQL(app)
socktio = SocketIO(app)

@app.rote("/",methods=["GET"])
def jump():
    return redirect("/login") 



#ログインページの表示
@app.route("/login",methods=["GET"])
def login_view():
    return render_template('auth/login.html')

#ログイン処理
@app.route('/login',methods=["POST"])
def login_process():
    email = request.form.get('email')
    password = request.form.get("password")

    #メールアドレスの形式を検証
    if not re.match(EMAIL_PATTERN,email):
        flash("無効なメールアドレスの形式です")
        return redirect(url_for('login_view'))
    
    if email =='' or password == '':
        flash('メールアドレスを入力してください')
        return redirect(url_for('login_view'))  
    
    user = User.find_by_email(email)
    if user is None:
            flash('ユーザーが存在しません')
            return redirect(url_for('login_view')) 
        
    #パスワードのハッシュ化
    from werkzeug.security import check_password_hash
    
    if hashPassword != user["password"]:
        flash('パスワードが間違っています！')
        return redirect(url_for('login_view')) 
                
    #セッションの設定
    session['uid'] = user["uid"]
    return redirect(url_for('channels_view'))


#ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

@socketio.on('message')
def handle_message(msg):
    emit('message',msg,broadcast=True)
    