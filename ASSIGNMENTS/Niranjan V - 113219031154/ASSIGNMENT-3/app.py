from flask import Flask,render_template
app = Flask(__name__)

app.config['DEBUG'] = True



@app.route("/")

def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
