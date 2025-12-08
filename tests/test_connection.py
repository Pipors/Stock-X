import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Test with .env values
print("Testing connection with .env values...")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"Port: {os.getenv('DB_PORT')}")
print(f"Database: {os.getenv('DB_NAME')}")
print(f"User: {os.getenv('DB_USER')}")
print(f"Password: {os.getenv('DB_PASSWORD')}")

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    print("\n✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nTrying common default passwords...")
    
    # Try common passwords
    for pwd in ['postgres', 'password', '123456', 'admin', '']:
        try:
          print(f"  Trying password: '{pwd}'")
          conn = psycopg2.connect(
              host=os.getenv('DB_HOST'),
              port=os.getenv('DB_PORT'),
              database=os.getenv('DB_NAME'),
              user=os.getenv('DB_USER'),
              password=pwd
          )
          print(f"\n✅ Success! The correct password is: '{pwd}'")
          print(f"\nUpdate your .env file:")
          print(f"DB_PASSWORD={pwd}")
          conn.close()
          break
        except Exception as e2:
          print(f"    Failed")
