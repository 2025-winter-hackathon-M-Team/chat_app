from flask import abort
import pymysql

from util.DB import DB

db_pool = DB.init_db_pool()

class User:
    @classmethod
    def create(cls, username, email, password):
        conn = db_pool.get_conn()
        # DB登録に失敗した時、rollbackをさせるようにする？
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users(username, email, password) VALUES(%s, %s, %s);"
                cur.execute(sql, (username, email, password,))
                conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しました。: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
                return user # ユーザーが存在しない場合、空ではなくNoneが入る？
        except pymysql.Error as e:
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)

class Main_category:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM main_categories;"
                cur.execute(sql)
                main_categories = cur.fetchall()
                return main_categories
        except pymysql.Error as e:
            print(f'エラーが発生しました。:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Sub_category:
    @classmethod
    def create(cls, uid, sub_category_name, sub_category_description, main_category_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO sub_categories(uid, sub_category_name, sub_category_description, main_category_id) VALUES(%s, %s, %s, %s);"
                cur.execute(sql, (uid, sub_category_name, sub_category_description, main_category_id,))
                conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しました。:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_main_category_id(cls, main_category_id):
        conn = db_pool.get_conn()

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM sub_categories WHERE main_category_id=%s;"
                cur.execute(sql, (main_category_id,))
                user = cur.fetchall()
                return user # ユーザーが存在しない場合、空ではなくNoneが入る？
        except pymysql.Error as e:
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, sub_category_id, sub_category_name, sub_category_description):
        conn = db_pool.get_conn()
        # uidが作成者出ないと、変更できない処理はapp.pyとmodels.pyのどちらに実装するか？
        try:
            with conn.cursor() as cur:
                sql = "UPDATE sub_categories SET sub_category_name=%s, sub_category_description=%s WHERE id=%s;"
                cur.execute(sql, (sub_category_name, sub_category_description, sub_category_id,))
                conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, sub_category_id):
        conn = db_pool.get_conn()
        # uidが作成者出ないと、変更できない処理はapp.pyとmodels.pyのどちらに実装するか？
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM sub_categories WHERE id=%s;"
                cur.execute(sql, (sub_category_id,))
                conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_sub_category_id(cls, sub_category_id):
        conn = db_pool.get_conn()

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM sub_categories WHERE id=%s;"
                cur.execute(sql, (sub_category_id,))
                sub_category = cur.fetchone()
                return sub_category
        except pymysql.Error as e:
            print(f'エラーが発生しました。: {e}')
            abort(500)
        finally:
            db_pool.release(conn)


class Message:
    @classmethod
    def create(cls, uid, username, sub_category_id, message):
        conn = db_pool.get_conn()
        # uidなどはapp.py側で取得できる？
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(uid, username, sub_category_id, message) VALUES(%s, %s, %s, %s);"
                cur.execute(sql, (uid, username, sub_category_id, message,))
                conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_sub_category_id(cls, sub_category_id):
        conn = db_pool.get_conn()

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM messages WHERE sub_category_id=%s;"
                cur.execute(sql, (sub_category_id,))
                messages = cur.fetchall()
                return  messages # ユーザーが存在しない場合、空ではなくNoneが入る？
        except pymysql.Error as e:
            print(f'エラーが発生しました。: {e}')
            abort(500) # 500でいい？これだけじゃなくて全部
        finally:
            db_pool.release(conn)
