from flask import Flask, render_template, json, request, redirect
from flaskext.mysql import MySQL
from base import base_page

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

    # validate the received values
    if _firstname and _lastname and _username and _username and _email and _password:
      # all fields are filled
      conn = mysql.connect()

      cursor = conn.cursor()
      cursor.callproc('sp_createUser', (_firstname, _lastname, _username, _email, _password))

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
    kwargs['message'] = "Error %s: %s" % e[0], e[1]
    kwargs['messageType'] = "danger"
    return render_template('/signup.html', **kwargs)

  cursor.close()
  conn.close()
  return redirect('/search')

@app.route('/updateinfo', methods=['POST'])
def updateinfo():
  val_status = False
  try:
    # read the posted values from the UI
    _email = request.form['input_email']
    _password = request.form['input_password']

    # validate the received values
    if  _email and _password:
      # all fields are filled
      try:
        conn = mysql.connect()
      except Exception as e:
        return json.dumps({'debugging':str(e)})

      cursor = conn.cursor()
      query_string="UPDATE users SET email= '" +_email +"', password= '" + _password +"' WHERE username='SampleUser'"
      cursor.execute(query_string)

      data = cursor.fetchall()

      if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
      else:
        return json.dumps({'error':'err'})

    else:
      return json.dumps({'html':'<span>Enter the required fields</span>'})

  except Exception as e:
    print e
    return json.dumps({'error': 'exception thrown' })

  cursor.close()
  conn.close()


@app.route('/search', methods=['POST'])
def search():
  val_status = False
  print("We're in here")
  try:
    _search = request.form['search']
    _year=request.form['year']
    # validate the received values
    if _search and _year:
      # all fields are filled
      try:
        conn = mysql.connect()
      except Exception as e:
        return json.dumps({'debugging':str(e)})

      cursor = conn.cursor()
      query_string="SELECT l.name FROM laws l, publications p  WHERE l.pub_id=p.pub_id and l.name like '%" + _search + "%' and EXTRACT(YEAR FROM p.pub_date) ="+_year+""
      cursor.execute(query_string)

      data = cursor.fetchall()

  except Exception as e:
    print e
    return json.dumps({'error': 'exception thrown' })

  cursor.close()
  conn.close()
  return str(data)

if __name__=="__main__":
  app.run(port=5009, host='0.0.0.0')
