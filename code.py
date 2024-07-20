# MAC Price API
from bs4 import BeautifulSoup
import requests
from code3 import *
from pandas import DataFrame as DF
from flask import Flask, jsonify
import json

data = requests.get(url_mac)
soup = BeautifulSoup(data.content, 'html5lib')
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# all_details = "arr"
def get_details():
    global all_details, names, max_price, max_name, max_pic, min_price, min_name, min_pic

    names = [x.text for x in soup.findAll('div', attrs={'class': "KzDlHZ"})]
    pics = [x['src'] for x in soup.findAll('img', attrs={'class': 'DByuf4'})][0:len(names)]
    price = [int(str(x.text).replace(",", "")[1::]) for x in soup.findAll('div', attrs={'class':'Nx9bqj _4b5DiR'})]

    df = DF({
        "NAME":names,
        "PRICE":price,
        "PIC":pics
    })
    df.to_excel("mm.xlsx")
    all_details = json.loads(df.to_json())
    mp = max(price)
    minp= min(price)
    max_price, max_name, max_pic = mp, names[price.index(mp)], pics[price.index(mp)]
    min_price, min_name, min_pic = minp, names[price.index(minp)], pics[price.index(minp)]

@app.route("/")
def home():
    data = {"/all": "All price data", "/max": "Maximum Price data", "/min": "Minimum Price data"}
    return jsonify(data)

@app.route("/all")
def alldata():
    return jsonify(all_details)

@app.route(r"/max")
def maxdata():
    data = {
        "NAME": max_name,
        "PRICE": max_price,
        "PIC": max_pic
    }
    return jsonify(data)

@app.route(r"/min")
def mindata():
    data = {
        "NAME": min_name,
        "PRICE": min_price,
        "PIC": min_pic
    }
    return jsonify(data)

if __name__ == '__main__':
    # app.run()
    get_details()
    app.run(debug=True)
