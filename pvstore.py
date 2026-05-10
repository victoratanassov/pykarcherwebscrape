import os
import sys

from cryptography.fernet import Fernet

if len(sys.argv) > 1:
    if sys.argv[1] != "":
        if sys.argv[1] == '--help':
            print("pvstore.py usage:")
            print("pvstore.py --help                                - prints this message")
            print("pvstore.py --genkey keyfilename.bin              - generates a key file")
            print("pvstore.py --readkey                             - reads key from a key file and decripts password from pass file")
            print("pvstore.py --readkey requires:")
            print("pvstore.py --readkey --keyfile keyfilename.bin   - reads key from a key file and decripts password from pass file")
            print("pvstore.py --readkey --passfile passfilename.bin - reads key from a key file and decripts password from pass file")
            print("pvstore.py --writekey                             - reads key from a key file and encripts password in pass file")
            print("pvstore.py --writekey requires:")
            print("pvstore.py --writekey --keyfile keyfilename.bin   - reads key from a key file and encripts password in pass file")
            print("pvstore.py --writekey --passfile passfilename.bin - reads key from a key file and encripts password in pass file")
            print("pvstore.py --writekey --password password         - reads key from a key file and encripts password in pass file")
            exit(0)
        elif sys.argv[1] == '--genkey':
            if len(sys.argv) >= 3:
                keyfilename = sys.argv[2]
                if os.path.isfile(keyfilename):
                    print("File " + keyfilename + " exsits! Please confirm you wnt to overwrite! (Y/N)?")
                    confirm = input()
                    if confirm != 'Y':
                        print("Program completed without key generation!")
                        exit(1)
            else:
                print("File name for generating keyfile not provided!")
                exit(1)
            if keyfilename != '' and keyfilename.find('.bin') != -1:
                print("Generating key...")
                key = Fernet.generate_key()
                # print(key)
                with open(keyfilename, 'wb') as file_object:
                    file_object.write(key)
                print("Key write to file " + keyfilename + " completed successfully!")
                exit(0)
            else:
                print("Missing filename or wrong file extension provided after --genkey!")
                exit(1)
        elif sys.argv[1] == '--readkey':
            if len(sys.argv) < 6:
                print("Not enough arguments provided!")
                exit(1)
            keyfilefound = False
            passfilefound = False
            key = b''
            password = ''
            errors = []
            for i in range(2, len(sys.argv)):
                if sys.argv[i] == '--keyfile':
                    if len(sys.argv) >= i + 1:
                        keyfilename = sys.argv[i + 1]
                        if keyfilename != '' and keyfilename.find('.bin') != -1:
                            if os.path.isfile(keyfilename):
                                with open(keyfilename, 'rb') as file_object:
                                    for line in file_object:
                                        key = line
                            else:
                                print("Keyfile " + keyfilename + " don't exist!")
                                exit(1)
                        else:
                            print("Please provide a valid keyfile.bin name!")
                            exit(1)
                    else:
                        print("Please provide a keyfile name!")
                        exit(1)
                    keyfilefound = True
                elif sys.argv[i] == '--passfile':
                    if len(sys.argv) >= i + 1:
                        passfilename = sys.argv[i + 1]
                        if passfilename != '' and passfilename.find('.bin') != -1:
                            if os.path.isfile(passfilename):
                                with open(passfilename, 'rb') as file_object:
                                    for line in file_object:
                                        password = line
                            else:
                                print("Passfile " + passfilename + " don't exist!")
                                exit(1)
                        else:
                            print("Please provide a valid passfile.bin name!")
                            exit(1)
                    else:
                        print("Please provide a passfile name!")
                        exit(1)
                    passfilefound = True
            if keyfilefound == False or passfilefound == False:
                error = "--keyfile is not found - please provide --keyfile and a valid filename.bin!"
                if error not in errors and keyfilefound == False:
                    errors.append(error)
                error = "--passfile is not found - please provide --passfile and a valid filename.bin!"
                if error not in errors and passfilefound == False:
                    errors.append(error)
            if len(errors) != 0:
                for e in range(0, len(errors)):
                    print(errors[e])
                    exit(1)
            else:
                print(key)
                print(password)
                cipher_suite = Fernet(key)
                unciphered_text = (cipher_suite.decrypt(password))
                print(unciphered_text)
                plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
                print(plain_text_encryptedpassword)
        elif sys.argv[1] == '--writekey':
            if len(sys.argv) < 8:
                print("Not enough arguments provided!")
                exit(1)
            keyfilefound = False
            passfilefound = False
            passwordfound = False
            key = b''
            password = ''
            errors = []
            for i in range(2, len(sys.argv)):
                if sys.argv[i] == '--keyfile':
                    if len(sys.argv) >= i + 1:
                        keyfilename = sys.argv[i + 1]
                        if keyfilename != '' and keyfilename.find('.bin') != -1:
                            if os.path.isfile(keyfilename):
                                with open(keyfilename, 'rb') as file_object:
                                    for line in file_object:
                                        key = line
                            else:
                                print("Keyfile " + keyfilename + " don't exist!")
                                exit(1)
                        else:
                            print("Please provide a valid keyfile.bin name!")
                            exit(1)
                    else:
                        print("Please provide a keyfile name!")
                        exit(1)
                    keyfilefound = True
                elif sys.argv[i] == '--passfile':
                    if len(sys.argv) >= i + 1:
                        passfilename = sys.argv[i + 1]
                        if passfilename != '' and passfilename.find('.bin') != -1:
                            if os.path.isfile(passfilename):
                                with open(passfilename, 'rb') as file_object:
                                    for line in file_object:
                                        password = line
                            else:
                                print("Passfile " + passfilename + " don't exist! Creating...")
                        else:
                            print("Please provide a valid passfile.bin name!")
                            passfilefound = False
                            exit(1)
                    else:
                        print("Please provide a passfile name!")
                        passfilefound = False
                        exit(1)
                    passfilefound = True
                elif sys.argv[i] == '--password':
                    if len(sys.argv) >= i + 1:
                        password = sys.argv[i + 1][0:]
                    else:
                        print("Please provide a valid password!")
                        exit(1)
                    passwordfound = True
            if keyfilefound == False or passfilefound == False or passwordfound == False:
                error = "--keyfile is not found - please provide --keyfile and a valid filename.bin!"
                if error not in errors and keyfilefound == False:
                    errors.append(error)
                error = "--passfile is not found - please provide --passfile and a valid filename.bin!"
                if error not in errors and passfilefound == False:
                    errors.append(error)
                error = "--password is not found - please provide --password and a valid password!"
                if error not in errors and passwordfound == False:
                    errors.append(error)
            if len(errors) != 0:
                for e in range(0, len(errors)):
                    print(errors[e])
                    exit(1)
            else:
                print(key)
                print(password)
                cipher_suite = Fernet(key)
                ciphered_text = cipher_suite.encrypt(bytes(password, 'utf-8'))
                print(ciphered_text)
                if os.path.isfile(passfilename):
                    print("File " + passfilename + " exists! Please confirm you wnt to overwrite! (Y/N)?")
                    confirm = input()
                    if confirm != 'Y':
                        print("Program completed without password generation!")
                        exit(1)
                with open(passfilename, 'wb') as file_object:
                    file_object.write(ciphered_text)
                unciphered_text = (cipher_suite.decrypt(ciphered_text))
                print(unciphered_text)
                plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
                print(plain_text_encryptedpassword)
else:
    print("Missing parameters!!! Please run with --help for other options!")
    print("pvstore.py usage:")
    print("pvstore.py --help                                - prints this message")
    print("pvstore.py --genkey keyfilename.bin              - generates a key file")
    print("pvstore.py --readkey                             - reads key from a key file and decripts password from pass file")
    print("pvstore.py --readkey requires:")
    print("pvstore.py --readkey --keyfile keyfilename.bin   - reads key from a key file and decripts password from pass file")
    print("pvstore.py --readkey --passfile passfilename.bin - reads key from a key file and decripts password from pass file")
    print("pvstore.py --writekey                             - reads key from a key file and encripts password in pass file")
    print("pvstore.py --writekey requires:")
    print("pvstore.py --writekey --keyfile keyfilename.bin   - reads key from a key file and encripts password in pass file")
    print("pvstore.py --writekey --passfile passfilename.bin - reads key from a key file and encripts password in pass file")
    print("pvstore.py --writekey --password password         - reads key from a key file and encripts password in pass file")
    exit(0)
