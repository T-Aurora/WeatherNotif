import json
import logging
from flask import Flask, request, redirect, url_for,Response
import SQLAlchemySingleton
from WNotif_app import models
from pproducer import ProducerW
import threading
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://wnotif:wnotif@weatherdb/wdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    models.db.init_app(app)
    producer = ProducerW(app)
    with app.app_context():
        models.db.create_all()
        try:
            thread = threading.Thread(target=producer.produce_weather_message, args=(app,))
            thread.start()
        except Exception as e:
            logging.error(f"Error producing weather message: {e}")
    @app.route('/')
    def hello():
        return 'Welcome to WeatherNotif!'

    @app.route('/add_user', methods=['POST'])
    def adduser():
        if request.method == 'POST':
            nome, chat_id = (
                request.form['nome'],
                request.form['chat_id']
            )
            #chat_id gia presente
            ex_user = models.User.query.filter_by(chat_id=chat_id).first()
            if ex_user:
                print("!!!!Chat ID already exists.!!!!") #gestire con excep
                # mysql.connector.errors.IntegrityError: 1062 (23000): Duplicate entry '275927520' for key 'user.chat_id'
            else:
                #end
                new_user = models.User(nome=nome, chat_id=chat_id)
                models.db.session.add(new_user)
                models.db.session.commit()

                return "User: "+nome+" committed"

    @app.route('/all_user')
    def show_users():
        def generate_users():
            with app.app_context():
                all_users = models.User.query.all()
                for user in all_users:
                    yield 'Utente: '+str(user.id)+' Nome: '+user.nome+' Chat_id: '+user.chat_id+'\n'
        return Response(generate_users(), content_type='text/plain')

    @app.route('/find_user',methods=['POST'])
    def find_user():
        if request.method == 'POST':
            nome, chat_id = (
                request.form['nome'],
                request.form['chat_id']
            )
            user_id = models.User.query.filter_by(chat_id=chat_id).first()
            if user_id:
                print(user_id)
                return str(user_id)
            else:
                return "Utente non trovato"
    # region

    @app.route('/add_subb', methods=['POST'])
    def add_subb():
        if request.method == 'POST':
            user = request.form.get('user_id')
            locazione = request.form.get('locazione')
            t_max = request.form.get('t_max', default=None)
            t_min = request.form.get('t_min', default=None)
            w_condition = request.form.get('w_condition', default=None)
            t_max = int(t_max) if t_max is not None and t_max.isdigit() else None
            t_min = int(t_min) if t_min is not None and t_min.isdigit() else None
            w_condition = w_condition if w_condition else None

            print("Received data:")
            print(f"user_id: {user}")
            print(f"locazione: {locazione}")
            print(f"t_max: {t_max}")
            print(f"t_min: {t_min}")
            print(f"w_condition: {w_condition}")

            new_subb=models.Subscription(user_id=user, locazione=locazione,t_max=t_max,t_min=t_min, w_condition=w_condition)
            models.db.session.add(new_subb)
            models.db.session.commit()
            return "Subscription added for user with ID: "+str(user)

    # endregion


    @app.route('/show_sub', methods=['POST'])
    def show_subs():
        if request.method == 'POST':
            chat = request.form.get('chat_id')
            subscriptions = models.Subscription.query.join(models.User).where(models.Subscription.user_id == models.User.id).filter(models.User.chat_id == chat).all()
            subs_data = []
            print(subscriptions)
            for sub in subscriptions:
                print(sub.locazione)
                subs_data.append({
                    'locazione': sub.locazione,
                    't_max': sub.t_max,
                    't_min': sub.t_min,
                    'w_condition': sub.w_condition
                })

            json_subs_data = json.dumps(subs_data)

                # Restituisci la risposta JSON
            return json_subs_data, 200, {'Content-Type': 'application/json'}



    return app