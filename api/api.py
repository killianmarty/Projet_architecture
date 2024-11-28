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

    signinResult = signin(username, password, firstName, lastName)
    
    #Create a page for the new user if the signin succeed
    if(signinResult[1] == 200):
        
        createPageResult = create_page(signinResult[0].json['userId'], firstName + " " + lastName, "Description", "Activity", False)
    
    return signinResult


@app.route('/login', methods=['POST'])
def login_controller():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return login(username, password)


@app.route('/page', methods=['GET', 'POST'])
def page_controller():

    if(request.method == 'POST'):
        data = request.get_json()
        visible = data.get('visible')
        pageName = data.get('page_name')
        description = data.get('description')
        activity = data.get('activity')
        print(pageName, description, activity, visible)
        return update_page(pageName, description, activity, visible)
    else:
        userId = authenticate_token()
        return get_user_page(userId)



@app.route('/page/<int:pageId>', methods=['GET'])
def get_id_controller(pageId):

    return get_page(pageId)


@app.route('/page/disponibilities', methods=['GET','POST'])
def page_disponibilities_controller():
    if(request.method == 'GET'):
        return get_user_disponibilities()
    else:
        data = request.get_json()
        date = data.get('date')

        return create_disponibility(date)
    
@app.route('/page/disponibilities/<int:disponibilityId>', methods=['DELETE'])
def page_disponibilities_id_controller(disponibilityId):
    return delete_disponibility(disponibilityId)


@app.route('/page/<int:pageId>/disponibilities', methods=['GET'])
def page_id_disponibilities_controller(pageId):
    return get_disponibilities(pageId)

@app.route('/page/<int:pageId>/disponibilities/<int:disponibilityId>', methods=['POST'])
def page_id_disponibilities_id_controller(pageId, disponibilityId):

    data = request.get_json()
    name = data.get('name')
    mail = data.get('mail')

    return book_disponibility(pageId, disponibilityId, name, mail)
        

@app.route('/cancel', methods=["DELETE"])
def cancel_controler():
    data = request.get_json()
    cancel_code = data['cancel_code']
    print(cancel_code)
    return free_disponibility(cancel_code)

@app.route('/search', methods=["GET"])
def search_query_controler():
    return search_pages(request.args.get("query"))

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
