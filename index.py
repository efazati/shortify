"""
Install : pip install pymongo flask
Minimalistic url shortener : use with curl -sd "url=http://example.com/" http://this-app.com/shorten
"""
from flask import Flask, request, redirect, abort, render_template
import base64, md5, re

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['shortify']
col = db.urls

app = Flask(__name__)

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/shorten', methods=['post'])
def shorten() :
    url = request.form.get('url')
    if not is_valid_url(url) :
        return abort(400)
    code = base64.b64encode(md5.new(url).digest()[-4:]).replace('=','').replace('/','_')
    row = {'code' : code, 'url' : url}
    domain = col.find_one({"code": code})
    if not domain:
        id = col.insert_one(row).inserted_id
        print url, id, code
    return render_template('index.html', code=code)

@app.route('/<code>')
def redirect_page(code) :
    #url = col.find_and_modify({'code' : code}, {'$inc' : {'v' : 1}})['url']
    return
    return redirect(code)

def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

if __name__ == '__main__' :
    app.debug = True
    app.run()