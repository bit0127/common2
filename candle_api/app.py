from chalice import Chalice, Response
import csv, os
import pytz
from datetime import datetime, timezone, timedelta
import pandas as pd

app = Chalice(app_name='candle-api')

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'chalicelib', 'order_books.csv')

JST = pytz.timezone('Asia/Tokyo')

def parse_time(time_str):
    try:
        time_str = time_str.replace(' JST', '')
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S %z')
        dt = dt.astimezone(JST)
        return dt
    except Exception as e:
        print(f"Error parsing time string: {time_str} -> {e}")
        return None

df = pd.read_csv(CSV_FILE_PATH)
df['time'] = df['time'].apply(parse_time)

@app.route('/candle', methods=['GET'])
def get_candle_data():
    code = app.current_request.query_params.get('code')
    year = int(app.current_request.query_params.get('year'))
    month = int(app.current_request.query_params.get('month'))
    day = int(app.current_request.query_params.get('day'))
    hour = int(app.current_request.query_params.get('hour'))

    if not all([code, year, month, day, hour]):
        return {'error': 'Missing required parameters'}, 400

    filtered_data = df[(df['code'] == code) & 
                        (df['time'].dt.year == year) &
                        (df['time'].dt.month == month) &
                        (df['time'].dt.day == day) &
                        (df['time'].dt.hour == hour)]

    if filtered_data.empty:
        return {'error': f"No data found for {code} on {year}-{month:02d}-{day:02d} at {hour}:00"}, 404

    open_price = filtered_data.iloc[0]['price']
    close_price = filtered_data.iloc[-1]['price']
    high_price = filtered_data['price'].max()
    low_price = filtered_data['price'].min()

    candle_data = {
        'open': int(open_price),
        'high': int(high_price),
        'low': int(low_price),
        'close': int(close_price)
    }

    return candle_data

@app.route('/flag', methods=['PUT'])
def flag():
    request = app.current_request
    try:
        body = request.json_body
        print(body)
        flag = body.get('Flag')
        if not flag:
            raise ValueError('Missing flag')

        return Response(
            body={'message': 'Flag received', 'flag': flag},
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )
    except (ValueError, KeyError):
        return Response(
            body={'error': 'Invalid request body'},
            status_code=400,
            headers={'Content-Type': 'application/json'}
        )
