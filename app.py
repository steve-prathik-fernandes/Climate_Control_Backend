from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Mock AI model function (replace this with the actual AI model call)
def call_ai_model(data):
    # This is a mock function representing the AI model
    # Replace this with the actual call to your friend's AI model
    print("Data sent to AI model:", data)
    # Assuming the AI model returns a response
    return {"prediction": "some_result"}

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    try:
        # Get data from the front end (Angular)
        data = request.json
        booking_time = data.get('booking_time')
        room_temperature = data.get('room_temperature')

        # Hardcode sensor values (replace with actual values if needed)
        motion_sensor = 1  # 1 for motion detected, 0 for no motion
        co2_sensor = 450   # CO2 level in ppm
        humidity = 60      # Humidity in percentage
        temperature = 22   # Temperature in Celsius (hardcoded, but you can use room_temperature)
        room_volume = 200   # Volume of the room in cubic meters

        # Prepare the data to send to the AI model
        ai_model_input = {
            "booking_time": booking_time,
            "room_temperature": room_temperature,
            "motion_sensor": motion_sensor,
            "co2_sensor": co2_sensor,
            "humidity": humidity,
            "temperature": temperature,
            "room_volume": room_volume
        }

        # Call the AI model (replace with actual call)
        ai_model_response = call_ai_model(ai_model_input)

        # Return the AI model's response to the front end
        return jsonify({
            "status": "success",
            "message": "Data processed successfully",
            "ai_model_response": ai_model_response
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)