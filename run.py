# Import required libraries
from geopy.geocoders import Nominatim
import requests
import datetime
from termcolor import colored
import readchar
import os
import time


# Define constants
BASE_URL = 'https://api.open-meteo.com/v1/forecast?'
# Define parts of the URL
LATITUDE_PART = 'latitude='
LONGITUDE_PART = '&longitude='
# Define closing part of the URL
CLOSING_PART = '&hourly=temperature_2m,relativehumidity_2m,\
precipitation_probability,surface_pressure,visibility,windspeed_10m,\
winddirection_10m,windgusts_10m&daily=temperature_2m_max,temperature_2m_min,\
sunrise,sunset,uv_index_max,\
precipitation_probability_max&windspeed_unit=ms&timezone=GMT'
BANNER_INPUT = """
.----..-. .-..----..----..-.  .-.    .---. .-.    .----. .-. .-..----.     
| {_  | | | || {_  | {}  }\ \/ /    /  ___}| |   /  {}  \| { } || {}  \   
| {__ \ \_/ /| {__ | .-. \ }  {     \     }| `--.\      /| {_} ||     /   
`----' `---' `----'`-' `-' `--'      `---' `----' `----' `-----'`----'     
.-. .-.  .--.   .----.     .--.      .----..-..-.   .-. .-..----..----.     
| {_} | / {} \ { {__      / {} \    { {__  | || |   | | | || {_  | {}  }   
| { } |/  /\  \.-._} }   /  /\  \   .-._} }| || `--.\ \_/ /| {__ | .-. \   
`-' `-'`-'  `-'`----'    `-'  `-'   `----' `-'`----' `---' `----'`-' `-'    
.-.   .-..-. .-..-..-. .-. .---. 
| |   | ||  `| || ||  `| |/   __}
| `--.| || |\  || || |\  |\  {_ }
`----'`-'`-' `-'`-'`-' `-' `---' 
"""
BANNER_INTRO = """                     					
        			
     .        .      /				
      \       |     .				
                  /
        \  ,g88R__== --__ =-
--__==-__ d888(`  ).                   _
 -  --==  888(     ).=--.--        .+(`  )`.
)         Y8P(       '`.          :(   .    )
        .+(`(      .   )     .--  `.  (    ) )
       ((    (..__.:'-'   .=(   )   ` _`  ) )
`.     `(       ) )       (   .  )     (   )  ._
  )      ` __.:'   )     (   (   ))     `-'.:(`  )
)  )  ( )       --'       `- __.'         :(      ))
.-'  (_.'          .')                    `(    )  ))
--..,___.--,--'`,---..-.--+--.,,-,,..._.--..-._.-a:f--.
"""


def key_pressed():
    """
    This function waits for a key to be pressed
    """
    print('Press any key to continue...')
    key = readchar.readkey()
    return


def clear_screen():
    """
    This function clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    return


# Defining Welcome message function
def welcome_message():
    """
    This function prints a welcome message to the user
    """
    print(colored('Welcome to Victoria\'s Weather App!'.upper(), 'green'))
    print(colored(BANNER_INTRO, 'yellow'))
    print(colored('This app will provide you with the weather \
information for the location of your choice.', 'green'))
    print(colored('In order to obtain the weather information, \
please enter the city and country.', 'yellow'))
    print(colored('Enjoy!', 'green'))


lines = BANNER_INPUT.split()

# Define name_input function


def name_input():
    """
    This function asks for the user's name
    """
    # Print banner
    for line in BANNER_INPUT.splitlines():
        for character in line:
            print(colored(character, 'yellow'), end='', flush=True)
            # delay printing of each character by 0.05 seconds
            time.sleep(.005)
        print('')  # print a new line
        time.sleep(0.5)  # delay printing of each line by 0.5 seconds

    # Ask for name
    name = input('Choose a name - it must be at least 3 characters long, but no longer than 10 characters, include only letters, no numbers or special characters: ')
    # Check if the name is valid
    while len(name) < 3 or len(name) > 10 or not name.isalpha():
        print(colored('Oops! Something went wrong. Please try again.', 'red'))
        name = input('Choose a name - it must be at least 3 characters long, but no longer than 10 characters, include only letters, no numbers or special characters: ')
    print(colored(f"Hello,{name}! {'come rain or shine'.upper()}, I wish you to be on a {'cloud nine'.upper()} and everything you do {'to be a breeze!'.upper()}", 'magenta'))
    return name


# Defining get_location function
def get_location(city, country):
    """
    This function returns a string of the form City, Country
    """
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")
    # Get location
    location = geolocator.geocode(f"{city}, {country}")
    if location is None:
        print(colored('Oops! Something went wrong. Please try again later.', 'red'))
        exit()
    # Get latitude and longitude
    latitude = str(location.latitude)
    longitude = str(location.longitude)
    return latitude, longitude


# Defining get_weather function
def get_weather(latitude, longitude):
    """
    This function returns the current weather information
    """
    global LATITUDE_PART, LONGITUDE_PART, CLOSING_PART
    # Define URL
    url = BASE_URL + LATITUDE_PART + latitude + \
        LONGITUDE_PART + longitude + CLOSING_PART

    # Get data from API
    response = requests.get(url)
    # Check if the response is successful
    # If successful, get data
    # 200 is the HTTP status code for "OK" used for data communication \
    # on the web (https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
    if response.status_code == 200:
        # Print success message
        print(colored('Success! Everything is okay. I got the data!', 'blue'))
        # Get data
        data = response.json()
        # Get current date
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None if the response is enything other then successful
        data = None
    return data


# Defining print_weather function
def print_weather(data):
    """
    This function prints the weather information
    """
    # calculate index for current hour and current date
    now = str(datetime.datetime.now()).split()
    now_time = now[0] + 'T' + now[1][:2] + ':00'
    hourly_index = data['hourly']['time'].index(now_time)
    daily_index = data['daily']['time'].index(
        str(datetime.datetime.now()).split()[0])

    if data is not None:
        # Hourly requests
        # Get current temperature
        current_temperature = data['hourly']['temperature_2m'][hourly_index]
        # Get current humidity
        current_humidity = data['hourly']['relativehumidity_2m'][hourly_index]
        # Get current precipitation probability
        current_precipitation_probability = data['hourly'][
            'precipitation_probability'][hourly_index]
        # Get current pressure
        current_pressure = data['hourly']['surface_pressure'][hourly_index]
        # Get current visibility
        current_visibility = data['hourly']['visibility'][hourly_index]
        # Get curreent windspeed
        current_windspeed = data['hourly']['windspeed_10m'][hourly_index]
        # Get current wind direction
        current_winddirection = data['hourly'][
            'winddirection_10m'][hourly_index]
        # Get current wind gusts
        current_windgusts = data['hourly']['windgusts_10m'][hourly_index]

        # Daily requests
        # Get current maximum temperature
        current_temperature_max = data['daily'][
            'temperature_2m_max'][daily_index]
        # Get current minimum temperature
        current_temperature_min = data['daily'][
            'temperature_2m_min'][daily_index]
        # Get current sunrise
        current_sunrise = data['daily']['sunrise'][daily_index]
        # Get current sunset
        current_sunset = data['daily']['sunset'][daily_index]
        # Get current UV index
        current_uv_index = data['daily']['uv_index_max'][daily_index]
        # Get current precipitation probability
        current_precipitation_probability = data['daily'][
            'precipitation_probability_max'][daily_index]

        # Print hourly requests
        # Print current temperature
        print(
            f"The current temperature is {current_temperature}\u00b0 C")
        # Print current humidity
        print(f"The current relative humidity is {current_humidity} %")
        # Print current precipitation probability
        print(
            f"The current precipitation probability is {current_precipitation_probability} %")
        # Print current surface pressure
        print(f"The current surface pressure is {current_pressure} hPa")
        # Print current visibility
        print(f"The current visibility is {current_visibility} km")
        # Print current windspeed
        print(f"The current windspeed is {current_windspeed} m/s")
        # Print current wind direction
        print(f"The current wind direction is {current_winddirection}")
        # Print current wind gusts
        print(f"The current wind gusts are {current_windgusts} m/s")

        # Print daily requests
        # Print daily maximum temperature
        print(
            f"The daily maximum temperature is {current_temperature_max}\u00b0 C")
        # Print daily minimum temperature
        print(
            f"The daily minimum temperature is {current_temperature_min}\u00b0 C")
        # Print sunrise
        print(f"The sunrise is at {current_sunrise}")
        # Print sunset
        print(f"The sunset is at {current_sunset}")
        # Print UV index
        print(f"The UV index is {current_uv_index}")
        # Print precipitation probability
        print(
            f"The maximum daily precipitation probability is {current_precipitation_probability} %")
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None if the response is enything other then successful
        data = None


def main():
    # Call welcome message function
    welcome_message()
    # Call key_pressed function
    key_pressed()
    # Call clear_screen function
    clear_screen()
    # Call name_input function
    name = name_input()
    key_pressed()
    clear_screen()
    # Ask for city and country
    city = input('City: ')
    country = input('Country: ')
    # Call get_location function
    latitude, longitude = get_location(city, country)
    # Call get_weather function
    data = get_weather(latitude, longitude)

    print(f"You have entered the following location: {city}, {country}")
    print('Please wait while I am getting the weather information for you...')
    print('This may take a few seconds...')
    print('Thank you for your patience!')
    print(
        colored(f'Here is the weather information for {city}, {country}:', 'cyan'))
    print_weather(data)


if __name__ == '__main__':
    main()
