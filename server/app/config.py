import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv('EMAIL')

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "https://rulkimi.github.io",
<<<<<<< HEAD
    "http://bus-location-tracker.rulkimi.com",
    "https://bus-location-tracker.rulkimi.com",
    "https://bus-location-server-pi.vercel.app",
=======
    "https://bus-location-tracker.rulkimi.com"
>>>>>>> 9559aa5 (fix: add email .env.example and for rulkimi origin)
]
