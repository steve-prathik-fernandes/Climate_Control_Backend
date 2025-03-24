import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import numpy as np
import joblib  

app = Flask(__name__)
CORS(app)


def load_hvac_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise ValueError("Model file not found. Ensure 'hvac_model.joblib' exists in the specified path.")

def call_ai_model(ai_input):
    model = load_hvac_model("hvac_model.joblib")
    

    processed_input = np.array([
        ai_input["inside_temp"],
        ai_input["outside_temp"],
        ai_input["room_volume"]
    ]).reshape(1, -1)
    
    predict_time = model.predict(processed_input)
    return predict_time[0] 


def parse_book_time(book_time):
    if isinstance(book_time, int):
        return book_time 
    elif isinstance(book_time, str):
        try:
           
            return int(book_time.split(':')[0])
        except (ValueError, IndexError):
            raise ValueError("Invalid book_time format. Expected integer or 'HH:MM' string.")
    else:
        raise ValueError("book_time must be an integer or string in 'HH:MM' format.")


def add_minutes_to_time(book_time_hour, minutes_to_add):
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    original_time = base_date + timedelta(hours=book_time_hour)
    

    new_time = original_time + timedelta(minutes=minutes_to_add)
 
    new_time_str = new_time.strftime("%H:%M")
    
    return new_time_str

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    try:
        data = request.json
        book_time_raw = data.get('book_time') 
        book_time = parse_book_time(book_time_raw) 
        outside_temp = float(data.get('temperature'))  
        diff_time = float(data.get('diff_time'))  
        room_name = data.get('room') 

        inside_temp = round(random.uniform(60, 62), 4)
        room_volume = 1000  

        ai_model_input = {
            "inside_temp": inside_temp,
            "outside_temp": outside_temp,
            "room_volume": room_volume
        }

        ai_time = float(call_ai_model(ai_model_input)) 
        calc_time =  diff_time - ai_time
        new_time = add_minutes_to_time(book_time, calc_time)

        if(calc_time<0):
              calc_time=None
        

      
        original_book_time = f"{book_time}:00"

        return jsonify({
            "status": "success",
            "message": "Data processed successfully",
            "room": room_name,
            "original_book_time": original_book_time,
            "ai_model_response": ai_time,
            "inside_temp": inside_temp,
            "calculated_time_adjustment": calc_time
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 