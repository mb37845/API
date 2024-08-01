from flask import Flask
import config
import id_token
import os
from dotenv import load_dotenv 
from flask_cors import CORS
import authorization
import operation_on_transaction

load_dotenv() 

app = Flask(__name__)
CORS(app)

app.config.from_object(config)
app.config.from_object(id_token)

DB_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")


def db_init():
    config.init_db() 
    return 'Database initialized.'



@app.route('/',methods = ['GET'])
def home():
    return('Welocme To This Page')



@app.route('/login',methods = ['POST'])
def login():
    return(authorization.login())



@app.route('/signup' , methods = ['POST'])
def signup():
   return(authorization.signup())


@app.route('/change password', methods = ['PATCH'])
def change_password():
    return(authorization.change_password())


@app.route('/Add_income',methods = ['POST'])
def add_income():
   return(operation_on_transaction.add_income())
   

@app.route("/calculate_incomes",methods = ['POST'])
def calc_income():
   return(operation_on_transaction.calc_income())


@app.route('/Add_expense',methods = ['POST'])
def add_expense():
    return(operation_on_transaction.add_expense())


@app.route("/calculate_expenses",methods = ['POST'])
def calc_expense():
   return(operation_on_transaction.calc_expense())


@app.route("/saving" , methods =['POST'])
def saving():
  return(operation_on_transaction.saving())
   
   
   




   

if __name__ == '__main__':
    db_init()
    app.run(debug = True)
