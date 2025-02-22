#必要なライブラリをインポート

from flask import Flask, render_template, request, redirect,url_for, flash, session 
#アプリケーション開発に必要なモジュールをインストール
from datetime import timedelta  #日時を扱うモジュール
import re #reモジュール 
from flask_socketio import SocketIO,  emit  #socket通信を管理
from  flask_login import  LoginManager,login_user,logout_user,login_required,current_user
#ログイン情報などを管理
from werkzeug.security import generate_password_hash, check_password_hash
#パスワードを安全に扱う為の関数

from flask_mysqldb import MySQL

from werkzeug.security import check_password_hash
from models import User, Main_category, Sub_category, Message


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
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] ='your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] ='your_database'


mysql = MySQL(app)
socketio = SocketIO(app)



@app.route("/",methods=["GET"])
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
        
    
    
    if not check_password_hash(user["password"], password):
        flash('パスワードが間違っています！')
        return redirect(url_for('login_view'))

    #セッションの設定
    session['uid'] = user["id"]
    return redirect(url_for('main_category_view'))


#ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

@socketio.on('chat_message')
def handle_message(data):
    username = data.get('username', 'Anonymous')  # ユーザー名がない場合は 'Anonymous'
    message = data.get('message', '')
    
    # メッセージの保存（オプション）
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages (username, content) VALUES (%s, %s)", (username, message))
    mysql.connection.commit()
    
    emit('chat_message', {'username': username, 'message': message}, broadcast=True)

#チャットルームの作成
@app.route('/create_room', methods=['POST'])
@login_required
def create_room():
    name = request.form.get('name')
    category_id = request.form.get('category_id')

    if not name or not category_id:
        flash('ルーム名とカテゴリを入力してください')
        return redirect(url_for('room_list'))

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO chat_rooms (name, category_id) VALUES (%s, %s)", (name, category_id))
    mysql.connection.commit()

    flash('チャットルームが作成されました')
    return redirect(url_for('room_list'))

#チャットルームの編集
@app.route('/update_room/<int:room_id>', methods=['POST'])
@login_required
def update_room(room_id):
    new_name = request.form.get('new_name')
    new_description = request.form.get('new_description')
    new_category_id = request.form.get('new_category_id')

    if not new_name:
        flash('新しいルーム名を入力してください')
        return redirect(url_for('room_list'))

    cursor = mysql.connection.cursor()
    
    # 更新対象のカラムを選択的に変更
    if new_description and new_category_id:
        cursor.execute("UPDATE chat_rooms SET name = %s, description = %s, category_id = %s WHERE id = %s",
                       (new_name, new_description, new_category_id, room_id))
    elif new_description:
        cursor.execute("UPDATE chat_rooms SET name = %s, description = %s WHERE id = %s",
                       (new_name, new_description, room_id))
    elif new_category_id:
        cursor.execute("UPDATE chat_rooms SET name = %s, category_id = %s WHERE id = %s",
                       (new_name, new_category_id, room_id))
    else:
        cursor.execute("UPDATE chat_rooms SET name = %s WHERE id = %s",
                       (new_name, room_id))

    mysql.connection.commit()
    flash('チャットルームが更新されました')
    return redirect(url_for('room_list'))

#メッセージの送信
@socketio.on('send_message')
def send_message(data):
    username = current_user.username  # ログインユーザーの名前
    message = data['message']
    room_id = data['room_id']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages (username, room_id, content) VALUES (%s, %s, %s)", (username, room_id, message))
    mysql.connection.commit()

    emit('receive_message', {'username': username, 'message': message}, room=room_id)


#メッセージの削除
@app.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    mysql.connection.commit()

    flash('メッセージが削除されました')
    return redirect(url_for('chat_view'))

# サインアップページ表示
@app.route('/signup', methods=['GET'])
def signup_view():	
    return render_template('auth/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password-confirmation')
    
    if name == '' or email == '' or password == '' or password_confirmation == '':
        flash('未入力の項目があります。')
    
    if password != password_confirmation:
        flash('パスワードが一致しません。')

    if re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスが正しい形式で入力されていません。')

    password = generate_password_hash(password)
    registered_user = User.find_by_email(email)
    if registered_user != None:
        flash('既に登録済みです。ログインページからログインして下さい。')
    else:
        User.create(name, email, password)
        user_info = User.find_by_email(email)
        session['uid'] = str(user_info["id"])
        return redirect(url_for('main_category_view')) 
    return redirect(url_for('login_view'))

@app.route('/channels', methods=['GET'])
def main_category_view():
    main_categories = Main_category.get_all()
    return render_template('home.html', main_categories=main_categories)

# サブカテゴリページ表示
@app.route('/channels/<cid>', methods=['GET'])
def sub_category_view(cid):
    sub_categories = Sub_category.find_by_main_category_id(cid)
    return render_template('channels.html', sub_categories=sub_categories, main_category_id=cid)

# サブカテゴリ追加
@app.route('/channels/update/<cid>', methods=['POST'])
def create_sub_category_view(cid):
    uid = session.get('uid')
    sub_category_name = request.form.get('sub_category_name')
    sub_category_description = request.form.get('sub_category_description')

    Sub_category.create(uid, sub_category_name, sub_category_description, cid)

    return redirect(url_for('sub_category_view', cid=cid))

# サブカテゴリ名前、説明の更新
@app.route('/channels/update_channel/<scid>', methods=['POST'])
def update_sub_category_view(scid):
    sub_category_name = request.form.get('sub_category_name')
    sub_category_description = request.form.get('sub_category_description')
    
    Sub_category.update(scid, sub_category_name, sub_category_description)
    
    sub_category = Sub_category.find_by_sub_category_id(scid)
    main_category_id = sub_category["main_category_id"]

    return redirect(url_for('chatroom_view', cid=main_category_id, scid=scid))


# チャット画面表示
@app.route('/channels/<cid>/<scid>', methods=['GET'])
def chatroom_view(cid, scid):
    uid = session.get('uid')
    messages = Message.find_by_sub_category_id(scid)
    sub_category = Sub_category.find_by_sub_category_id(scid)
    return render_template('messages.html', uid=uid, messages=messages, sub_categories=sub_category)

# メッセージを送信
@app.route('/channels/<cid>/<scid>', methods=['POST'])
def send_message(cid, scid): 
    uid = session.get('uid')
    user_info = User.find_by_uid(uid)
    username = user_info["username"]
    sub_category_id = request.form.get('sub_category')
    message = request.form.get('message')
    Message.create(uid, username, sub_category_id, message)

    return redirect(url_for('chatroom_view', cid=cid, scid=scid))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500


if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",debug=True,allow_unsafe_werkzeug=True)

