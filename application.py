from flask import Flask, render_template, json, request, redirect, flash, session, abort, url_for
from flaskext.mysql import MySQL
from base import base_page
from os import urandom
import re
import json
import unicodedata
from datetime import date
from scripts.advanced_search import get_results

application = Flask(__name__)
application.register_blueprint(base_page)

mysql = MySQL()

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'amucunguzi'
application.config['MYSQL_DATABASE_PASSWORD'] = 'mysqlpass'
application.config['MYSQL_DATABASE_DB'] = 'rwandanlaw'
application.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
application.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(application)


@application.route('/login')
def check_login():
    if session.get('logged_in'):
        return redirect('/updateinfo')
    else:
        kwargs = {}
        kwargs['message'] = ""
        kwargs['messageType'] = ""
        return render_template('/login.html', **kwargs)


@application.route('/login', methods=['POST'])
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
        return render_template('index.html', **kwargs)
    except Exception as e:
        print("The Error is " + str(e))
        kwargs['message'] = "Error %s: %s" % (e[0], e[1])
        kwargs['messageType'] = "danger"
        return render_template('/login.html', **kwargs)


@application.route('/signup', methods=['POST'])
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
            return render_template('/login.html', **kwargs)
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


@application.route('/updateinfo', methods=['POST'])
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


@application.route('/query', methods=['POST'])
def query():
    kwargs = {}
    try:
        query_input = request.get_json(force=True)
        new_input = {}

        for k in query_input:
            b = k.encode('ascii', 'ignore')

            new_input[b] = query_input[k].encode('ascii', 'ignore')

        _search = new_input['search']
        _year = new_input['year']
        _content_type = new_input['content_type']
        _agency = new_input['agency']

        if (_year == "None"):
            _year = False
        if (_content_type == "None"):
            _content_type = False
        if (_agency == "None"):
            _agency = False

        query_results = get_results(_agency, _content_type, _year, _search)
        #print(query_results)
        #print("\n\n")

        law_info = {}
        for res in query_results:
            law_info[res["law_num_date"].encode('ascii', 'ignore')] = {}
            for field in res:
                if field !="law_num_date":
                    law_info[res["law_num_date"]][field] = res[field]

        #print(law_info)

        law_info = json.dumps(law_info)
        return law_info

    except Exception as e:
        kwargs['message'] = "Error " + str(e)
        kwargs['messageType'] = "danger"
        print("ERROR: ", e)
        

    cursor.close()
    conn.close()
    # return render_template('index.html', **kwargs)


@application.route('/details', methods=['POST'])
def get_detail_page():
    kwargs = {}
    try:
        output= {}
        query_input = request.get_json(force=True)
        law_num, law_date = query_input.split("_")
        day, month, year = [int(i) for i in law_date.split('/')]
        exact_date = date(year, month, day)

        conn = mysql.connect()  
        cursor = conn.cursor()

        # Get repeals
        query_string = """
            SELECT impacted_law_num, impacted_law_date from repeals WHERE
            parent_law_num = %s and parent_law_date = %s;
        """
        cursor.execute(query_string,(law_num, exact_date))
        data = cursor.fetchall()
        
        if(len(data) == 0):
            output["repeal_law"]= ""
        else:
            cursor = conn.cursor()
            repeal_string = """
                SELECT name from laws WHERE
                law_num = %s and exact_date = %s;
            """
            cursor.execute(repeal_string,(data[0][0], data[0][1]))
            repeal_law_name = cursor.fetchall()
            if(len(repeal_law_name) == 0):
                output["repeal_law"]= ""
            else:
                output["repeal_law"]= repeal_law_name[0][0]        

        # Get reference
        query_string = """
            SELECT cited_law_num, cited_law_date from cites WHERE
            parent_law_num = %s and parent_law_date = %s;
        """
        cursor.execute(query_string,(law_num, exact_date))
        data = cursor.fetchall()
        
        if(len(data) == 0):
            output["cited_law"]= ""
        else:
            cursor = conn.cursor()
            repeal_string = """
                SELECT name from laws WHERE
                law_num = %s and exact_date = %s;
            """
            cursor.execute(repeal_string,(data[0][0], data[0][1]))
            cited_law = cursor.fetchall()
            if(len(cited_law) == 0):
                output["cited_law"]= ""
            else:
                output["cited_law"]= cited_law[0][0]  

        # Get articles
        query_string = """
            SELECT law_id from laws WHERE
            law_num = %s and exact_date = %s;
        """
        cursor.execute(query_string,(law_num, exact_date))
        data = cursor.fetchall()
        
        if(len(data) == 0):
            output["articles"]= ""
        else:
            cursor = conn.cursor()
            repeal_string = """
                SELECT article_num,article_text,name from articles WHERE
                law_id = %s;
            """
            cursor.execute(repeal_string,(data[0][0]))
            articles = cursor.fetchall()
            if(len(articles) == 0):
                output["articles"]= ""
            else:
                #print("???????????????")
                #print(articles)
                output["articles"]= articles

        output = json.dumps(output)
        return output 
        

    except Exception as e:
        kwargs['message'] = "Error " + str(e)
        kwargs['messageType'] = "danger"
        print("ERROR:", e)
       
        return render_template('index.html', **kwargs)

    cursor.close()
    conn.close()



application.secret_key = urandom(12)
#application.run(port=5020, host='0.0.0.0')
