"""
This module will serve as automatic notification to watch latest version of hamachi for linux.
"""

import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("no-sandbox")
driver = webdriver.Chrome(options=options)

URL = "https://vpn.net/linux"

# Navigate to URL
driver.get(URL)
time.sleep(1)

# XPath for 64bit version
XPATH = '//*[@id="lb_hamachiLinuxMore"]/div[2]/a[3]'

current_version = driver.find_element(By.XPATH, XPATH).text

# Close the browser
driver.close()
driver.quit()

# Trasform text to get desired format
current_version = current_version.replace("logmein-hamachi-", "")
current_version = current_version.replace("-x64.tgz", "")
current_version = current_version.strip()

# Get last checked version (should only contain one line)
with open("last.txt", "r", encoding="utf-8") as f:
    last_version = f.readlines()[0].strip()

print(f"Last    version: {last_version}")
print(f"Current Version: {current_version}")

if last_version == current_version:
    print("No new version.")
else:
    print("There is a new version.")
    print(f"Last version: {last_version}")
    print(f"New  version: {current_version}")
    print("Saving current version as last version.")
    with open("last.txt", "w", encoding="utf-8") as f:
        f.write(f"{current_version}")

    requests.post(
        os.getenv("SMS_CONFIG_ENDPOINT"),
        json={
            "user": os.getenv("SMS_CONFIG_USER"),
            "pass": os.getenv("SMS_CONFIG_PASS"),
            "msg": f"[AUR] - Hamachi\nNew version available: {current_version}",
        },
    )
