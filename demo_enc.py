from cryptography.fernet import Fernet
import os.path

dir_contents = os.listdir(os.getcwd())
if 'ktext' not in dir_contents:
    key = Fernet.generate_key()
    with open('ktext', 'wb') as kt:
        kt.write(key)
else:
    with open('ktext', 'rb') as k:
        my_key = k.read()

print('My Key:', my_key)

with open('NOODLES', 'r') as unc:
    upage = unc.read()

fernet = Fernet(my_key)
enc_text = fernet.encrypt(upage.encode())

print("Encrypted Text:\n", enc_text)
dec_page = fernet.decrypt(enc_text).decode()
print("Decoded Page:\n", dec_page)