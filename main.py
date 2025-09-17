import os
import time
import pyotp
import requests
import logging
from dotenv import load_dotenv

# ======================
# SmartAPI imports
# ======================
try:
    from smartapi import SmartConnect
except ModuleNotFoundError:
    print("❌ Missing SmartAPI package. Please install 'smartapi-python'.")
    raise

# check Twisted early for clear error
try:
    import twisted
except ModuleNotFoundError:
    print("❌ Missing 'twisted' (required for SmartAPI websockets). Add twisted, autobahn, service-identity to requirements.txt.")
    raise

# ======================
# Load environment
# ======================
load_dotenv()

SMARTAPI_API_KEY = os.getenv("SMARTAPI_API_KEY")
SMARTAPI_CLIENT_ID = os.getenv("SMARTAPI_CLIENT_ID")
SMARTAPI_CLIENT_PWD = os.getenv("SMARTAPI_CLIENT_PWD")
SMARTAPI_TOTP_SECRET = os.getenv("SMARTAPI_TOTP_SECRET")

if not SMARTAPI_API_KEY or not SMARTAPI_CLIENT_ID or not SMARTAPI_CLIENT_PWD or not SMARTAPI_TOTP_SECRET:
    raise ValueError("❌ SmartAPI credentials incomplete. Check your .env values.")

# ======================
# SmartAPI login
# ======================
try:
    s = SmartConnect(api_key=SMARTAPI_API_KEY)
except TypeError:
    try:
        s = SmartConnect(SMARTAPI_API_KEY)
    except Exception as e:
        print("❌ SmartConnect init failed:", e)
        raise

# Generate OTP
totp = pyotp.TOTP(SMARTAPI_TOTP_SECRET).now()
print("[SmartAPI] Trying OTP:", totp)

try:
    data = s.generateSession(SMARTAPI_CLIENT_ID, SMARTAPI_CLIENT_PWD, totp)
    print("✅ Login successful")
except Exception as e:
    print("❌ Login failed:", e)
    raise

# ======================
# Add your further logic below (market data, orders, etc.)
# ======================

