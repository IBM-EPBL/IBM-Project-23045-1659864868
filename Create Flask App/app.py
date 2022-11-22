from flask import Flask,render_template

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/home')

def helloworld():
    return render_template("homepage.html");

if __name__ == '__main__':
    app.run()


