from flask import Flask, request, jsonify, json
import csv
import uuid
import os
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

def returndata():
    data = []
    with open('REAL_ESTATE.csv','r') as f:
        reader = csv.DictReader(f)
        for records in reader:
            data.append(records)
        return json.dumps(data)

@app.route('/properties', methods=["GET"])
def testget():
    return returndata, 200


@app.route('/properties', methods=["PUT"])
def testput():
    data = request.get_json()
    isFound = False
    isTypeMismatch = not(data['propertyName'] and data['area'] and data['price'] and data['price'] > 0 and data['gym'] and data['gym'] >= 0 and data['pool'] and data['pool'] >= 0 and data['playArea'] and data['playArea'] > 0 and data['clubHouse'] and data['clubHouse'] >= 0 and data['areaSize'] and data['areaSize'] >= 0)
    with open('REAL_ESTATE.csv', 'r') as file:
        reader = csv.DictReader(file)
        for records in reader:
            if records['propertyName'] == data['propertyName'] and data['propertyName']:
                isFound = True
    if isTypeMismatch:
       return jsonify({"error": "Please check your input and try again"}), 400
    elif isFound:
       return jsonify({"error": "Property already exists"}), 400
    else:
        csvData = [uuid.uuid4(), data['propertyName'], data['price'], data['area'], data['areaSize'], data['pool'], data['gym'], data['playArea'], data['clubHouse']]
        with open('REAL_ESTATE.csv', 'a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow(csvData)
        return data, 201

@app.route('/properties/<string:propertyId>', methods=["DELETE"])
def testdelete(propertyId):
    isFound = False
    with open('REAL_ESTATE.csv', 'r') as file:
        with open('NEW_FILE.csv', 'w', newline='\n') as f:
            reader = csv.DictReader(file)
            writer = csv.writer(f)
            writer.writerow(['propertyId', 'propertyName', 'price', 'area', 'areaSize', 'pool', 'gym', 'playArea', 'clubHouse'])
            for records in reader:
                if records['propertyId'] != propertyId:
                    writer.writerow([records['propertyId'], records['propertyName'], records['price'], records['area'], records['areaSize'], records['pool'], records['gym'], records['playArea'], records['clubHouse']])
                else:
                    isFound = True
    if isFound:
        os.remove('REAL_ESTATE.csv')
        os.rename('NEW_FILE.csv', 'REAL_ESTATE.csv')
        return jsonify({"deleted": True}), 204
    else:
        return jsonify({"error": "Property not found"}), 404

if __name__=="__main__":
    app.run(debug=True)

