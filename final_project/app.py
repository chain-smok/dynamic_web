from flask import Flask, session, render_template, redirect, request, url_for
from datetime import datetime, date
import sqlite3
import os
import jsonpickle

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_user(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_record(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM record where user_id = ? ORDER BY date DESC", [user_id])
    record = c.fetchall()
    conn.close()
    return record

def get_date_record(user_id, date):
    dateRecord = []
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM record where user_id = ? ORDER BY date DESC", [user_id])
    records = c.fetchall()
    conn.close()

    for record in records:
        dt = datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
        if dt.date() == date.date():
            dateRecord.append(record)
    return dateRecord

def get_daily_expense(records):
    daily_expense = 0
    today = date.today()
    for record in records:
        dt = datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
        if dt.date() == today and record[2] == 0:
            daily_expense += record[4]
    return daily_expense

def get_weekly_expense(records):
    weekly_expense = 0
    weekly_income = 0
    today = date.today()
    year, week, weekday = today.isocalendar()
    for record in records:
        dt = datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
        dt_year, dt_week, dt_weekday = dt.isocalendar()
        if dt_year == year and dt_week == week:
            if record[2] == 0:
                weekly_expense += record[4]
            elif record[2] == 1:
                weekly_income += record[4]
    return weekly_expense, weekly_income

def create_record():
    user_id = session['user_id']
    info = request.form['info']
    type = request.form['type']
    money = request.form['money']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user_id != '' and type != '' and money != '' and date != '' and info != '':
        con = sqlite3.connect('./data.db')
        con.execute(
            'insert into `record` (user_id,type,info,money,date) values (?,?,?,?,?)',(
                user_id, type, info, money, date
            )
        )
        con.commit()
        return redirect('/')
    else:
        return render_template('err.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        user_id = session['user_id']
        today = date.today().strftime("%Y-%m-%d %H:%M:%S")
        record = get_date_record(user_id, today)
        full_record = get_all_record(user_id)
        daily_expense = get_daily_expense(full_record)
        weekly_expense, weekly_income = get_weekly_expense(full_record)
        return render_template('index.html', records = record, daily_expense = daily_expense, weekly_expense = weekly_expense, weekly_income = weekly_income)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['account']
        password = request.form['pwd']

        user = get_user(username)
        if user and user[2] == password:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            info = '登入失敗！！！'
            return render_template('login.html', login_info = info)
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['account']
        password = request.form['pwd']
        con = sqlite3.connect('./data.db')
        con.execute(
            'insert into `user` (username,password) values (?,?)', [username, password]
        )
        con.commit()
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/record_action', methods=['POST', 'GET'])
def record_acrion():
    data = request.form
    if request.form['action'] == 'add':
        user_id = session['user_id']
        info = request.form['info']
        type = request.form['type']
        money = request.form['money']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if user_id != '' and type != '' and money != '' and date != '' and info != '':
            con = sqlite3.connect('./data.db')
            con.execute(
                'insert into `record` (user_id,type,info,money,date) values (?,?,?,?,?)',[
                    user_id, type, info, money, date]
            )
            con.commit()
            return redirect('/')
        else:
            return render_template('err.html')
    if request.form['action'] == 'delete':
        record_id = request.form['record_id']
        if record_id != '':
            con = sqlite3.connect('./data.db')
            con.execute('delete from `record` where `id` = ?', [record_id])
            con.commit()
            return redirect('/')
        else:
            return render_template('err.html', record_id = record_id)
    if request.form['action'] == 'update':
        record_id = request.form['record_id']
        new_info = request.form['info']
        new_price = request.form['money']
        new_type = request.form['type']
        if record_id != '':
            con = sqlite3.connect('./data.db')
            con.execute('update `record` set `type` = ?, `info` = ?, `money` = ? where `id` = ?', [new_type, new_info, new_price, record_id])
            con.commit()
            return redirect('/')
        else:
            return render_template('err.html', record_id = record_id)
        
@app.route('/update_date', methods=['GET'])
def update_date():
    user_id = session['user_id']
    date = request.args.get('date')
    record = get_date_record(user_id, date + " 00:00:00")
    full_record = get_all_record(user_id)
    daily_expense = get_daily_expense(full_record)
    weekly_expense, weekly_income = get_weekly_expense(full_record)
    return render_template('index.html', records = record, full_record = full_record, daily_expense = daily_expense, weekly_expense = weekly_expense, weekly_income = weekly_income)