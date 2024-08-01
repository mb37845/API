from flask import request,jsonify
import sqlite3
import id_token
import os


DB_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")


def login():
    data = request.get_json()
    name = data['name']
    password = data['password']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name = ? and password = ?", (name,password))
    result = cursor.fetchall()
    if len(result) != 0:
       token_id = id_token.create_token(result[0][0])
       response = jsonify( {'message': "You Login Succefully!", 'token': token_id}),200
    
    else:
       response = jsonify({'message': "Failed To Login"}) , 404
       
    conn.commit()
    conn.close()

    return (response)


def signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
    result = cursor.fetchall()
    #if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password) and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
    # password = hash(password)
    if (len(result)== 0):
        cursor.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(name,email,password))
        response = jsonify({'message': "Signup Succefully!"}) , 200
        
       
    else:
        response = jsonify({'message': "Signed up before!"}) , 404
    
    conn.commit()
    conn.close()

    return (response)


def change_password():
    data = request.get_json()
    name = data['name']
    email = data['email']
    new_password = data['new_password']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    password = cursor.execute("SELECT password FROM users WHERE name = ? and email = ? ",(name,email))
    if len(password.fetchall()) == 1: 
     cursor.execute("UPDATE users SET password = ? WHERE email = ? and name = ?",(new_password,email,name))
     response = jsonify({'message': "The Password Changed Succefully"}) , 200
    
    else :
     response = jsonify({'message': "The name or email is wrong"}) , 404
     
    conn.commit()
    conn.close()
    return (response)