import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your_oauth_client_id')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', 'your_oauth_client_secret')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class LocalConfig(Config):
    MYSQL_UNIX_SOCKET = os.getenv('MYSQL_UNIX_SOCKET')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?unix_socket={MYSQL_UNIX_SOCKET}"
    )

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

def get_config():
    env = os.getenv('ENV', 'local')
    if env == 'local':
        return LocalConfig
    elif env == 'docker':
        return DockerConfig
    else:
        raise ValueError("Nieznane środowisko aplikacji. Ustaw zmienną ENV na 'local' lub 'docker'.")