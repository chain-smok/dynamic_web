from flask import Flask, request,render_template
import json
import sqlite3
app = Flask(__name__)
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        
        account = request.form['account']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT INTO groups(account,password,address,phone) VALUES \
                  (?, ?, ?, ?)",(account,password,address,phone))
        conn.commit()
        print ("数据插入成功")
        conn.close()
    
        data = {
            "account": account,
            "password": password,
            "phone": phone,
            "address": address
        }
        jsonfile=open('user_data.json','r')
        info = json.load(jsonfile)
        info.append(data)
        with open('user_data.json','w') as f:
            json.dump(info, f,ensure_ascii=False)
        
    
        return "註冊成功"

