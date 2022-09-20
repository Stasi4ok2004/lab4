from flask import Flask

app = Flask(__name__)



@app.route("/api/v1/hello-world-9")
def home():

    return f"Hello world! 9 variant"


