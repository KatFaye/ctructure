from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
 

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'm90753'
app.config['MYSQL_DATABASE_DB'] = 'ctructure'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
  return render_template('index.html')

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
      conn = mysql.connect()
      cursor = conn.cursor()
      val_status = True
      cursor.callproc('sp_createUser', (_firstname, _lastname, _username, _email, _password))
      data = cursor.fetchall()

      if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
      else:
        return json.dumps({'error':str(data[0])})

    else:
      return json.dumps({'html':'<span>Enter the required fields</span>'})
  
  except Exception as e:
    return json.dumps({'error':str(e)})
    
  cursor.close()
  conn.close()

if __name__=="__main__":
  app.run()
