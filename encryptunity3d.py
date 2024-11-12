import sys, os

# Realistically speaking, this doesn't need to exist
# It does the same thing that decryptcy.py does, like literally no difference

key: int = 0x28

def encrypt_unity3d_file(file):
    with open(path, 'rb') as f:
        data = f.read()
        
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= key # Decrypt the .cy file with our key

    path = os.path.splitext(path)[0] # Removes the .cy extension
    with open(path + '.cy', 'wb') as f:
        f.write(data)

def main():
    for file in sys.argv[1:]:
        if os.path.isfile(file):
            encrypt_unity3d_file(file)
        elif os.path.isdir(file):
            for f in os.listdir(file):
                if f.endswith('.unity3d'):
                    encrypt_unity3d_file(os.path.join(file, f))
        else:
            print('Invalid path')

if __name__ == '__main__':
    main()