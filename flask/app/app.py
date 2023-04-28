from flask import Flask,render_template,jsonify,request,redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        user='flask',
        password='flask',
        host='3c3dd07cf6f4',
        database='flask'
    )
    return conn

@app.route('/')
def main_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todo_list')
    todos = cursor.fetchall()
    cursor.execute('SELECT * FROM complete_list')
    completes = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos,completes=completes)

@app.route('/addtask',methods=['POST'])
def addtask():
    taskname=request.form['task']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todo_list (task) VALUES (%s)', (taskname,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/completion',methods=['POST'])
def completion():
    id= request.form['id']
    taskname = request.form['task']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todo_list WHERE id=(%s)', (id,))
    cursor.execute('INSERT INTO complete_list (task) VALUES (%s)', (taskname,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete',methods=['POST'])
def delete():
    id= request.form['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM complete_list WHERE id=(%s)', (id,))
    conn.commit()
    conn.close()
    return redirect('/')