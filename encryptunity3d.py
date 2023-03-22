import sys, os

def encrypt_unity3d_file(file):
    # encrypt unity3d fule to \x28 or decimal 40 using XOR
    with open(file, 'rb') as f:
        data = f.read()
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= 0x28
    # file = file with .unity3d extension
    file = os.path.splitext(file)[0]
    with open(file + '.cy', 'wb') as f:
        f.write(data)

def main():
    file = sys.argv[1]
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