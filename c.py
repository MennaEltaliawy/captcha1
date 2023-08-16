import requests
import time
import json

# Step 1: Get your API key
api_key = '0ee94deb238aaea7015077b91082d9b9'
captcha_type = "recaptcha2"
#step 2 : get the id of captcha 

response = requests.post("http://78.47.103.185/in.php", params={
    "key": api_key,
    "method" : "userrecaptcha",
    "googlekey" : "6Lc88v8SAAAAADOaElZWLTtlvww8wA1q29GyX9Aq" ,
    "pageurl" :"https://www.silkroadtop100.com/index.php?p=vote&id=100212",
    "json": 1

})

if response.ok:
    captcha_id = response.json().get("request")
    print(f"Captcha submitted successfully. ID: {captcha_id}")
else:
    print(f"Error submitting captcha. Response: {response.text}")
    exit()
# Step 3: Submit a HTTP GET request to get the result
max_retries = 20 if captcha_type == "recaptcha2" else 5 # set max retries based on captcha type
retry_count = 0
while retry_count < max_retries:
    response = requests.get("http://78.47.103.185/res.php", params={
        "key": api_key,
        "action": "get",
        "id": captcha_id,
        "json": 1 if captcha_type == "recaptcha2" else 0 # set json parameter for recaptcha2 captcha type
    })
    if response.ok:
        status = response.json().get("status")
        if status == 1: # captcha solved
            captcha_result = response.json().get("request")
            print(f"Captcha solved. Result: {captcha_result}")
            break
        elif status == 0: # captcha not solved yet
            retry_count += 1
            time.sleep(5)
        elif status == -1: # captcha rejected
            print("Captcha was rejected by server.")
            break
    else:
        print(f"Error checking captcha status. Response: {response.text}")
        break
# Step 3: Submit the form with the captcha solution
if captcha_result:
    response = requests.post("https://www.silkroadtop100.com/index.php?p=vote&id=100212", data={
        "g-recaptcha-response": captcha_result, # replace with appropriate form field name
        "submit": "Vote Now" # replace with appropriate submit button name
    })
    if response.ok:
        print("Captcha result submitted successfully.")
        with open("h.html","w")as file :
            file.write(response.text)
    else:
        print(f"Error submitting captcha result. Response: {response.text}")