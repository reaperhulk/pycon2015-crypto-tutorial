import bcrypt


with open("bcrypt_passwords.txt") as f:
    bcrypt_passwords = f.read()

bcrypt_list = bcrypt_passwords.splitlines()

with open("/usr/share/dict/words") as f:
    words = f.read()

word_list = words.splitlines()

for hash in bcrypt_list:
    for word in word_list:
        if bcrypt.hashpw(word, hash) == hash:
            print("Found password: {0} for hash {1}".format(word, hash))
            break
