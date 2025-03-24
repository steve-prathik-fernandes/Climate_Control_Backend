import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

#calling ai model
def call_ai_model(ai_input):

    print("Data sent to AI model:", ai_input)
    # Assuming the AI model returns a response

    predict_time=20
    return predict_time

#adding minutes to the booking time 
def add_minutes_to_time(time_str, minutes_to_add):
    # Convert the input time string to a datetime object
    time_format = "%H:%M"
    original_time = datetime.strptime(time_str, time_format)
    
    # Add the specified minutes
    new_time = original_time + timedelta(minutes=minutes_to_add)
    
    # Convert the new time back to a string in 24-hour format
    new_time_str = new_time.strftime(time_format)
    
    return new_time_str

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    try:
        # Get data from the front end (Angular)
        data = request.json
        booking_time = data.get('booking_time')
        outside_temp = data.get('outside_temp')
        diff_time=data.get('diff_time')

        
        inside_temp =round(random.uniform(60, 62), 4)   # Temperature in Fahreinheit
        room_volume = [500,1000,1500]  # Volume of the rooms

        # Prepare the data to send to the AI model
        ai_model_input = {
            "inside_temp": inside_temp,
            "outside_temp": outside_temp,
            "room_volume": room_volume
        }

        # Call the AI model (replace with actual call)
        ai_time = call_ai_model(ai_model_input)

        calc_time=ai_time-diff_time

        new_time=add_minutes_to_time(booking_time,calc_time) 


        # Return the AI model's response to the front end
        return jsonify({
            "status": "success",
            "message": "Data processed successfully",
            "ai_model_response": new_time
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
    