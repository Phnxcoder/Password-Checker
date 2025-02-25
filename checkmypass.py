import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/'+query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def get_pass_leak_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h , count in hashes:
        if h == hash_to_check:
            print(count)
            return count
    return 0

def api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five_char = sha1password[:5]
    tail = sha1password[5:]
    response = request_api_data(first_five_char)
    return get_pass_leak_count(response,tail)

def main(args):
    for password in args:
        count = api_check(password)
        if count:
            print(f'This password was found {count} times , you should change this password')
        else:
            print('Password was not found , you should carry On!')
    return 'done'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))