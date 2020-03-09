from flask import Flask,jsonify,render_template,request,url_for,redirect
from flask_mysqldb import MySQL
import json, redis,urllib.request
from datetime import datetime
from pytz import timezone  



app = Flask(__name__)

app.config['MYSQL_HOST']='db'
#app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='myapp'
mysql= MySQL(app)
r_server= redis.Redis("redis")
def timestamp():
    cartagena = timezone('America/Bogota')
    sa_time = datetime.now(cartagena)
    return (sa_time.strftime('%D %T'))

def temperatura():
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=3687238&appid=9583c3b4fa60a5323f4d1d115a5f2592") as url:
        data = json.loads(url.read().decode())
        return(data["main"]["temp"]-273.15)
def Getjson():
    temp= temperatura()
    tie = timestamp()
    dato =  ('{ "temperatura":"%s", "timestamp":"%s"}') % (temp,tie)
    j = json.loads((dato))
    return (j)

def Guardar(temp,tie):
  cur= mysql.connection.cursor()
  r_server.rpush("timestamp",str(tie))
  r_server.rpush("temp",str(temp))
  cur.execute('CREATE TABLE IF NOT EXISTS `tiempo` (`id` INT NOT NULL AUTO_INCREMENT, `timestamp` TIMESTAMP NOT NULL,`temperatura` FLOAT NOT NULL,PRIMARY KEY (`id`))')
  cur.execute('INSERT INTO tiempo (timestamp,temperatura) VALUES (%s,%s)',(tie,temp))
  mysql.connection.commit()
  cur.close
def leerjson(j):
    temp=j["temperatura"]
    tie=j["timestamp"]
    Guardar(temp,tie)
    return (temp,tie)

@app.route('/index')

def ping():
    
    return render_template('index.html')
@app.route('/')
def home():
    temp=temperatura()
    tie=timestamp()
    return render_template('main.html',tie=tie,temp=temp)
@app.route('/guardar',methods=['POST'])
def save():
    if (request.method=='POST'):
        j=Getjson()
        leerjson(j)
        return redirect(url_for('home'))
@app.route('/=<var>')
def iot(var):
    if var=='iot':
        j=Getjson()
        leerjson(j)
        return j


if __name__ =='__main__':
    app.run(debug=True)
