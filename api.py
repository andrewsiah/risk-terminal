import flask
import modules.goplus as goplus

app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/security', methods=['GET'])
def security():
    dapp_security, address_security = goplus.get_security('contracts/chains/binance-smart-chain/bep20_pools.json', 'add_bnb_usdt')
    return [dapp_security, address_security]

@app.route('/position1', methods=['GET'])
def position1():
    return "Position is fine."

app.run()