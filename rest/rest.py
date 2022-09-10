from flask import Flask, json
from flask_restful import Resource, Api, reqparse, request
import sqlite3
from stl import mesh
import werkzeug
from flask_cors import CORS

def convert_into_binary(file_path):
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary

def analyze_3d_file(name):
    file = mesh.Mesh.from_file(name)
    volume, _, _ = file.get_mass_properties()
    return round(volume,3)


def materials_db_init():
    conn=sqlite3.connect('materials.db')
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS materials(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        weight TEXT NOT NULL);
    """)
    conn.commit()
    cur.close()
    conn.close()

def users_db_init():
    conn=sqlite3.connect('users.db')
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        pass_hash TEXT NOT NULL,
        salt TEXT NOT NULL);
    """)
    conn.commit()
    cur.close()
    conn.close()

def orders_db_init():
    conn=sqlite3.connect('orders.db')
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        file_name text NOT NULL,
        file_blob text NOT NULL);
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_value_by_key(db_name,value):
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM "+db_name+" WHERE id = "+"'"+value+"'"+" ;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def get_value(db_name):
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM "+db_name+" ;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result


def push_element(db_name,lines):
  
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    
    
    values=[]
    
    for i in lines:
      values.append("'"+lines[i]+"'")
      
    values=", ".join(values)
    keys=", ".join(lines.keys())
    
    request="INSERT INTO "+db_name+"( "+keys+" ) VALUES( "+values+" );"
    #request="INSERT INTO "+db_name+" ("+keys+") VALUES( "+values+" );"
    try:
        cur.execute(request,lines)
    except sqlite3.IntegrityError:
        return -1
    conn.commit()
    cur.close()
    conn.close()
    return lines
    
def update_element(db_name, lines, id):
  
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    cur.execute("UPDATE "+db_name+" SET "+lines["update_param"]+" = "+"'"+lines["new_value"]+"'"+" WHERE id = "+id+" ;")
    conn.commit()
    cur.close()
    conn.close()
    return 0
    
class all_db(Resource):
      
    def get(self,db_name):
        
        return get_value(db_name)
      
    def post(self,db_name):
        # lines = json from post request { "line_name" : line_value , "line_name" : line_value...... }
        
        # example curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"test1\", \"price\": \"1\", \"weight\": \"1\" }" http://localhost:5000/
        
        lines = request.get_json()
        push_element(db_name,lines)

class single_element(Resource):
  
    def get(self,db_name,id):
        
        return get_value_by_key(db_name,id)
    
    def patch(self,db_name,id):
        #pars values from json { "key_param" : key_param , "key_value" : key_value , "update_param" : update_param , "new_value" : new_value }
        # example curl -X PATCH -H "Content-Type: application/json" -d "{ \"update_param\": \"update_param\", \"new_value\": \"new_value\" }" http://localhost:5000/
        lines = request.get_json()
        
        return update_element(db_name,lines,id)


class get_file(Resource):
    def post(self):
        #example curl -X POST -H "Content-Type: multipart/form-data" -F "file=@test.stl" http://127.0.0.1:5000/analyze
        if 'file' in request.files:
          file = request.files['file']
          file.save("files/"+file.filename)
          return {"volume":analyze_3d_file("files/"+file.filename)}
         
def main():
  
    materials_db_init()
    users_db_init()
    orders_db_init()
    
    app = Flask(__name__)
    
    
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    api = Api(app)
    
    api.add_resource(all_db, '/<string:db_name>')
    api.add_resource(get_file, '/analyze')
    api.add_resource(single_element, '/<string:db_name>/<string:id>')
    
    app.run()
main()
    

