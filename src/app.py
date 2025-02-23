# app.py
import gradio as gr
import openai
import boto3
import json
import os
import requests
from urllib.parse import urlencode, parse_qs, urlparse
from pycognito import Cognito
from typing import Optional, Dict, Any
import sys 
import logging


# Create logger
logger = logging.getLogger(__name__)

# Configure Gradio specific logger
gradio_logger = logging.getLogger("gradio")
gradio_logger.setLevel(logging.INFO)
gradio_logger.addHandler(logging.StreamHandler(sys.stdout))

# Get configuration from environment variables
USER_POOL_ID = os.environ['COGNITO_USER_POOL_ID']
CLIENT_ID = os.environ['COGNITO_CLIENT_ID']
REDIRECT_URI = os.environ['COGNITO_REDIRECT_URI']
COGNITO_DOMAIN = os.environ['COGNITO_DOMAIN']
APPLICATION_URL = os.environ['APPLICATION_URL']
AWS_REGION = os.environ['AWS_DEFAULT_REGION']

class CognitoAuthenticator:
    def __init__(self):
        self.user_pool_id = USER_POOL_ID
        self.client_id = CLIENT_ID
        self.pool_region = AWS_REGION

    def verify_token(self, token: str) -> bool:
        """Verify the JWT token using pycognito"""
        try:
            u = Cognito(
                user_pool_id=self.user_pool_id,
                client_id=self.client_id,
                user_pool_region=self.pool_region,
                id_token=token.get('id_token'),
                access_token=token.get('access_token')
            )
            # # Verify the token - specify 'id' as the token_use
            # ==print(f"Token is {token}")
            u.check_token()  # Optional, if you want to maybe renew the tokens
            #u.verify_token(token.get('id_token').encode('utf-8'), 'id_token', 'id')  # Required, this will verify the token
            return True
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return False

def get_secret():
    """Retrieve OpenAI API key from AWS Secrets Manager"""
    if os.getenv("APP_ENVIRONMENT") == "local":
        logger.info("Local environment")
        return os.getenv("CHATGPT_KEY")
    
    session = boto3.session.Session()
    client = session.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=os.getenv("CHATGPT_KEYNAME"))
        return response['SecretString']
        #return json.loads(response['SecretString'])['OPENAI_API_KEY']
    except Exception as e:
        logger.error(f"Error retrieving secret: {str(e)}")
        raise

def get_login_url():
    """Generate Cognito hosted UI login URL"""
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'email openid',
        'redirect_uri': REDIRECT_URI
    }
    return f"{COGNITO_DOMAIN}/login?{urlencode(params)}"

def exchange_code_for_tokens(code: str) -> Optional[Dict[str, Any]]:
    """Exchange authorization code for tokens"""
    token_endpoint = f"{COGNITO_DOMAIN}/oauth2/token"
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    try:
        response = requests.post(token_endpoint, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Token exchange failed: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error exchanging code for tokens: {str(e)}")
        return None

def get_coordinates(location):
    """Fetch latitude and longitude for a given location using Open-Meteo Geocoding API."""
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
        else:
            raise ValueError("Location not found.")
    else:
        raise Exception("Failed to fetch coordinates.")

def get_weather_from_coordinates(latitude, longitude):
    """Fetch weather forecast for a given latitude and longitude using Open-Meteo API."""
    weather_url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": ["temperature_2m", "relative_humidity_2m"],
        "timezone": "auto"
    }
    response = requests.get(weather_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch weather data.")
    
def get_weather(location: str) -> str:
    """Get weather for a location using a weather API"""
    try:
        logger.info(f"Location to be passed to get_coordinates: {location}")
        latitude, longitude = get_coordinates(location)
        logger.info(f"Coordinates for location {location} are {latitude}:{longitude}")
        weather_data = get_weather_from_coordinates(latitude, longitude)
        logger.info("Current Weather:")
        logger.info(weather_data.get("current_weather", {}))
        
        # return f"The current temperature in {location} is {weather_data.get('current_weather').get('temperature')}°C"
        return f"The current temperature in {location} is {weather_data.get('current_weather')}°C"
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Unable to fetch weather data"
    
        

# Available tools definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a location which is a City",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Only city location"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def process_message(message: str, token: str) -> str:
    """Process message using OpenAI API with tools"""
    auth = CognitoAuthenticator()
    if not auth.verify_token(token):
        return "Authentication required"
    
    try:
        openai.api_key = get_secret()
        
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": "You are an AI assistant who have knowledge of weather updates and humour sense."},
                {"role": "user", "content": message}],
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        tool_responses = []

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_weather":
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = get_weather(function_args["location"])
                    
                    tool_responses.append(    {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": function_response
                        })
                    #]
                    
            second_response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                        {"role": "user", "content": message},
                        response_message,  # Original response message
                        *tool_responses  # Include responses for each tool call
                    ],
            )
            return second_response.choices[0].message.content
        
        return response_message.content
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return f"An error occurred: {str(e)}"

# Gradio interface
def create_interface():
    """Create Gradio interface"""

    def handle_oauth_callback(code):
        """Handle OAuth callback and exchange code for tokens"""
        if code:
            tokens = exchange_code_for_tokens(code)
            if tokens:
                return tokens #tokens.get('id_token')
        return None

    with gr.Blocks() as demo:
        gr.Markdown("# OpenAI Tools Chat Interface")
        
        # Authentication state
        token = gr.State(None)
        auth_html = gr.HTML()
        
        with gr.Row():
            login_btn = gr.HTML(f"""
    <div>
        <a href="{get_login_url()}" target="_self" 
           style="display:inline-block; padding:10px 15px; 
                  background-color:#2196F3; color:white; 
                  text-decoration:none; border-radius:4px;
                  min-width: 200px; text-align: center; display: inline-block;">
           Login with Cognito
        </a>
    </div>
""")

            
            logout_btn = gr.Button("Logout")
        
        chatbot = gr.Chatbot(visible=False)
        msg = gr.Textbox(visible=False, placeholder="Type your message here...")
        clear = gr.Button("Clear", visible=False)

        def show_chat_interface(token_value):
            """Show/hide chat interface based on authentication state"""
            if token_value:
                return {
                    chatbot: gr.update(visible=True),
                    msg: gr.update(visible=True),
                    clear: gr.update(visible=True),
                    login_btn: gr.update(visible=False)
                }
            return {
                chatbot: gr.update(visible=False),
                msg: gr.update(visible=False),
                clear: gr.update(visible=False),
                login_btn: gr.update(visible=True)
            }

        def logout():
            """Handle logout"""
            return {
                token: None,
                chatbot: gr.update(visible=False),
                msg: gr.update(visible=False),
                clear: gr.update(visible=False),
                login_btn: gr.update(visible=True)
            }

        def respond(message, chat_history, token):
            """Handle chat messages"""
            if not token:
                return chat_history + [["Please login first", ""]]
            
            bot_message = process_message(message, token)
            chat_history.append((message, bot_message))
            return "", chat_history


        token.change(show_chat_interface, token, [chatbot, msg, clear, login_btn])
        logout_btn.click(logout, None, [token, chatbot, msg, clear, login_btn])
        msg.submit(respond, [msg, chatbot, token], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

        # Check for authorization code on page load
        def check_auth(request: gr.Request):
            """Check for authorization code in URL"""
            parsed_url = urlparse(request.headers.get('referer', ''))
            query_params = parse_qs(parsed_url.query)
            if 'code' in query_params:
                code = query_params['code'][0]
                return handle_oauth_callback(code)
            return None

        demo.load(check_auth, outputs=[token])

    return demo

if __name__ == "__main__":
    # Force stdout to flush immediately
    sys.stdout.reconfigure(line_buffering=True)

    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=80)