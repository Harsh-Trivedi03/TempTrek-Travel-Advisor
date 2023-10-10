
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import json
import requests

class Message(Model):
    message: str

temperature_agent = Agent(
    name="temperature_agent",
    port=8000,
    seed="temperature_secret_phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(temperature_agent.wallet.address())

# Define a dictionary to store temperature data for multiple cities
city_temperatures = {}

# Ask the user how many cities they want to track
num_cities = int(input("How many cities do you want to track? "))

for _ in range(num_cities):
    # Define the city for which you want to track the temperature
    selected_location = input("Enter the city you want to put in surveillance (or 'quit' to exit): ")

    # Check if the user wants to quit
    if selected_location.lower() == 'quit':
        break

    # Define the user's desired temperature range
    desired_min_temp = int(input("Enter your desired minimum temperature: "))
    desired_max_temp = int(input("Enter your desired maximum temperature: "))

    url = f'https://api.openweathermap.org/data/2.5/weather?q={selected_location}&appid={ENTER_API_KEY_HERE}' 
    try:
        # Send a GET request to the API
        response = requests.get(url)

        # Initialize temperature_celsius with a default value
        temperature_celsius = None
        weather_condition = None

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and print relevant weather information
            temperature_kelvin = data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15

            # Extract weather condition
            weather_condition = data['weather'][0]['description']

            # Display current temperature
            print(f"Current temperature in {selected_location}: {temperature_celsius}°C")

        else:
            print(f"Request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    # Store temperature data in the dictionary
    city_temperatures[selected_location] = {
        'desired_min_temp': desired_min_temp,
        'desired_max_temp': desired_max_temp,
        'current_temperature': temperature_celsius,
        'weather_condition': weather_condition
    }

# Import the required modules for sending WhatsApp notifications
import requests

# Define the CallMeBot WhatsApp API key......" I allow callmebot to send me messages " send this message at +34644718199
CALLMEBOT_API_KEY = 'Put_Your_CallMeBot_API_Key_Here' #here you have to enter your api key code

def send_whatsapp_notification(phone_number, message):
    try:
        # Construct the URL with phone number and message
        url = f"https://api.callmebot.com/whatsapp.php?phone={ENTER_REGISTERED_MOBILE_NUMBER_GIVEN_BY_BOT}&text={message}&apikey={CALLMEBOT_API_KEY}" 

        # Send a GET request to the CallMeBot API
        response = requests.get(url)

        if response.status_code == 200:
            print("WhatsApp notification sent successfully.")
        else:
            print(f"Failed to send WhatsApp notification. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def trigger_notification(city_name, city_data):
    current_temperature = city_data['current_temperature']
    desired_min_temp = city_data['desired_min_temp']
    desired_max_temp = city_data['desired_max_temp']
    weather_condition = city_data['weather_condition']

    # Define the message content
    message = f"Temperature in {city_name} is {current_temperature}°C.\n\n Weather: {weather_condition}\n\n"

    if current_temperature < desired_min_temp:
        message += f"Alert: Temperature is below the desired minimum ({desired_min_temp}°C).\n"
    elif current_temperature > desired_max_temp:
        message += f"Alert: Temperature is above the desired maximum ({desired_max_temp}°C).\n"

    # Generate clothing recommendations
    clothing_recommendations = generate_clothing_recommendation(city_data)
    message += "\nClothing Recommendations:\n" + '\n'.join(clothing_recommendations) + '\n\n'

    # Generate a weather poem
    weather_poem = generate_weather_poem(city_data)
    message += "\nWeather Poem:\n" + weather_poem

    # Send a WhatsApp notification
    send_whatsapp_notification('your_recipient_phone_number_here', message)

def monitor_temperature(city_name, city_data):
    current_temperature = city_data['current_temperature']
    desired_min_temp = city_data['desired_min_temp']
    desired_max_temp = city_data['desired_max_temp']

    if current_temperature is not None:
        if current_temperature < desired_min_temp:
            trigger_notification(city_name, city_data)

            return f"Temperature in {city_name} is below the desired minimum ({desired_min_temp}°C)."
        elif current_temperature > desired_max_temp:
            trigger_notification(city_name, city_data)
            return f"Temperature in {city_name} is above the desired maximum ({desired_max_temp}°C)."
        else:
            trigger_notification(city_name, city_data)
            return f"Temperature in {city_name} is within the desired range ({desired_min_temp}-{desired_max_temp}°C)."
    else:
        return f"Unable to fetch current temperature for {city_name}."

def generate_weather_poem(city_data):
    current_temperature = city_data['current_temperature']
    weather_condition = city_data['weather_condition']

    poem = ""

    if 'rain' in weather_condition:
        poem = "Raindrops fall from the gray sky,\nPattering softly, my, oh my.\nGrab an umbrella, stay dry and warm,\nNature's music, a soothing charm."
    elif current_temperature < 10:
        poem = "The air is crisp, a chilly embrace,\nA scarf and coat, it's a cool day's grace.\nEmbrace the chill, it's time to play,\nIn cozy layers, you'll keep the cold at bay."
    elif 10 <= current_temperature < 20:
        poem = "The sun is shining bright and high,\nA perfect day to reach the sky.\nGrab your shades and step outside,\nLet the warmth be your guide."
    else:
        poem = "It's a pleasant day, not too hot nor cold,\nEnjoy the weather, let your spirit unfold.\nDress just right and step out the door,\nThe world awaits, there's so much to explore."

    return poem

def generate_clothing_recommendation(city_data):
    current_temperature = city_data['current_temperature']

    recommendations = []

    if current_temperature < 10:
        recommendations.append("It's very cold. Wear a heavy coat, gloves, and a warm hat.")
    elif 10 <= current_temperature < 20:
        recommendations.append("It's cool. Consider wearing a sweater or jacket.")
    elif 20 <= current_temperature < 30:
        recommendations.append("It's pleasant. Wear light clothing.")
    else:
        recommendations.append("It's hot. Wear light and breathable clothing.")

    return recommendations

async def notify_user(ctx: Context, message):
    # Define the user's address (replace with the actual user's address)
    user_address = "agent1q2kxet3vh0scsf0sm7y2erzz33cve6tv5uk63x64upw5g68kr0chkv7hw50"

    # Create a message object with a valid model schema
    message_obj = Message(message=message)

    # Send the message to the user agent
    await ctx.send(user_address, message_obj)

@temperature_agent.on_interval(period=3600.0)  # Check every hour
async def temperature_monitor(ctx: Context):
    for city, city_data in city_temperatures.items():
        temperature_status = monitor_temperature(city, city_data)
        clothing_recommendations = generate_clothing_recommendation(city_data)
        weather_poem = generate_weather_poem(city_data)

        ctx.logger.info(temperature_status)

        ctx.logger.info("Clothing Recommendations:")
        for recommendation in clothing_recommendations:
            ctx.logger.info(recommendation)
        
        ctx.logger.info("Weather Poem:")
        ctx.logger.info(weather_poem)
        
        await notify_user(ctx, f"{temperature_status}")

if __name__ == "__main__":
    temperature_agent.run()
