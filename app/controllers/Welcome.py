from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        self.load_model('User')

    def index(self):
        return self.load_view('index.html')
    def login(self):
        user = {
            'email' : request.form['email'],
            'password' : request.form['password']
        }
        login_user = self.models['User'].login(user)

        if login_user['status'] == True:
            session['id'] = login_user['user']['id']
            session['first_name'] = login_user['user']['first_name']
            return self.load_view('success.html')
        else:
            for message in login_user['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def register(self):
        user_details = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : request.form['password'],
            'confirm_password' : request.form['confirm_password']
        }
        # print dir(self.models['User'])
        user_status = self.models['User'].register(user_details)

        if (user_status['status']==True):
            session['id']=user_status['user']['id']
            session['first_name']=user_status['user']['first_name']
            session['last_name']=user_status['user']['last_name']
            session['email']=user_status['user']['email']
            return redirect('/')
        else:
            for message in user_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')        
