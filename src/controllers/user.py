from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import User, db
from http import HTTPStatus


app = Blueprint('user', __name__, url_prefix='/users')


def create_user():
    data = request.json
    user = User(username = data['username'])

    db.session.add(user)
    db.session.commit()


def list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    return [
        {
            'id': user.id,
            'username': user.username
        }
        for user in users
    ]



@app.route('/', methods=['GET', 'POST'])
def handle_users():

    if request.method == 'POST':
        create_user()
        return {'message': 'user created'}, HTTPStatus.CREATED
    else:
        return {"users": list_users()}, HTTPStatus.OK
    
# list users by id
@app.route('/<int:user_id>')
def get_user(user_id):
   user = db.get_or_404(User, user_id)
   return{
       "id": user.id,
       "username": user.username,
   }
# update user
@app.route('/<int:user_id>', methods = ['PATCH'])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    mapperUser = inspect(User)
    for column in mapperUser.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    

    return {
        "id": user.id,
        "username": user.username,
    }

# delete 
@app.route('/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT