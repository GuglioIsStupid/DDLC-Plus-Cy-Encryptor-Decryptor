import sys, os, json
from PIL import Image
try:
    import UnityPy as up
except ImportError:
    print('UnityPy not found. Please install UnityPy.')
    sys.exit(1)
# .cy files are files used in ddlc+ that use the encryption key of \x28 or decimal 40
# using the decryption key \x28 or decimal 40, it uses an XOR decryption on every .cy file and save them into a new file with the extension .unity3d
# the decrypted files are then extracted using UnityPy

def decrypt_cy_file(path):
    with open(path, 'rb') as f:
        data = f.read()
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= 0x28
    # path = path without .cy extension
    path = os.path.splitext(path)[0]
    with open(path + '.unity3d', 'wb') as f:
        f.write(data)

    extract_unity3d_file(path + '.unity3d')

def main():
    file = sys.argv[1]
    if os.path.isfile(file):
        decrypt_cy_file(file)
    elif os.path.isdir(file):
        for f in os.listdir(file):
            if f.endswith('.cy'):
                decrypt_cy_file(os.path.join(file, f))
    else:
        print('Invalid path')

def extract_unity3d_file(path):
    env = up.load(path)
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            img = data.image
            data.image.save(os.path.join(os.path.dirname(path), 'Decrypted', f"{data.name}.png"))
            # edit the image 
            fp = os.path.join(os.path.dirname(path), 'Decrypted', f"{data.name}.png")
            pil_img = Image.open(fp)
            data.image = pil_img
            data.save()
        elif obj.type.name == "TextAsset":
            data = obj.read()
            with open(os.path.join(os.path.dirname(path), 'Decrypted', data.name), 'wb') as f:
                f.write(data.script)
        elif obj.type.name == "MonoBehaviour":
            if obj.serialized_type.nodes:
                tree = obj.read_typetree()
                fp = os.path.join(os.path.dirname(path), 'Decrypted', f"{tree['m_Name']}.json")
                with open(fp, 'w', encoding = "utf8") as f:
                    json.dump(tree, f, indent = 4, ensure_ascii = False)
            else:
                print(f"MonoBehaviour {obj.name} has no serialized data")
                data = obj.read()
                fp = os.path.join(os.path.dirname(path), 'Decrypted', f"{data.name}.bin")
                with open(fp, 'wb') as f:
                    f.write(data.raw_data)
        elif obj.type.name == "AudioClip":
            clip = obj.read()
            for name, data in clip.samples.items():
                with open(os.path.join(os.path.dirname(path), 'Decrypted', name), 'wb') as f:
                    f.write(data)
        elif obj.type.name == "Font":
            font = obj.read()
            extension = ".ttf"

            if font.m_FontData:
                extension = ".ttf"
                if font.m_FontData.startswith(b'OTTO'):
                    extension = ".otf"
            
            with open(os.path.join(os.path.dirname(path), 'Decrypted', f"{font.name}{extension}"), 'wb') as f:
                f.write(font.m_FontData)
        elif obj.type.name == "Mesh":
            mesh = obj.read()
            with open(os.path.join(os.path.dirname(path), 'Decrypted', f"{mesh.name}.obj"), 'w') as f:
                f.write(mesh.to_obj())


if __name__ == '__main__':
    # make Decrypted folder
    if not os.path.exists('Decrypted'):
        os.makedirs('Decrypted')
    main()