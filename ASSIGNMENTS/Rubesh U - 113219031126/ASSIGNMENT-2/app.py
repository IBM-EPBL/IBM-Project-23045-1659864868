from flask import Flask,render_template
from flask import request

import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;SECURITY=SSL;PORT=31498;PROTOCOL=TCPIP;UID=nnm68033;PWD=DUTMGiDWgJy5zlS8",'','')

print(conn)

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/home')

def home():
    entries = []

    sql = "select * from users;"
    stmt = ibm_db.exec_immediate(conn,sql);
    dictionary = ibm_db.fetch_both(stmt);
    while(dictionary!=False):
        entries.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    print(entries)

    return render_template("home.html")

@app.route('/about')

def about():
    return render_template("about.html")

@app.route('/signin')

def signin():
    return render_template("signin.html")


@app.route("/checkcred",methods = ['POST', 'GET'])

def checkCred():
    name = request.args.get('name')
    password = request.args.get('password')
    sql = "select * from users where name=? and password=?;"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    result = []

    dictionary = ibm_db.fetch_both(stmt)

    while(dictionary!=False):
        result.append({'name':dictionary[0],'password':dictionary[1]})
        dictionary = ibm_db.fetch_both(stmt)
    
    if(len(result)==1):
        return {'message':'success'}
    else:
        return {'message': 'failure'}


@app.route('/check')

def check():

    name = request.args.get("name")
    password = request.args.get("password")
    sql = "insert into users values(?,?);"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    return {'message' : 'success'}


@app.route('/signup')

def signup():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run()
