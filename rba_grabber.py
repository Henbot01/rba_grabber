import requests
from datetime import datetime, timezone
import os
import configparser

# Load configuration from config.ini
def load_config(config_file="config.ini"):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

def download_rba_file(config_file="config.ini"):
    # Load configuration
    config = load_config(config_file)
    if not config:
        print("Configuration not loaded. Exiting.")
        return

    # Extract paths from configuration
    download_path = config.get("Paths", "download_path", fallback="./")
    log_file_path = config.get("Paths", "log_file_path", fallback="log.log")

    # Ensure directories exist
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Static URL
    base_url = "https://www.rba.gov.au/statistics/tables/xls/f01d.xlsx"

    # Generate filename with the current date
    current_time = datetime.now(timezone.utc)
    file_date = current_time.strftime("%Y%m%d")
    filename = os.path.join(download_path, f"{file_date}_f01d.xlsx")

    # Get script name for logging
    script_name = os.path.basename(__file__)

    try:
        # Make the request
        response = requests.get(base_url)
        
        # Check for successful response
        if response.status_code == 200:
            # Save the file locally
            with open(filename, "wb") as file:
                file.write(response.content)
            status = f"Success - File saved as {filename}"
        else:
            status = f"Failed - HTTP Status Code: {response.status_code}"
        
    except Exception as e:
        # Log the exception if any
        status = f"Exception - {e}"
    
    # Log the result
    log_entry = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')},{script_name},{status}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)
    
    # Print status for debugging purposes
    print(status)

# Run the function
download_rba_file()
