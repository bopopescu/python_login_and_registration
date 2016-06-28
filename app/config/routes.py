
from system.core.router import routes


routes['default_controller'] = 'Welcome'
routes['POST']['/register'] = 'Welcome#register'
routes['POST']['/login'] = 'Welcome#login'



