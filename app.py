import apiai
import json
import requests
import random
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__, static_url_path="/static")
# Routing
@app.route('/message', methods=['POST'])


def reply():
    return jsonify({'text': execution(request.form['msg'])})

@app.route("/")
def index():
    return render_template("index.html")

#print apiai.__version__
CLIENT_ACCESS_TOKEN='c7282454a8834c65800d5775530d58c8'
ram=None
core=None
screen=None

def handle_query(query,sessionId):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    req = ai.text_request()

    req.lang = 'en'
    req.query = query
    req.session_id=sessionId
    response = req.getresponse()
    #print json.loads(response.read())
    return json.loads(response.read())


def saveParam(param):
    ram=param['ram_size']
    core=param['core']
    screen=param['screen_size']
    return ram,core,screen


def searchCata(ram,core,screen):
    l_price=float(price)-1000

    r_url='http://localhost:8000/about/?brand='+brand+'&price='+str(l_price)+'-'+price
    r=requests.get(r_url)

    if r.text:
        res=json.loads(r.text)
        #print res
        return ['model\t'+' price']+[t['title']+'\t'+str(t['mrp']) for t in res[:3]]
    else:
        return ['Sorry we dont have such a mobile']

def execution(input):
    #user_input = ''
#    cata_flag=True
   #loop the queries to API.AI so we can have a conversation client-side
    sessionId=random.randint(1, 10)
    global ram,screen,core
    # while input != 'exit':
    #     #user_input = raw_input("me: ")
    #     if input == 'exit':
    #         break
    #         # query the console with the user input, retrieve the response
    if not ram or not screen or not core:
        response = handle_query(input, sessionId)
        # parse the response
        # print response
        result = response['result']
        fulfillment = result['fulfillment']

        bot = fulfillment['speech']

        # if an action is deteted, fire the appropriate function
        if result['action'] == 'laptop_buy':
            ram, core, screen = saveParam(result['parameters'])
            # print ram,core,screen
            # if ram and core and screen:
            # print searchCata(ram,core,screen)
    return bot


# start app
if (__name__ == "__main__"):
    app.run(port = 5000)
