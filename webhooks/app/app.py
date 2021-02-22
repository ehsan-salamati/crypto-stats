from flask import Flask, escape, request
from flask.ext.mongoalchemy import MongoAlchemy
import logging
import json
import os
import uuid

app = Flask(__name__)
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
print(f"os.environ['MONGODB_DATABASE'] is {os.environ['MONGODB_DATABASE']}")

app.config['MONGOALCHEMY_DATABASE'] = os.environ['MONGODB_DATABASE']
db = MongoAlchemy(app)
logging.basicConfig(level=logging.DEBUG)


class IndicatorsEntity(db.Document):
    unique_hash = db.StringField()
    exchange = db.StringField()
    market = db.StringField()
    indicator = db.StringField()
    candle_period = db.StringField()
    creation_date = db.StringField()
    json_message = db.StringField()


@app.route('/health-check')
def health_check():
    return "Alive!"


@app.route('/crypto-signal', methods=['POST'])
def crypto_signal():
    app.logger.info(f'Request form is: , {request.form}!')
    request_body = request.form
    values = json.loads(request_body['messages'])
    app.logger.info(f'values[0]["exchange"] is: , {values[0]["exchange"]}!')
    # seems like there is only one
    if len(values) > 0:
        value = values[0]
        analysis_config = value["analysis"]["config"]
        print(f'analysis_config {analysis_config}')
        # TODO: Probably the hash should be sent from the crypto-signal
        indicator = IndicatorsEntity(unique_hash=str(uuid.uuid4()), exchange=value["exchange"], market=value["market"],
                                     indicator=value["indicator"], candle_period=analysis_config["candle_period"],
                                     creation_date=value["creation_date"], json_message=str(value))
        indicator.save()
    return "Success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
