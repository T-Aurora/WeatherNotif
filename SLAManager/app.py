from SLAManager_app import create_app
import time

app, db = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=6000)
