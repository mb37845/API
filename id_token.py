import jwt
from datetime import timedelta, datetime, timezone
import os
from dotenv import load_dotenv
import json

load_dotenv() 

def create_token(id):

 secret_key = os.getenv("SECRET_KEY")

 payload = {
    'user_id': id,
    'exp': datetime.now(timezone.utc) + timedelta(hours=3)
 }
 token = jwt.encode(payload, secret_key, algorithm='HS256')
 return token
 
  

def decode_token(token,secret_key):
 decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
 print(token)
 print(decoded_payload)
 return decoded_payload





 