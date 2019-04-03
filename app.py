import flask
import os
from flask import jsonify, request
from flask import flash, redirect, url_for, session
from joblib import load
from flask_cors import CORS, cross_origin
import requests, json
import pandas as pd
import requests



predictions = pd.read_csv("predictionApi.csv")
prof = pd.read_csv("profileApi.csv")
prof.set_index('userID', inplace=True)



app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'super secret key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})







@app.route('/test', methods=['GET','POST'])
def test():
    print(prof.head())
    data = [ 1 , 2 , "Buckle My Shoe" , 3 , 4 , "Shut the Door" ]
    return jsonify( data )







@app.route('/predict', methods=['GET'])
def predict():

    # print( json.dumps( request.json['data'] ) )

    try :
        print("hi")

        user = request.args.get('user')
        userData = ( prof.loc[user , :].to_json() )
        userData = json.loads(userData.replace("\'", '"'))

        hotelList = predictions[user]
        # print(hotelList.values)
        arr = ( hotelList.sort_values(ascending=False)[:10].values )
        
        hotels = {}

        for i,a in enumerate(arr):
            
            hotels[i] = a
        
        print(hotels)

        return jsonify( { "userData" : userData, "hotels" : hotels , "status"  : True } )

    except Exception as e:
        return jsonify( { "result" : "error" , "status"  : False  } )      





@app.route('/', methods=['GET'])
def home():
    print("loaded")
    return "Welcome to My API"




if __name__ == '__main__':
    app.run()
