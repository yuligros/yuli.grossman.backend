from flask import Flask, redirect, url_for,render_template
from flask import request, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = '123'
app.permanent_session_lifetime = 30

# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(
                         host="localhost",
                         user="root",
                         password="Y$11Gros"
    )
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value
# ------------------------------------------------- #
# ------------------------------------------------- #

@app.route('/users')
def func_users():
    query = "select * from users.user"
    query_reasult = interact_db(query, 'fetch')
    return render_template('users.html', users = query_reasult)

# @app.route('/delete_user')
# def func_delete_user():
#     return render_template('users.html')

# Home page
@app.route('/yuli')
@app.route('/')
def main_func():  # put application's code here
    # TODO
    return redirect(url_for('home_func'))

@app.route('/Home')
def home_func():
    session['user_name'] = 'Stranger'
    return render_template('welcome.html')

# About me page
@app.route('/About_me')
def about_func():
    return render_template('cv.html')


# Hobbies page
@app.route('/hobbies')
def hobbies_func():
    return render_template('assignment8.html',
                           hobbies = ['Basketball','Snowboard','Running','Reformer pilates','hiking','cooking','Free - diving'])

# Contact page
@app.route('/contact')
def contact_func():
    if 'y_name' in request.args:
          name = request.args['y_name']
          email = request.args['y_email']
          password = request.args['y_password']
          return render_template('contact.html', user_name = name,user_email = email,user_password = password)
    return render_template('contact.html')

# Contact page
@app.route('/Search',methods = ['GET','POST'])
def search_func():
    user_name,second_name = '',''
    users = get_users()
    if_exist = False

    if request.method == 'POST':
          user_name = request.form['y_name']
          user_email= request.form['y_email']
          user_password = request.form['y_password']
          id = request.form['y_id']
          date_time = date.today()
          session['user_name'] = user_name
          session['logged_in'] = True
          query = '''INSERT INTO `users`.`user` (`id`, `user_name`, `email`, `password`, `date`) VALUES('%s','%s', '%s','%s','%s');'''%(id,user_name, user_email,user_password,date_time)
          interact_db(query,'commit')
          return render_template('welcome.html')

    if request.method == 'GET':
        query = "select * from users.user"
        query_reasult = interact_db(query, 'fetch')
        if 'y_id' in request.args:
           id = request.args['y_id']
           user_name = request.args['y_name']
           query_2 = "select COUNT(*) as exist from users.user WHERE users.user.id = ('%s');"%id
           query_reasult_2 = interact_db(query_2, 'fetch')
           for q in query_reasult_2:
              if q.exist == 1:
                session['user_name'] = user_name
                session['logged_in'] = True
                return render_template('welcome.html')
           return render_template('users.html', users=query_reasult)

    return render_template('assignment9.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    session['logged_in'] = False
    return redirect(url_for('home_func'))


def get_users():
    users = {'user1': {'user_name': 'yuli', 'email' : 'yuli11@gmail.com'},
             'user2': {'user_name': 'yosik', 'email': 'yosik12@gmail.com'},
             'user3': {'user_name': 'erez', 'email': 'erezMaster@gmail.com'},
             'user4': {'user_name': 'amit', 'email': 'tuli@gmail.com'},
             'user5': {'user_name': 'guy', 'email': 'guyTheKing@gmail.com'},
             'user6': {'user_name': 'shahaf', 'email': 'shahafgros@gmail.com'},
             'user7': {'user_name': 'dor', 'email': 'dori100@gmail.com'},
             'user8': {'user_name': 'itamar', 'email': 'itamari@gmail.com'}}
    return users


# def check_if_user_exist(id,users):
#     for for user in users:
#             if user.id == id:
#                 return True;
#     return False


if __name__ == '__main__':
    app.run(debug=True)








