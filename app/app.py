from flask import Flask,render_template,jsonify,request,redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        user='flask',
        password='flask',
        host='my-db-host',
        database='flask'
    )
    return conn

@app.route('/')
def main_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks where completed = 0')
    todos = cursor.fetchall()
    cursor.execute('SELECT * FROM tasks where completed = 1')
    completes = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos,completes=completes)

@app.route('/addtask',methods=['POST'])
def addtask():
    taskname=request.form['task']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task_name,completed) VALUES (%s,%s)', (taskname,0))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/completion',methods=['POST'])
def completion():
    id= request.form['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = %s WHERE id = %s', (1, id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/back',methods=['POST'])
def back():
    id= request.form['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = %s WHERE id = %s', (0, id,))
    conn.commit()
    conn.close()
    return redirect('/')
@app.route('/delete',methods=['POST'])
def delete():
    id= request.form['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=(%s)', (id,))
    conn.commit()
    conn.close()
    return redirect('/')