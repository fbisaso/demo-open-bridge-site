from flask import Flask, render_template, request, jsonify
import json
import time
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/capi/events', methods=['POST'])
def capi_events():
    raw_data = request.get_data()  
    str_data = raw_data.decode('utf-8')
    data_bag = json.loads(str_data)

    access_token = 'EAANVvkrZCToIBAGoZBGaU8Mnob4RBacpjDZCmVmaHr3wObKMYVL4WjBGgJEKFTCjGqN1iAyUm9CLi2dHq8jPTpIe2iaQNLAcAeaKPzqpvWdG7S6NTYPI99r7Ngl1GNgFLwFqyXRexIiJ2CzuWCddE6BmZAZBuVia63EdNfEKkEINwKocfkW05POzJOtaDlKQPqIVS05CvAgZDZD'
    pixel_id = data_bag.get('fb.pixel_id')

    payload = {
        'data': [
            {
                'event_name': data_bag.get('event_name'),
                'event_time': int(time.time()),
                'event_id': data_bag.get('event_id'),
                'action_source': 'website',
                'event_source_url': data_bag['website_context']['location'],
                'user_data': {
                    'fbp': data_bag.get('fb.fbp'),
                    'client_ip_address': request.remote_addr,
                    
                },
                # 'custom_data': ... set custom data,
            }
        ],
        'test_event_code': 'TEST17310',
    }

    response = requests.post(f"https://graph.facebook.com/v15.0/{pixel_id}/events?access_token={access_token}", json=payload)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0')

