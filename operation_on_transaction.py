from flask import request,jsonify
import sqlite3
import id_token
import os
from flask_cors import CORS
import API
from datetime import datetime


DB_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
CORS(API.app)

def check_for_access():
    
    # Get the decoded data 
    try: 
     print(request.headers)
     access_token = request.headers["Authorization"].split()[1]
    except Exception as e:
     print('error', str(e))
     return (False,(jsonify({'error': str(e)}), 401)) 
    
    try: 
     decoded_token = id_token.decode_token(access_token,SECRET_KEY)
   
    except decoded_token.ExpiredSignatureError:
        return (False,(jsonify({'error': 'Token has expired'}), 401)) 
        
    except decoded_token.InvalidTokenError:
        return (False,(jsonify({'error': 'Invalid token'}), 401))
       
    except Exception as e:
        return (False,(jsonify({'error': str(e)}), 400)) 
      
    
    # Check user id 
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ? ", (decoded_token['user_id'],))
    if len(cursor.fetchall()) != 0:
       flag =  True
    else:
       flag = False
    conn.commit()
    conn.close()
    return (flag,decoded_token['user_id'])


def add_income():
    data = request.get_json()
    access = check_for_access()
    if (access[0] == False):
       return jsonify({'message': "unauthorized access"}) , 403
    source = data['source']
    amount = data['amount']
    if(amount < 0):
       return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
   
    date = data['date']
    if(not datetime.strptime(date, "%Y-%m-%d")):
        return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
       
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("SELECT * FROM incomes")
    before = cursor.fetchall()
    cursor.execute("INSERT INTO incomes (user_id,source,amount,date) VALUES (?,?,?,?)",(access[1],source,amount,date))
    cursor.execute("SELECT * FROM incomes")
    after = cursor.fetchall()
    conn.commit()
    conn.close()
    if(len(after)-len(before) == 1):
       return(jsonify({'message': "Added Succefully"}) , 200)
    else:
     return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
    


def calc_income():
    access = check_for_access()
    if (access[0] == False):
       return jsonify({'message': "unauthorized access"}) , 403
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(AMOUNT) FROM incomes WHERE user_id = ?" , (access[1],))
    result = cursor.fetchall()
    if(result[0][0] == None):
       result = 0
    else:
       result = result[0][0]
    conn.commit()
    conn.close()
    return(jsonify({'result': result}))



def add_expense():
    data = request.get_json()
    access = check_for_access()
    if (access[0] == False):
       return (access[1])
    conn = sqlite3.connect(DB_NAME)
    source = data['source']
    amount = data['amount']
    if(amount < 0):
       return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
   
    date = data['date']
    if(not datetime.strptime(date, "%Y-%m-%d")):
        return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    before = cursor.fetchall()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("INSERT INTO expenses (user_id,source,amount,date) VALUES (?,?,?,?)",(access[1],source,amount,date))
    cursor.execute("SELECT * FROM expenses")
    after = cursor.fetchall()
    conn.commit()
    conn.close()
    if(len(after)-len(before) == 1):
       return(jsonify({'message': "Added Succefully"}) , 200)
    else:
     return(jsonify({'message': "There is a mistake in entries please check them"}) , 404)
    


def calc_expense():
    access = check_for_access()
    if (access[0] == False):
       print(type(jsonify({'message': "unauthorized access"})))
       return jsonify({'message': "unauthorized access"}) , 403
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(AMOUNT) FROM expenses WHERE user_id = ?" , (access [1],))
    result = cursor.fetchall()
    if(result[0][0] == None):
       result = 0
    else:
       result = result[0][0]
    conn.commit()
    conn.close()
    return(jsonify({'result': result}))



def saving():
   access = check_for_access()
   if (access[0] == False):
       return jsonify({'message': "unauthorized access"}) , 403
   income_response = calc_income()
   data = income_response.get_json()
   income_result = data.get('result')

   expense_response = calc_expense()
   data = expense_response.get_json()
   expense_result = data.get('result')
   result = float(income_result) - float(expense_result)
   return(jsonify({'result': result}))