import os
from flask import Flask, render_template

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=os.urandom(24),
))


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
