from flask_sqlalchemy import SQLAlchemy

class SingletonSQLAlchemy(SQLAlchemy):
    _instance=None

    def __new__(cls, app=None):
        if not cls._instance:
            cls._instance = super(SingletonSQLAlchemy, cls).__new__(cls)
        return cls._instance