from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'kherring'
app.config['MYSQL_DATABASE_PASSWORD'] = '12faye'
app.config['MYSQL_DATABASE_DB'] = 'rwandanlaw'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.route("/")
def main():
  return render_template('index.html')

# Insert: User Sign up
@app.route('/showSignUp')
def showSignUp():
  return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
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
      try:
        conn = mysql.connect()
      except Exception as e:
        return json.dumps({'debugging':str(e)})

      cursor = conn.cursor()
      cursor.callproc('sp_createUser', (_firstname, _lastname, _username, _email, _password))

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

# Update: change user info 
@app.route('/changeInfo')
def showChangeInfo():
  return render_template('changeInfo.html')

@app.route('/changeInfo', methods=['POST'])
def updateUserInfo():
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
      cursor.callproc('sp_updateUserInfo',(_email, _password))

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


# Query: query for law
@app.route('/search')
def showSearch():
  return render_template('query.html')

@app.route('/search', methods=['GET'])
def getLaws():
  val_status = False
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
      query_string="SELECT name FROM laws l, publications p inner join l.pub_id=p.pub_id WHERE name like '" + _search + "' and year(p.pub_date) ='"+_year+"'"
      cursor.execute(query_string)
      cursor.callproc('sp_selectFunction',(_search,_name))

      data = cursor.fetchall()

  except Exception as e:
    print e
    return json.dumps({'error': 'exception thrown' })
    
  cursor.close()
  conn.close()
  return str(data)


if __name__=="__main__":
  app.run(port=5009, host='0.0.0.0')
