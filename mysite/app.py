from flask import Flask
from multicards import pages as m
from phyoid import pages as p

app = Flask(__name__)
app.register_blueprint(m.bp)
app.register_blueprint(p.bp)

if __name__ == '__main__':
    app.run(debug=True)
