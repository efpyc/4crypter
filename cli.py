# -*- coding:utf-8 -*-

import os
from crypter import Fcrypter, ext

path = os.getcwd()
extend = os.sep
merge = path + extend

def mystrip(_path, _merge=merge):
    result = ""
    temp = 0
    for x in _path:
        try:
            if not x == _merge[temp]:
                result += x
        except IndexError:
            result += x
        temp += 1
    return result

def mysort(itemlist : list):
    folders = []
    files = []
    result = []
    for x in itemlist:
        item = x['item']
        name = item[::-1].split(extend)[-1]+extend if item.endswith(extend) else item.split(extend)[-1]
        itemtype = x['type']
        if itemtype == "FILE":
            files.append(
                {
                    "path": item,
                    "name": name,
                    "type": itemtype
                }
            )
        else:
            folders.append(
                {
                    "path": item,
                    "name": name,
                    "type": itemtype
                }
            )
    for folder in folders:
        result.append(folder)
    for file in files:
        result.append(file)
    return result

def ls(path=merge, fourext=False):
    items = []
    listdir = os.listdir(path)
    listdir.sort()
    if fourext:
        for root, dirs, file in os.walk(path):
            for f in file:
                if f.endswith(ext):
                    items.append(
                        {
                            "item": os.path.join(root, f), "type": "FILE"
                        }
                    )
    else:
        for item in listdir:
            if os.path.isfile(os.path.join(path, item)):
                items.append({"item": os.path.join(path, item), "type": "FILE"})
            else:
                items.append({"item": os.path.join(path, item), "type": "FOLDER"})
    temp = 1
    pretty = "[ {} ] {} | {}"
    mysorted = mysort(itemlist=items)
    if not fourext:
        for x in mysorted:
            objtype = x["type"]
            objname = x["name"]
            print(pretty.format(temp, objname, objtype))
            temp += 1
    else:
        for x in mysorted:
            objname = mystrip(x['path'])
            objtype = x['type']
            print(pretty.format(temp, objname, objtype))
            temp += 1
    return mysorted

def parse(string : str):
    result = []
    if "," in string:
        strlist = string.split(",")
        for num in strlist:
            result.append(num.strip())
    else:
        strlist = string.split()
        for num in strlist:
            result.append(num.strip())
    return result

def main():
    key = input("[?] Key (max length 32 char): ")
    if len(key) > 32:
        print("Please put key sorter than 32 char")
        return main()
    crypter = Fcrypter(key=key)
    ec = input("Encrypt/Decrypt?: ").lower()
    cryptmode = int(input("\n[ 0 ] AES-256-CBC\n[ 1 ] MultiFernet\n\nCrypt mode: "))
    if cryptmode == 0:
        aes = True
    elif cryptmode == 1:
        aes = False
    else:
        print("Please select 0 or 1")
        return main()
    spesific_path = input("Path (if press enter, path will be current work directory): ")
    print(" ")
    print("[ 0 ] All")
    if not spesific_path == "":
        if ec.startswith("d"):
            items = ls(path=spesific_path, fourext=True)
        else:
            items = ls(path=spesific_path)
    else:
        if ec.startswith("d"):
            items = ls(fourext=True)
        else:
            items = ls()
    print(" ")
    options_ask = input("[?] Select file(s)/folder(s) you want crypt: ")
    if options_ask.replace(" ", "") == "":
        print("Please select number.")
        return main()
    print(" ")
    options = parse(options_ask)
    if options[0] != 0 and len(options) > 1:
        for opt in options:
            item = items[int(opt) - 1]
            print(item['name'], "|", item['type'])
    else:
        for item in items:
            print(item['name'], "|", item['type'])
    print(" ")
    if ec.startswith("e"):
        print("Will be encrypted.")
    else:
        print("Will be decrypted.")
    yesno = input("Are you sure?: ").lower()
    if yesno.startswith("y"):
        if options[0] != 0 and len(options) > 1:
            for option in options:
                cryptable = items[int(option) - 1]
                cpath = cryptable['path']
                ctype = cryptable['type']
                cname = cryptable['name']
                if ec.startswith("e"):
                    if ctype == 'FOLDER':
                        crypter.encryptFolder(cpath, aes=aes)
                        print(f"'{cname}' folder is crypted!")
                    else:
                        crypter.encryptFile(cpath, aes=aes)
                        print(f"'{cname}' file is crypted!")
                elif ec.startswith("d"):
                    if ctype == 'FOLDER':
                        crypter.decryptFolder(cpath, aes=aes)
                        print(f"'{cname}' folder is decrypted!")
                    else:
                        crypter.decryptFile(cpath, aes=aes)
                        print(f"'{cname}' file is decrypted!")
        else:
            for it in items:
                cpath = it['path']
                ctype = it['type']
                cname = it['name']
                if ec.startswith("e"):
                    if ctype == 'FOLDER':
                        crypter.encryptFolder(cpath, aes=aes)
                        print(f"'{cname}' folder is crypted!")
                    else:
                        crypter.encryptFile(cpath, aes=aes)
                        print(f"'{cname}' file is crypted!")
                elif ec.startswith("d"):
                    if ctype == 'FOLDER':
                        crypter.decryptFolder(cpath, aes=aes)
                        print(f"'{cname}' folder is decrypted!")
                    else:
                        crypter.decryptFile(cpath, aes=aes)
                        print(f"'{cname}' file is decrypted!")
    else:
        print("Process is canceled!")

if __name__ == '__main__':
    main()