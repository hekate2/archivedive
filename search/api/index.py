from vercel_wsgi import make_lambda_handler
from server.app import app

handler = make_lambda_handler(app)
