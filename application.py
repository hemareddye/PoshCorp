#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
import time
from oauthlib import oauth1
import requests
from urllib.parse import urlencode
import oauthlib.oauth1
import re
import random
import json

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    
    MerchantId = "bd5c1517-8d80-48d7-8e8e-365433ad124f"
    public_key = "VFHRRIQQ"
    secret_key = "QQ8ZDIEHHIX5WPYKGXIY5YSF"
    EnvUrl = "http://www.testln.martjack.com/devapi/"
    Staging = "http://www.stageln.martjack.com/devapi"
    ProdEnv = "http://www.martjack.com/devapi" 
    
    host = "poshlette.cnauabwc9dbm.us-east-1.rds.amazonaws.com"
    port = "3306"
    user = "sandieps"
    password = "Sandie0713"
    database = "PoshCorp"

    def timestamp():
        t = time.time()
        return t
    pass
    
    url = EnvUrl + 'Pricelist/' + MerchantId
    url2 = EnvUrl + 'Location/' + MerchantId + '/search'
    
    def GET_signatureBuilder(public_key, secret_key, url):
        client = oauthlib.oauth1.Client(client_key=public_key, client_secret=secret_key, signature_type=oauth1.SIGNATURE_TYPE_QUERY, signature_method=oauth1.SIGNATURE_HMAC, timestamp = timestamp())  
        uri, header, body = client.sign(url, http_method='GET')
        return uri
        
    def POST_signatureBuilder(public_key, secret_key, url):
        client = oauthlib.oauth1.Client(client_key=public_key, client_secret=secret_key, signature_type=oauth1.SIGNATURE_TYPE_QUERY, signature_method=oauth1.SIGNATURE_HMAC, timestamp = timestamp())  
        uri, header, body = client.sign(url, http_method='POST')
        return uri
            
    def Getpricelists():
        u = GET_signatureBuilder(public_key, secret_key, url)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
        Getpricelists = response.json()
        PricelistRefcode = (Getpricelists["PriceListDetails"][1]["ReferenceCode"])
        LocationId = (Getpricelists["PriceListDetails"][1]["LocationId"])
        return PricelistRefcode, LocationId
    
    PricelistRefcode, LocationId = Getpricelists()
    
    def Products():
        url7 = EnvUrl + 'Product/' + MerchantId + '/Search'
        u = POST_signatureBuilder(public_key,secret_key,url7)
        params  = {'Merchantid' : MerchantId}
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}, data=params)
        a = response.json()
        i = random.randint(0,100)
        productId = (a['ProductIds'][i])
        pricelistrefcode, locationId = Getpricelists()
        url8 = EnvUrl + 'Product/Information/' + MerchantId +'/' +productId +  '/' + str(locationId)
        u = GET_signatureBuilder(public_key,secret_key,url8)
        response2 = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
        skufetch = response2.json()
        sku = skufetch['Product']['SKU']
        r = response2.json()
        r1 = r['Product']['IsParentProduct']
        def variantproduct():
            if r1 == True:
                url9 = EnvUrl + 'Product/Varients/' + MerchantId +'/' + productId + '/ALL'
                u = GET_signatureBuilder(public_key,secret_key,url9)
                response3 = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
                variantskufetch = response3.json()
                variantsku = variantskufetch['ProductVarient'][0]['SKU']
                return variantsku
            elif r1 == False:
                return sku
        return sku, variantproduct()
      
    sku,variantsku =  Products()
        
    def PricelistAPI():
        
        url3 = EnvUrl + 'Pricelist/' + MerchantId +  '/' + PricelistRefcode + "/upload"
        u = POST_signatureBuilder(public_key, secret_key, url3)
        mrp = random.randint(3000,5000)
        webprice = random.randint(2000,4000)
        tokenprice = random.randint(500,1000)

        def payload():
            if sku == variantsku :
                payload = {"pricelistitems": {"pricelistitem": {"sku": sku,"variantsku":"" ,"qty": "1","mrp": mrp,"webprice": webprice,"tokenprice": tokenprice}}}
                Indata= {'MerchantId' : MerchantId, 'InputFormat' : 'application/json', 'InputData' : payload }
                d = urlencode(Indata)
                return d
            elif sku != variantsku:
                payload = {"pricelistitems": {"pricelistitem": {"sku": sku,"variantsku":variantsku ,"qty": "1","mrp": mrp,"webprice": webprice,"tokenprice": tokenprice}}}
                Indata= {'MerchantId' : MerchantId, 'InputFormat' : 'application/json', 'InputData' : payload }
                d = urlencode(Indata)
                return d
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}, data=payload())
        taskidfetch = response.json()
        TaskId1 = taskidfetch['Taskid']
        return TaskId1
        
    Taskid = PricelistAPI()   

    def PricelistTaskStatus():
        url10 = EnvUrl + 'Product/MSMQTaskDetails/'  + MerchantId +'/' + Taskid + '/Product'
        u = GET_signatureBuilder(public_key,secret_key,url10)
        response = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
        r  = response.json()
        TaskStatus = r['TaskMsmqDetails']['TaskStatus']
        return response.json()

    def LocationInfo():
        url11 = EnvUrl + 'Location/Information/'+ MerchantId + '/'+str(LocationId)
        u = GET_signatureBuilder(public_key,secret_key, url11)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/json'})
        e = response.json()
        Locationrefcode = (e['Location']['LocationCode'])
        return Locationrefcode


    def GetPrice():
        
        time.sleep(1)
        url4 = EnvUrl + 'Product/Price/' + MerchantId
        u = POST_signatureBuilder(public_key,secret_key,url4)
        f= json.dumps({"sku":variantsku, "locationrefcode": LocationInfo()})
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/json'}, data=f )
        return response.json()
    return GetPrice()
    


@application.route('/', methods=['POST'])
def post():
    return '{"Output":"Hello World"}'


if __name__ == '__main__':
    flaskrun(application)
