from flask import Flask, jsonify
from flask import render_template
from flask import request, redirect, url_for
import mariadb
import sys
import json
from datetime import datetime

app = Flask(__name__)




app.config["DEBUG"] = True

# configuration used to connect to MariaDB
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '#Siebzehn123',
    'database': 'Termine'
}





@app.route('/db', methods=['GET'])
def db():
   # connection for MariaDB
   conn = mariadb.connect(**config)
   # create a connection cursor
   cur = conn.cursor()
   # execute a SQL statement
   cur.execute("select * from first")


   
    
   # serialize results into JSON
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))

   return render_template('db.html', headers=row_headers, data=json_data)

    
    










@app.route('/k', methods=['POST', 'GET'])
def k():
    date = request.args.get('date')
    
    
    
    # Um aktuelle Termine anzuzeigen
    conn2 = mariadb.connect(**config)
    
    cur2 = conn2.cursor()
    
    cur2.execute("select * from first where datum=?", (date,))
    
    conn2.commit()
    
    
    row_headers=[x[0] for x in cur2.description]
    
    #row_headers.remove('id')
        

    rv = cur2.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
            
    #for data in json_data:
    #        if id in data:
    #            del data[id]
                
                
    return render_template('k.html', date=date, headers=row_headers, data=json_data)






@app.route('/adding', methods=['POST'])
def add_entry():
    data = request.json
    date = data['date']
    name = data['name']
    time = data['time']
   
    conn = mariadb.connect(**config)
    
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO first (name, datum, zeit) VALUES (?, ?, ?)', (name, date, time))
        conn.commit()
        new_id = cursor.lastrowid  
        return jsonify({'success': True, 'id': new_id})
    except mariadb.Error as e:
        print(f"Error: {e}")
        return jsonify({'success': False})
    finally:
        cursor.close()
        conn.close()

    







@app.route('/delete', methods=['POST', 'GET'])
def delete():   
    data = request.json
    id = data['id']
    
    conn = mariadb.connect(**config)
    
    cursor = conn.cursor()
    
    try:    
        cursor.execute("delete from first where id = %s", (id,))
        conn.commit()
        return jsonify({'success': True})
    except mariadb.Error as e:
        print(f"Error: {e}")
        return jsonify({'success': False})
    finally:
        cursor.close()
        conn.close()
    




@app.route('/test')
def test():
    
    return render_template('test.html')

   





@app.route('/')
def index():
    return render_template('index.html')


















if __name__ == '__main__':
    app.run(debug=True, port=8080)