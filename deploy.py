import os
import subprocess
import sys
import time
import webbrowser
import requests
import json

def download_ngrok():
    """Download ngrok if it doesn't exist"""
    if not os.path.exists("ngrok.exe"):
        print("Downloading ngrok...")
        import urllib.request
        urllib.request.urlretrieve("https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip", "ngrok.zip")
        
        # Extract ngrok
        import zipfile
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print("ngrok downloaded successfully!")
    else:
        print("ngrok already exists")

def setup_ngrok_auth():
    """Setup ngrok authentication"""
    auth_token = "2slA6lKLAgsiY96bp6WKTNStagN_7g4C1mRciLP6hWtBE87bt"  # Your ngrok auth token
    subprocess.run(["ngrok", "config", "add-authtoken", auth_token], shell=True)
    print("ngrok authentication configured")

def start_flask_server():
    """Start the Flask server in the background"""
    print("Starting Flask server...")
    flask_process = subprocess.Popen(["python", "app.py"], 
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    time.sleep(3)  # Give Flask time to start
    return flask_process

def start_ngrok_tunnel():
    """Start ngrok tunnel and return the public URL"""
    print("Starting ngrok tunnel...")
    ngrok_process = subprocess.Popen(["ngrok", "http", "5000"], 
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True)
    
    # Get the ngrok public URL
    time.sleep(3)  # Give ngrok time to start
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = json.loads(response.text)["tunnels"]
        public_url = tunnels[0]["public_url"]
        print(f"Honeypot deployed! Public URL: {public_url}")
        return ngrok_process, public_url
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        return ngrok_process, None

def main():
    """Main function to deploy the honeypot"""
    print("=== Honeypot Deployment Script ===")
    
    # Download ngrok if needed
    download_ngrok()
    
    # Setup ngrok authentication
    setup_ngrok_auth()
    
    # Start Flask server
    flask_process = start_flask_server()
    
    # Start ngrok tunnel
    ngrok_process, public_url = start_ngrok_tunnel()
    
    if public_url:
        print("\nYour honeypot is now live on the internet!")
        print(f"Public URL: {public_url}")
        print("\nShare this URL to capture attack attempts.")
        print("All login attempts and keystrokes will be logged.")
        
        # Open the URL in the default browser
        webbrowser.open(public_url)
    
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        flask_process.terminate()
        ngrok_process.terminate()
        print("Honeypot deployment stopped")

if __name__ == "__main__":
    main()
