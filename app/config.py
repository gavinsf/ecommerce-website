from dotenv import load_dotenv
import os
import boto3

load_dotenv()

def get_jwt_secret():
    secret_name = os.getenv("AWS_SECRET_NAME")
    region = os.getenv("AWS_REGION")

    client = boto3.client(service_name="secretsmanager", region_name=region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response["SecretString"]
    except Exception as e:
        print("Error : Failed to retrieve JWT secret")
        raise e

class Settings():
    DB_URL = os.getenv("DB")
    DEBUG = True
    ACCESS_TOKEN_EXPIRE = 3600
    REFRESH_TOKEN_EXPIRE = 3600 * 24 * 14 # 2 weeks
    JWT_SECRET = get_jwt_secret()

settings = Settings()