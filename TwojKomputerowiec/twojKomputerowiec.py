from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/dom')
def strona_startowa():
    return '<h1>Strona startowa</h1>'

@app.route('/o_mnie')
@app.route('/about')
def o_mnie():
    return '<h1>O mnie</h1>'

if __name__ == '__main__':
    app.run(debug=True)