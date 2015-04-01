import hashlib
import random


with open("/usr/share/dict/words") as f:
    words = f.read()

word_list = words.splitlines()
passwords = []
for i in range(0, 500):
    password = random.choice(word_list)
    hex_digest = hashlib.sha256(str(i) + password).hexdigest()
    passwords.append(hex_digest)

with open("sha256_passwords.txt", "w") as f:
    f.write("\n".join(passwords))
