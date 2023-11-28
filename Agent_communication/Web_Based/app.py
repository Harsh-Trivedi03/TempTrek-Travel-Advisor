from flask import Flask, render_template, request, redirect, url_for
from temperature_agent import send_user_input_to_temperature_agent

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        num_cities = int(request.form['num_cities'])
        city_data = []

        for i in range(1, num_cities + 1):
            city_name = request.form[f'city_name_{i}']
            min_temp = int(request.form[f'min_temp_{i}'])
            max_temp = int(request.form[f'max_temp_{i}'])

            city_data.append({
                'city': city_name,
                'min_temp': min_temp,
                'max_temp': max_temp
            })

        # Forward the user input to the Temperature Agent
        for data in city_data:
            # print("sending data to temperature agent")
            send_user_input_to_temperature_agent(data['city'], data['min_temp'], data['max_temp'])

        # Redirect to a confirmation page or display a message
        return "Updates Sent to Telegram..."

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

