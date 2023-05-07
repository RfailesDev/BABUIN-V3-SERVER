from flask import Flask, request

import API_system

app = Flask(__name__)

@app.route('/login')
def api():
    secret_key = request.args.get('secret_key')
    # Do something with the secret key
    return str(API_system.account_exists())

if __name__ == '__main__':
    app.run()