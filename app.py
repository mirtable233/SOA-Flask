from flask import Flask

from py.routes.material_dao import borrow_blueprint

app = Flask(__name__)
app.register_blueprint(borrow_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=8081)
