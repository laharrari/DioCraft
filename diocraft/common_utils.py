import os
from dotenv import load_dotenv

load_dotenv()

discord_token = os.environ["DISCORD_TOKEN"]
server_ip = os.environ["SERVER_IP"]
server_port = os.environ["SERVER_PORT"]
server_password = os.environ["SERVER_PASSWORD"]