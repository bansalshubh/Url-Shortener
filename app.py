from flask import Flask, render_template, request,session
from mysql.connector import connect
import random
import string

from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key='FeelingHappy'

@app.route('/')
def hello():
    return render_template("demo4.html")

@app.route('/registration')
def index():
    # connection=connect(host="localhost",database="project",user="root",password="shubh@21")
    fname = request.args.get("name")
    # lname = request.args.get("secondname")
    # clgname=request.args.get("name")
    # email=request.args.get("email")
    # pwd= request.args.get("password")
    # cno=request.args.get("contact no.")
    # cur = connection.cursor()
    # query="insert into regform values('{}','{}','{}','{}','{}','{}')".format(fname,lname,clgname,email,pwd,cno)
    # query="select * from regform"
    # cur.execute(query)
    # result=cur.fetchall()
    # print(result)
    # connection.commit()
    return render_template("index.html", demo=fname)

@app.route('/<url>')
def dynamicUrl(url):
    connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
    cur=connection.cursor()
    query1="select * from urlinfo where encryptedurl='{}'".format(url)
    cur.execute(query1)
    originalurl=cur.fetchone()
    if originalurl==None:
        return render_template(("demo4.html"))
    print(originalurl[1])
    return redirect(originalurl[1])

@app.route('/urlshortener')
def urlshorten():
    url = request.args.get('link')
    custom = request.args.get('customurl')
    print(custom)
    print("planettech")
    connection=connect(host="localhost",database="pythonapp",user="root",password="shubh@21")
    cur = connection.cursor()
    encryptedurl=''
    if custom=='':
        while True:
            encryptedUrl = createEncryptedurl()
            query = "select * from urlinfo where encryptedurl='{}'".format(encryptedurl)
            cur.execute(query)
            xyz = cur.fetchone()
            if xyz == None:
                break
        print(encryptedUrl)
        query = "insert into urlinfo(original_url,encryptedurl,is_active) values('{}','{}','{}')".format(url,
                                                                                                         encryptedUrl,
                                                                                                         1)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl='sd.in/' + encryptedUrl
    else:
        query = "select * from urlinfo where encryptedurl='{}'".format(custom)
        cur.execute(query)
        xyz = cur.fetchone()
        if xyz==None:
            query = "insert into urlinfo(original_url,encryptedurl,is_active) values('{}','{}','{}')".format(url,
                                                                                                             custom,
                                                                                                             1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom
        else:
            return "url already exist"

    return render_template("demo4.html",finalencryptedurl = finalencryptedurl,url=url)

@app.route("/Signup")
def Signup():
    return render_template("signUp.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/Checklogin")
def Checklogin():
    email = request.args.get("email")
    password = int(request.args.get("pwd"))
    connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
    cur = connection.cursor()
    query = "select * from userdetails where email='{}'".format(email)
    cur.execute(query)
    xyz = cur.fetchone()
    if xyz == None:
        return "You are  not registered yet"
    else:
        if password == xyz[3]:
            session['email']=email
            session['userid']=xyz[0]
            return redirect('/home')
        return render_template("login.html", demo="Pasword is incorrect")


@app.route("/home")
def home():
    if 'email' in session:
        email=session['email']
        id=session['userid']
        print(id)
        connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
        cur = connection.cursor()
        query1 = "select * from urlinfo where created_by={}".format(id)
        cur.execute(query1)
        data = cur.fetchall()
        return render_template("updateUrl.html",data=data)
    return render_template("login.html")

@app.route("/google")
def google():
    return render_template("google.html")

@app.route("/register")
def register():
    name = request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("pwd")
    connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
    cur = connection.cursor()
    query1 = "select * from userdetails where email='{}'".format(email)
    cur.execute(query1)
    emailid = cur.fetchone()
    if emailid==None:
        query = "insert into userdetails (name,email,password) values('{}','{}','{}')".format(name, email, password)
        cur.execute(query)
        connection.commit()
    else:
        return "Acount Already exist"
    return render_template("form.html")


@app.route("/editUrl 1")
def editUrl():
    if 'email' in session:
        email = session['email']
        id=request.args.get("id")
        url=request.args.get("originalurl")
        encrypted=request.args.get("encrypted")
        return render_template("editUrl 1.html", url=url, encrypted=encrypted, id=id)
    return render_template("login.html")

@app.route('/updateUrl')
def updateUrl():
    id=request.form.get('id')
    url=request.form.get('orignalurl')
    encrypted=request.form.get('encrypted')
    print(url)
    print(id)
    print(encrypted)
    return encrypted
    connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
    cur = connection.cursor()
    data=cur.fetchone()
    if data == None:
        query1 = "update urlinfo set orignalUrl='{}', encryptedUrl='{}' where pk_urlId={}".format(url, encrypted, id)
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    else:
        return render_template("editUrl.html", url=url, encrypted=encrypted, id=id, error='short url already exist')

@app.route('/deleteUrl')
def deleteUrl():
    if 'email' in session:
        email = session['email']
        id = request.args.get('id')
        connection = connect(host="localhost", database="pythonapp", user="root", password="shubh@21")
        cur = connection.cursor()
        query1 = "delete from urlinfo where pk_urlid ='{}'".format(id)
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    return render_template("login.html")

def createEncryptedurl():
    letter = string.ascii_letters + string.digits

    encryptedurl = ''
    for i in range(6):    #First website of my own
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl   #THIS IS FIRST WEBSITE OF MY OWN.

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('userid',None)
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
