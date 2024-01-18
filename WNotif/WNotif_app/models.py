from SQLAlchemySingleton import SingletonSQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SingletonSQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80))
    username = db.Column(db.String(80),nullable=False,unique=True)
    sub = db.relationship("Subscription", back_populates="user")

#class Costraints(db.Model):
    #__tablename__ = 'constraints'
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))
    #tipo =   #tempmax #tempmin #snow{pioggia, grandine, neve}, latitudine e long
    #tipo = db.Column(db.String(20), nullable=False)
   # descrizione = db.Column(db.String(100))
    #valore =
    #percent =
 #   pass

class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    locazione = db.Column(db.String(80), nullable=False)
    t_max = db.Column(db.Integer, nullable = True)
    t_min = db.Column(db.Integer, nullable = True)
    w_condition = db.Column(db.String(80), nullable = True)
    user = db.relationship("User", back_populates="sub")

