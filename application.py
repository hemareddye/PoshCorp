#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
import time
from oauthlib import oauth1
import oauthlib
import requests


application = Flask(__name__)


@application.route('/', methods=['GET'])
def get():
    MerchantId = "bd5c1517-8d80-48d7-8e8e-365433ad124f"
    public_key = "VFHRRIQQ"
    secret_key = "QQ8ZDIEHHIX5WPYKGXIY5YSF"
    TestEnv = "http://www.testln.martjack.com/devapi/"
    Staging = "http://www.stageln.martjack.com/devapi"
    ProdEnv = "http://www.martjack.com/devapi"

    def timestamp():
        t = time.time()
        return t
    pass

    url = TestEnv + 'Pricelist/' + MerchantId

    def signatureBuilder(public_key, secret_key):
        client = oauthlib.oauth1.Client(client_key=public_key, client_secret=secret_key, signature_type=oauth1.SIGNATURE_TYPE_QUERY, signature_method=oauth1.SIGNATURE_HMAC, timestamp = timestamp())
        uri, header, body = client.sign(url, http_method = 'get')
        return uri ,header
    pass

    def response():
        u, h = signatureBuilder(public_key, secret_key)
        response = requests.get(u, auth = h, headers = {'accept':'application/json'})
        return response.text
    return response()


@application.route('/', methods=['POST'])
def post():
    return '{"Output":"Hello World"}'


if __name__ == '__main__':
    flaskrun(application)
