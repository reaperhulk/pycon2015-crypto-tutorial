import hashlib


def digest_a_thing(data):
    return hashlib.sha256(word).hexdigest()


with open("sha256_passwords.txt") as f:
    sha256_passwords = f.read()

sha256_list = sha256_passwords.splitlines()

with open("/usr/share/dict/words") as f:
    words = f.read()

word_list = words.splitlines()
i = 0
for hex_digest in sha256_list:
    for word in word_list:
        computed_digest = hashlib.sha256(str(i) + word).hexdigest()
        if hex_digest == computed_digest:
            print("Found password: {0} for hash {1}".format(word, hex_digest))
            break

    i += 1
