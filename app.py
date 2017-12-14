from flask import Flask, render_template, json, request, redirect, flash, session, abort, url_for
from flaskext.mysql import MySQL
from base import base_page
from os import urandom
import re,json
from scripts.advanced_search import get_results

app = Flask(__name__)
app.register_blueprint(base_page)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'kherring'
app.config['MYSQL_DATABASE_PASSWORD'] = '12faye'
app.config['MYSQL_DATABASE_DB'] = 'rwandanlaw'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.route('/login')
def check_login():
    if session.get('logged_in'):
        return redirect('/updateinfo')
    else:
        kwargs = {}
        kwargs['message'] = ""
        kwargs['messageType'] = ""
        return render_template('/login.html', **kwargs)


@app.route('/login', methods=['POST'])
def do_admin_login():
    kwargs = {}
    if session.get('logged_in') == True:
        kwargs['message'] = "You're logged in already!"
        kwargs['messageType'] = "warning"
    try:
        user = request.form['username']
        password = request.form['password']

        conn = mysql.connect()

        cursor = conn.cursor()

        query = """
            SELECT username, password from users u WHERE
            u.username = %s and u.password = %s;
        """

        isValid = cursor.execute(query, (user, password))
        if isValid > 0:  # not an empty SET
            session['logged_in'] = True
            session['user'] = user
            kwargs['message'] = "%s Logged In Successfully!" % user
            kwargs['messageType'] = "success"
        else:
            kwargs['message'] = "Error: Invalid user or password!"
            kwargs['messageType'] = "danger"
        cursor.close()
        conn.close()
        return render_template('login.html', **kwargs)
    except Exception as e:
        print("The Error is " + str(e))
        kwargs['message'] = "Error %s: %s" % (e[0], e[1])
        kwargs['messageType'] = "danger"
        return render_template('/login.html', **kwargs)


@app.route('/signup', methods=['POST'])
def signup():
    kwargs = {}
    val_status = False
    try:
        # read the posted values from the UI
        _firstname = request.form['input_firstname']
        _lastname = request.form['input_lastname']
        _username = request.form['input_username']
        _email = request.form['input_email']
        _password = request.form['input_password']

        # all fields are filled
        conn = mysql.connect()

        cursor = conn.cursor()
        cursor.callproc('sp_createUser', (_firstname,
                                          _lastname, _username, _email, _password))

        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            kwargs['message'] = "User Created Successfully!"
            kwargs['messageType'] = "success"
            return render_template('/signup.html', **kwargs)
        else:
            kwargs['message'] = "Error: Unknown Error"
            kwargs['messageType'] = "danger"
            return render_template('/signup.html', **kwargs)

    except Exception as e:
        kwargs['message'] = "Error %s: %s" % (e[0], e[1])
        kwargs['messageType'] = "danger"
        return render_template('/signup.html', **kwargs)

    cursor.close()
    conn.close()
    return redirect('/index')


@app.route('/updateinfo', methods=['POST'])
def updateinfo():
    kwargs = {}
    val_status = False
    try:
        # read the posted values from the UI
        _email = request.form['input_email']
        _password = request.form['input_password']

        conn = mysql.connect()

        cursor = conn.cursor()
        user = session.get('user')
        query_string = "UPDATE users SET email= '" + _email + \
            "', password= '" + _password + "' WHERE username='" + user + "'"
        cursor.execute(query_string)

        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            kwargs['message'] = "User Updated Successfully!"
            kwargs['messageType'] = "success"
            return render_template('/updateinfo.html', **kwargs)
        else:
            kwargs['message'] = "Error: Unknown Error"
            kwargs['messageType'] = "danger"
            return render_template('/updateinfo.html', **kwargs)

    except Exception as e:
        kwargs['message'] = "Error %s: %s" % (e[0], e[1])
        kwargs['messageType'] = "danger"
        return render_template('updateinfo.html', **kwargs)

    cursor.close()
    conn.close()


@app.route('/query', methods=['POST'])
def query():
    kwargs = {}
    try:
        query_input = request.json
        query_input = json.load(query_input)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        print(query_input)

        _search = query_input['search']
        _year = int(query_input['year'])
        _content_type = query_input['content_type']
        _agency = query_input['agency']

        if (_year == "None"):
            _year = False
        if (_content_type == "None"):
            _content_type = False
        if (_agency == "None"):
            _agency = False

        conn = mysql.connect()
        cursor = conn.cursor()

        query_results = get_results(_agency, _content_type, _year, _search)
        print(query_results)
        law_names = []
        for res in query_results:
        	law_names.append(res["law_name"])
        

        #query_string="SELECT l.name FROM laws l, publications p  WHERE l.pub_id=p.pub_id and l.name like '%" + _search + "%' and EXTRACT(YEAR FROM p.pub_date) ="+_year+""
        #query_string="SELECT l.name FROM laws l  WHERE  l.name like '%" + _search + "%'"
        # cursor.execute(query_string)

        #kwargs['data'] = cursor.fetchall()
        #kwargs['message'] = law_names
        #kwargs['messageType'] = "success"
        return law_names

    except Exception as e:
        kwargs['message'] = "Error " + str(e)
        kwargs['messageType'] = "danger"
        print("ERROR!!!!!!!!!!!!!!")
        print(e)
        return render_template('index.html', **kwargs)

    cursor.close()
    conn.close()
    #return render_template('index.html', **kwargs)


if __name__ == "__main__":
    app.secret_key = urandom(12)
    app.run(port=5020, host='0.0.0.0')
