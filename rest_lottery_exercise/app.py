import os
from flask import Flask, request
import pandas as pd
from flask import jsonify

app = Flask(__name__)

data = None
data = pd.read_csv('input/powerball_winning_numbers.csv'), parse_dates=['Draw Date'])
data['Winning Numbers'] = [[int(num) for num in row.split(' ')] for row in df['Winning Numbers']]
        
@app.route('/winning_number/date/{start_date}', methods=['GET'])
def winning_numbers_for_date(start_date):
    return data.loc[(data['Draw Date'] == start_date)]

@app.route('/winning_number/date/{start_date}/{end_date}', methods=['GET'])
def winning_numbers_for_dates(start_date, end_date):
    return data.loc[(data['Draw Date'] >= start_date) & (data['Draw Date'] <= end_date)]

@app.route('/multiplier/{multiplier}', methods=['GET'])
def winning_numbers_with_multiplier(multiplier):
    df = data[data['Multiplier'] == multiplier]
    return df.to_csv(columns=['Draw Date', 'Winning Numbers', 'Multiplier'])

@app.route('/winning_number/date/{start_date}/{end_date}', methods=['GET'])
def highest_sum(start_date, end_date):
    req_data = data.loc[(data['Draw Date'] >= start_date) & (data['Draw Date'] <= end_date)]
    max_sum = 0
    req_details = None
    for index, row in req_data.iterrows():
        if sum(row['Winning Numbers']) > max_sum:
            req_details = row['Draw Date']
    return req_details            

if __name__ == '__main__':
    app.run(debug=True)
