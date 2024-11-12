import sys, os

# .cy files are files used in ddlc+ that use the encryption key of \x28 or decimal 40
# using the decryption key \x28 or decimal 40, it uses an XOR decryption on every .cy file and save them into a new file with the extension .unity3d

key: int = 0x28

def decrypt_cy_file(path):
    with open(path, 'rb') as f:
        data = f.read()
        
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= key # Decrypt the .cy file with our key

    path = os.path.splitext(path)[0] # Removes the .cy extension
    with open(path + '.unity3d', 'wb') as f:
        f.write(data)

def main():
    for file in sys.argv[1:]:
        if os.path.isfile(file):
            decrypt_cy_file(file)
        elif os.path.isdir(file):
            for f in os.listdir(file):
                if f.endswith('.cy'):
                    decrypt_cy_file(os.path.join(file, f))
        else:
            print('Invalid path')

if __name__ == '__main__':
    # make Decrypted folder
    if not os.path.exists('Decrypted'):
        os.makedirs('Decrypted')
    main()
