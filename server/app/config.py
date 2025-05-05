import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv('EMAIL')

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "https://rulkimi.github.io",
    "http://bus-location-tracker.rulkimi.com",
    "https://bus-location-tracker.rulkimi.com",
    "https://bus-location-server-pi.vercel.app",
]
