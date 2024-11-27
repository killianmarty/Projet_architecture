from flask import Flask, request

from database import *
from authentification import *
from page import *
from disponibility import *


app = Flask(__name__)


@app.route('/signin', methods=['POST'])
def signin_controller():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    firstName = data.get('first_name')
    lastName = data.get('last_name')

    return signin(username, password, firstName, lastName)


@app.route('/login', methods=['POST'])
def login_controller():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return login(username, password)


@app.route('/page', methods=['POST'])
def page_controller():

    data = request.get_json()
    visible = data.get('visible')
    pageName = data.get('page_name')
    description = data.get('description')

    return create_page(pageName, description, visible)


@app.route('/page/<int:pageId>', methods=['GET'])
def get_id_controller(pageId):

    return get_page(pageId)


@app.route('/page/<int:pageId>/disponibilities', methods=['POST'])
def page_id_disponibilities_controller(pageId):

    data = request.get_json()
    date = data.get('date')

    return create_disponibility(pageId, date)


@app.route('/page/<int:pageId>/disponibilities/<int:disponibilityId>', methods=['POST', "DELETE"])
def page_id_disponibilities_id_controller(pageId, disponibilityId):

    if(request.method == 'POST'):

        data = request.get_json()
        name = data.get('name')
        mail = data.get('mail')

        book_disponibility(pageId, disponibilityId, name, mail)

    elif(request.method == 'DELETE'):

        delete_disponibility(pageId, disponibilityId)



if __name__ == '__main__':
    app.run(port = 5000, debug=True)
