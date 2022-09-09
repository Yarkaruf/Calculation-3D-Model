from flask import Flask, json
from flask_restful import Resource, Api, reqparse, request
import sqlite3
from stl import mesh
import werkzeug

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
        name TEXT PRIMARY KEY,
        price TEXT,
        weight TEXT);
    """)
    conn.commit()
    cur.close()
    conn.close()

def users_db_init():
    conn=sqlite3.connect('users.db')
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        login TEXT PRIMARY KEY,
        pass_hash TEXT,
        salt TEXT);
    """)
    conn.commit()
    cur.close()
    conn.close()

def orders_db_init():
    conn=sqlite3.connect('orders.db')
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        name TEXT PRIMARY KEY,
        description TEXT,
        file_name text NOT NULL,
        file_blob text NOT NULL);
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_value_by_key(db_name,key,value):
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM "+db_name+" WHERE "+key+" = "+"'"+value+"'"+" ;")
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
    #keys=", ".join(lines.keys())
    
    #request="INSERT INTO "+db_name+"("+keys+") VALUES( "+values+" );"
    request="INSERT INTO "+db_name+" VALUES( "+values+" );"
    try:
        cur.execute(request,lines)
    except sqlite3.IntegrityError:
        return -1
    conn.commit()
    cur.close()
    conn.close()
    return 0
    
def update_element(db_name, key_param,key_value, update_param,new_value):
    conn=sqlite3.connect(db_name+".db")
    cur=conn.cursor()
    cur.execute("UPDATE "+db_name+" SET "+update_param+" = "+new_value+" WHERE "+key_parame+" = "+key_value+" ;")
    conn.commit()
    cur.close()
    conn.close()
    return 0


class materials(Resource):
    
    def get(self,id):
        
        return get_value_by_key("materials","name",id)
    
    def patch(self,id):
        #pars values from json { "key_param" : key_param , "key_value" : key_value , "update_param" : update_param , "new_value" : new_value 
        
        return update_element("materials", key_param,key_value, update_param,new_value)

class users(Resource):
    
    def get(self,id):
        
        return get_value_by_key("users","login",id)
    
    def patch(self,id):
        #pars values from json { "key_param" : key_param , "key_value" : key_value , "update_param" : update_param , "new_value" : new_value }
        
        return update_element("users",key_param,key_value,update_param,new_value)
    
class orders(Resource):
    
    def get(self,id):
        
        return get_value_by_key("orders","name",id)
    
    def patch(self,id):
        #pars values from json { "key_param" : key_param , "key_value" : key_value , "update_param" : update_param , "new_value" : new_value 
        
        return update_element("orders",key_param,key_value,update_param,new_value)
    
class all_db(Resource):
      
    def get(self,db_name):
        
        return get_value(db_name)
      
    def post(self,db_name):
        # lines = json from post request { "line_name" : line_value , "line_name" : line_value...... }
        
        # example curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"test1\", \"price\": \"1\", \"weight\": \"1\" }" http://localhost:5000/
        
        lines = request.get_json()
        push_element(db_name,lines)
  
class get_file(Resource):
    def post(self):
        #example curl -X POST -H "Content-Type: multipart/form-data" -F "file=@test.stl" http://127.0.0.1:5000/analyze
        if 'file' in request.files:
          file = request.files['file']
          # parse = reqparse.RequestParser()
          # parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
          # args = parse.parse_args()
          # file = args['file']
          file.save("files/"+file.filename)
          #return {"volume":analyze_3d_file("files/"+file.filename)}
         
def main():
  
    materials_db_init()
    users_db_init()
    orders_db_init()
    
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(materials, '/materials/<string:id>')
    api.add_resource(users, '/users/<string:id>')
    api.add_resource(orders, '/orders/<string:id>')
    api.add_resource(all_db, '/<string:db_name>')
    api.add_resource(get_file, '/analyze')
    
    app.run()
main()
    

