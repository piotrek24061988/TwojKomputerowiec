from flask import Flask, render_template, url_for
app = Flask(__name__, template_folder='Szablony')

posty = [
    {
        'autor': 'Piotr Górecki',
        'tytul': 'Strona w przygotowaniu',
        'tresc': 'Trwa przygotowanie strony firmowej',
        'data': '05.03.2021'
    },
    {
        'autor': 'Piotr Górecki',
        'tytul': 'Firma w przygotowaniu',
        'tresc': 'Trwa przygotowanie koncecji firmy',
        'data': '05.03.2021'
    }
]

@app.route('/')
@app.route('/home')
@app.route('/dom')
def stronaStartowa():
    return render_template('domowa.html')


@app.route('/news')
@app.route('/aktualnosci')
def aktualnosci():
    return render_template('aktualnosci.html', posts=posty)


@app.route('/contact')
@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


@app.route('/about')
@app.route('/oMnie')
def oMnie():
    return render_template('oMnie.html')


if __name__ == '__main__':
    app.run(debug=True)