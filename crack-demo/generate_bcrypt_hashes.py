import random

import bcrypt


with open("/usr/share/dict/words") as f:
    words = f.read()

word_list = words.splitlines()
passwords = []
for _ in range(0, 5):
    password = random.choice(word_list)
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    passwords.append(hashed)

with open("bcrypt_passwords.txt", "w") as f:
    f.write("\n".join(passwords))
