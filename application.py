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

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    
    MerchantId = "f48fdd16-92db-4188-854d-1ecd9b62d066"
    public_key = "K5DYSCRC"
    secret_key = "WHPT74UEQUYRZ33GUSBI7MGU"
    EnvUrl = "http://www.testln.martjack.com/devapi/"
    Staging = "http://www.stageln.martjack.com/devapi"
    ProdEnv = "http://www.martjack.com/devapi" 
    
    host = "poshlette.cnauabwc9dbm.us-east-1.rds.amazonaws.com"
    port = "3306"
    user = "sandieps"
    password = "Sandie0713"
    database = "PoshCorp"

    mrp = random.randint(2000,5000)
    webprice = random.randint(1000,4000)
    tokenprice = random.randint(500,1000)

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
    
    def GetCategoryproducts():
        url5 = EnvUrl + 'Category/' + MerchantId + '/NA'
        u = GET_signatureBuilder(public_key,secret_key,url5)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
        categories = response.json()
        categoryid = (categories['Categories'][0]['CategoryId'])
        url6 = EnvUrl + 'Product/Category/' + MerchantId + '/'+categoryid
        u = GET_signatureBuilder(public_key,secret_key,url6)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
        r = response.json()
        if r['Message'] == "No Record Found":
            categoryid = (categories['Categories'][1]['CategoryId'])
            url6 = EnvUrl + 'Product/Category/' + MerchantId + '/'+categoryid
            u = GET_signatureBuilder(public_key,secret_key,url6)
            response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
            r2 = response.json()
            return r2
        elif r['Message'] == "No Record Found":
            categoryid = (categories['Categories'][2]['CategoryId'])
            url6 = EnvUrl + 'Product/Category/' + MerchantId + '/'+categoryids
            u = GET_signatureBuilder(public_key,secret_key,url6)
            response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
            r3 = response.json()
            return r3
        else:
            return "yes"
            
    def Getpricelists():
        u = GET_signatureBuilder(public_key, secret_key, url)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'})
        Getpricelists = response.json()
        PricelistRefcode = (Getpricelists["PriceListDetails"][3]["ReferenceCode"])
        LocationId = (Getpricelists["PriceListDetails"][3]["LocationId"])
        return PricelistRefcode, LocationId
    
    def Products():
        url7 = EnvUrl + 'Product/' + MerchantId + '/Search'
        u = POST_signatureBuilder(public_key,secret_key,url7)
        params  = {'Merchantid' : MerchantId}
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}, data=params)
        a = response.json()
        i = 0
        productId = (a['ProductIds'][i+1])
        pricelistrefcode, locationId = Getpricelists()
        url8 = EnvUrl + 'Product/Information/' + MerchantId +'/' +productId +  '/' + str(locationId)
        u = GET_signatureBuilder(public_key,secret_key,url8)
        response2 = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
        skufetch = response2.json()
        sku = skufetch['Product']['SKU']
        return response2.json(), sku, productId
        
    def variantproducts():
        r, sku,pid = Products()
        if (r['Product']['IsParentProduct']) == True:
            url9 = EnvUrl + 'Product/Varients/' + MerchantId +'/' + pid + '/ALL'
            u = GET_signatureBuilder(public_key,secret_key,url9)
            response3 = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
            variantskufetch = response3.json()
            variantsku = variantskufetch['ProductVarient'][0]['SKU'] 
            return variantsku
        elif (r['Product']['IsParentProduct']) == False:
            return sku
        
    def PricelistAPI():
        p,l = Getpricelists()
        url3 = EnvUrl + 'Pricelist/' + MerchantId +  '/' + p + "/upload"
        u = POST_signatureBuilder(public_key, secret_key, url3)
        r, sku,pid = Products()
        variantsku = variantproducts()
        mrp = "4990"
        webprice = "3990"
        def payload():
            if variantproducts() == sku:
                payload = {"pricelistitems": {"pricelistitem": {"sku": sku,"variantsku":"" ,"qty": "1","mrp": mrp,"webprice": webprice,"tokenprice": tokenprice}}}
                Indata= {'MerchantId' : MerchantId, 'InputFormat' : 'application/json', 'InputData' : payload }
                d = urlencode(Indata)
                return d
            elif variantproducts() == variantsku:
                payload = {"pricelistitems": {"pricelistitem": {"sku": sku,"variantsku":variantsku ,"qty": "1","mrp": mrp,"webprice": webprice,"tokenprice": tokenprice}}}
                Indata= {'MerchantId' : MerchantId, 'InputFormat' : 'application/json', 'InputData' : payload }
                d = urlencode(Indata)
                return d
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}, data=payload())
        taskidfetch = response.json()
        TaskId = taskidfetch['Taskid']
        return TaskId
        
            
    def PricelistTaskStatus():
        Taskid = PricelistAPI()
        url10 = EnvUrl + 'Product/MSMQTaskDetails/'  + MerchantId +'/' + Taskid + '/Product'
        u = GET_signatureBuilder(public_key,secret_key,url10)
        response = requests.get(u,headers = {'accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'} )
        r  = response.json()
        TaskStatus = r['TaskMsmqDetails']['TaskStatus']
        return response.json()

    def LocationInfo():
        locationId = l
        url11 = EnvUrl + 'Location/Information/'+ MerchantId + '/'+str(locationId)
        u = GET_signatureBuilder(public_key,secret_key, url11)
        response = requests.get(u, headers = {'accept':'application/json', 'Content-Type':'application/json'})
        e = response.json()
        Locationrefcode = (e['Location']['LocationCode'])
        return Locationrefcode

    def GetPrice():
        r  = PricelistTaskStatus()
        time.sleep(60)
        url4 = EnvUrl + 'Product/Price/' + MerchantId
        u = POST_signatureBuilder(public_key,secret_key,url4)
        variantsku = sku
        f= json.dumps({"sku":variantsku, "locationrefcode": LocationInfo()})
        response = requests.post(u, headers = {'accept':'application/json', 'Content-Type':'application/json'}, data=f )
        return response.json()
    
    g = GetPrice()
    mrp_posted = (g['CurrentPrice'][0]['mrp'])
    webprice_posted = (g['CurrentPrice'][0]['webprice'])
    if mrp != mrp_posted and webprice != webprice_posted:
        return "DCN is not active"
    elif mrp == mrp_posted and webprice == webprice_posted:
        return "DCN is active"


@application.route('/', methods=['POST'])
def post():
    return '{"Output":"Hello World"}'


if __name__ == '__main__':
    flaskrun(application)
