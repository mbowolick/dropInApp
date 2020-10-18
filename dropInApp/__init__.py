from flask import Flask, render_template, request
from .app.payments import getPaymentMethods, sendPayment, getPaymentsDetails
from configparser import ConfigParser

app = Flask(__name__)

# Read in Config
parser = ConfigParser()
parser.read('params.ini')
merchant_account = parser['DEFAULT']['merchant_account']
checkout_apikey = parser['DEFAULT']['checkout_apikey']
client_key = parser['DEFAULT']['client_key']

# Route for Home
@app.route("/")
def home():
    if (client_key == 'exampleKey'):
        abort("Unable to start, config.ini is not updated to actual params. ")
    return render_template("home.html", title="Demo Store")

# Route for Checkout
@app.route('/checkout')
def checkout():
    paymentMethods = getPaymentMethods()
    return render_template('checkout.html', 
        title="Checkout",
        paymentMethods=paymentMethods, 
        clientKey=client_key)

# Route for Application Payment Request API (with drop-in Event Data)
@app.route('/payments/payment', methods=['POST'])
def payments():
    paymentResponse = sendPayment(request.get_json()) # Response to SendPayment
    return paymentResponse

# Route for redirectHandler
@app.route('/redirectHandler')
def orderRedirectHandler():
    # Load the payload from the URL parameters and pass to getPaymentsDetails to get the payment results
    redirectedPaymentDetails = getPaymentsDetails(request.args.get('payload'))
    
    if (redirectedPaymentDetails['resultCode'].lower() == 'authorised' or
        redirectedPaymentDetails['resultCode'].lower() == 'received'): 
        return render_template('success.html', 
            resultCode=redirectedPaymentDetails['resultCode'],
            merchantReference=redirectedPaymentDetails['merchantReference'],
            pspReference=redirectedPaymentDetails['pspReference'],
            paymentMethod=redirectedPaymentDetails['paymentMethod']
        )
    else:
        return render_template('failure.html')

# Route for order Success
@app.route('/success')
def orderSuccess():
    return render_template('success.html', 
        resultCode=request.args.get('resultCode'),
        merchantReference=request.args.get('merchantReference'),
        pspReference=request.args.get('pspReference'),
        title="Your Order Was Successful!"  )

# Route for order failure
@app.route('/failed')
def orderFailed():
    return render_template('failure.html',
        title="An Error Occurred"  )

# Route for Application Payment Details Request API (with drop-in Event Data). Required during redirect. 
@app.route('/payments/details', methods=['POST'])
def paymentDetails():
    paymentDetails = getPaymentsDetails(request.get_json())
    return paymentDetails

if __name__ == '__main__':
    app.run()