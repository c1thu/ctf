def swap_bytes(hex_string):
    swapped_hex = ""
    for i in range(0, len(hex_string), 4):
        swapped_hex += hex_string[i+2:i+4] + hex_string[i:i+2]
    return swapped_hex

def swap_png_header(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        hex_content = content.hex()

        # Swap bytes in the hex content
        swapped_hex = swap_bytes(hex_content)

        # Write the modified content back to the file
        with open('modified_' + filename, 'wb') as modified_file:
            modified_file.write(bytes.fromhex(swapped_hex))

if __name__ == "__main__":
    filename = 'chl.png'
    swap_png_header(filename)
