from system.core.model import *
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()


    def register(self, user):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not user['first_name']:
            errors.append('Name cannot be blank')
        elif len(user['first_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid!')
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['confirm_password']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            pw = self.bcrypt.generate_password_hash(user['password'])
            query = "INSERT INTO user (first_name, last_name, email, password, created_at) VALUES (%s, %s, %s, %s, NOW())"
            data = [user['first_name'], user['last_name'], user['email'], pw]
            self.db.query_db(query, data)

            get_user_query = "SELECT * FROM user ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)

            return {"status": True, "user": users[0]}

    def login(self, user):
        query = "SELECT * FROM user WHERE email = '{}'".format(user['email'])
        id = self.db.query_db(query)

        if user and self.bcrypt.check_password_hash(id[0]['password'], user['password']):
            id = self.db.query_db(query)
            return {'status': True, 'user': id[0]}
        else:
            errors = []
            errors.append('Invalid info')

            return {'status': False, "errors": errors}

      
