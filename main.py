
from waitress import serve
from waitress_main import app


serve(app, host='127.0.0.1', port=8080, threads = 6)