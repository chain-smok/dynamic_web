from flask import Flask, request,render_template
import sqlite3
import os
app = Flask(__name__)
def is_valid(account, password):
    con = sqlite3.connect('project.db')
    cur = con.cursor()
    cur.execute('SELECT account, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == account and row[1] == password:
            return True
    return False
@app.route('/')
def Hello():
    return render_template('homepage.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if is_valid(account, password):
            return "登入成功"
        else:
            error = 'Invalid Account / Password'
            return render_template('login.html', error=error)
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        repassword=request.form['repassword']
        phone = request.form['phone']
        address = request.form['address']
        if password!=repassword:
            error="密碼確認有誤"
            return render_template('registration.html',error=error)
    
    with sqlite3.connect('project.db') as conn:
         cur = conn.cursor()
         cur.execute('''INSERT INTO users (account,password,phone,address) VALUES (?, ?, ?, ?)''', (account,password,phone,address))
         conn.commit()

    return render_template('homepage.html')


if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
