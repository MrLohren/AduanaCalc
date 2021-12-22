from flask import Flask, render_template, request
import requests
import os

API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    def convert(_from: str, _to: str, qty=1) -> float:
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}'.format(
            _from, _to, API_KEY)
        response = requests.get(url=url).json()
        value = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return float(value)*qty

    if request.method == 'POST':
        try:
            amount = request.form['amount']
            amount = float(amount)

            result = convert('CLP', 'USD', qty=amount)

            if result >= 30:
                # Tax Calc
                def _tax(x): return (x + (x)*0.06)*0.19

                return render_template('index.html',
                                       usd_value=convert('USD', 'CLP'),
                                       _import='{:0.2f}'.format(result),
                                       warning='Debe pagar!',
                                       tax='El impuesto que le corresponde es: $CLP {:0.2f}'.format(
                                           convert('USD', 'CLP', qty=_tax(result))))

            else:
                return render_template('index.html',
                                       usd_value=convert('USD', 'CLP'),
                                       _import='{:0.2f}'.format(result),
                                       warning='Felicidades! No paga impuesto!',
                                       tax='')

        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)

    else:
        return render_template('index.html',
                               usd_value=convert('USD', 'CLP'),
                               _import=0,
                               warning='',
                               tax='')

if __name__ == "__main__":
    app.run()