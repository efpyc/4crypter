import os,time,platform,sys
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 32
uzantı = ".four"
uyari = "[!] UYARI: Gireceğiniz Key En Fazla 32 Karakter Olmalıdır.\n[!] UYARI: Lütfen Girdiğiniz 'Key' i Unutmayın Eğer Unutursanız Bir Daha O Dosyaya Erişemezsiniz."

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

converter = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

if platform.system().lower().startswith("win"):
    clear = lambda : os.system("cls")
else:
    clear = lambda : os.system("clear")

def succes(msg):
    print(f"[+] {msg}")

def error(msg):
    print(f"[!] {msg}")

def status(msg):
    print(f"[*] {msg}")

def soru(msg):
    cevap = input(f"[?] {msg}")
    return cevap

def par(sayi, msg):
    print(f"[ {sayi} ] {msg}")


def banner():
    ban = """
           █████▒▒█████   █    ██  ██▀███      ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███  ▒███████▒
         ▓██   ▒▒██▒  ██▒ ██  ▓██▒▓██ ▒ ██▒   ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▒ ▒ ▒ ▄▀░
         ▒████ ░▒██░  ██▒▓██  ▒██░▓██ ░▄█ ▒   ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒░ ▒ ▄▀▒░ 
         ░▓█▒  ░▒██   ██░▓▓█  ░██░▒██▀▀█▄     ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄    ▄▀▒   ░
         ░▒█░   ░ ████▓▒░▒▒█████▓ ░██▓ ▒██▒   ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒███████▒
          ▒ ░   ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░    ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░░▒▒ ▓░▒░▒
          ░       ░ ▒ ▒░ ░░▒░ ░ ░   ░▒ ░ ▒░    ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░░▒ ▒ ░ ▒
          ░ ░   ░ ░ ░ ▒   ░░░ ░ ░   ░░   ░     ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░ ░ ░ ░ ░ ░
                    ░ ░     ░        ░         ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░       ░ ░    
                                                                ░                               ░        

                                @@@   @@@       @@@@@@@   @@@@@@   @@@@@@@   
                               @@@@   @@@       @@@@@@@@  @@@@@@@  @@@@@@@@  
                              @@!@!   @@!       @@!  @@@      @@@  @@!  @@@  
                             !@!!@!   !@!       !@!  @!@      @!@  !@!  @!@  
                            @!! @!!   @!!       @!@@!@!   @!@!!@   @!@!!@!   
                           !!!  !@!   !!!       !!@!!!    !!@!@!   !!@!@!    
                           :!!:!:!!:  !!:       !!:           !!:  !!: :!!   
                           !:::!!:::   :!:      :!:           :!:  :!:  !:!  
                                :::    :: ::::   ::       :: ::::  ::   :::  
                                :::   : :: : :   :         : : :    :   : :  
    """
    return ban

class Fcrypter:
    def __init__(self, key):
        self.key = key
        self.path = os.getcwd()
        self.extend = os.sep
        self.merge = self.path+self.extend
    def aesCrypt(self, veri):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cipher_bytes = cipher.encrypt(pad(veri))
        data = iv + cipher_bytes
        return data

    def aesDecrypt(self, crypted_data):
        iv = crypted_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(crypted_data[AES.block_size:]).rstrip(b"\0")
        return decrypted

    def encryptFile(self, file):
        with open(file, "rb") as dosya:
            text = dosya.read()
        encrypted = self.aesCrypt(text)
        with open(file + uzantı, "wb") as encrypted_file:
            encrypted_file.write(encrypted)
            os.remove(file)

    def decryptFile(self, file):
        with open(file, "rb") as dosya:
            crypted_text = dosya.read()
        decrypted = self.aesDecrypt(crypted_text)
        with open(file[:-int(len(uzantı))], "wb") as decrypted_file:
            decrypted_file.write(decrypted)
            os.remove(file)

def main(key):
    print(banner())
    crypted_key = converter(key)
    crypter = Fcrypter(crypted_key)
    par(1, "Verilen Dosyayı Cryptle")
    par(2, "Verilen Dosyayı Decryptle")
    print(" ")
    try:
        four = int(input("4>> "))
    except:
        error("Lütfen bir sayı girin.")
        time.sleep(2)
        clear()
        return main()

# FileNotFoundError

    if four == 1:
        dosya = input("Dosya: ")
        try:
            crypter.encryptFile(file=dosya)
        except FileNotFoundError:
            error(f"{dosya} isimli dosya bulunamadı ! Lütfen dosyaları gözden geçirin...")
            time.sleep(1)
            sys.exit()
        succes(f"{dosya} Crypt edildi !")

    elif four == 2:
        dosya = input("Dosya: ")
        try:
            crypter.decryptFile(file=dosya)
        except FileNotFoundError:
            error(f"{dosya} isimli dosya bulunamadı ! Lütfen dosyaları gözden geçirin...")
            time.sleep(1)
            sys.exit()
        succes(f"{dosya} Decrypt edildi !")

print(uyari)
key = soru("Key: ")
if len(key) > 32:
    clear()
    error("Lütfen 32 Karakterden Daha Kısa Bir Key Girin...")
    time.sleep(2)
    status("Program Sonlandırılıyor...")
    time.sleep(2)
    sys.exit()
main(key)