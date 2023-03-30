from flask import Flask, request,render_template
import json

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

