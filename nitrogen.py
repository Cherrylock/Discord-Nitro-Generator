import requests
import threading
import random
import string
from termcolor import colored

THREADS = 10

user_agents = []
with open("useragents.txt", "r") as f:
    user_agents = f.read().splitlines()

def generate_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))

def check_code():
    while True:
        code = generate_code()
        user_agent = random.choice(user_agents)
        headers = {
            "User-Agent": user_agent,
        }
        try:
            response = requests.get(
                f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true",
                headers=headers,
                timeout=10,
            )
            if response.status_code == 200:
                print(colored(f"[+] Valid code found: {code}", "green"))
                with open("valid_codes.txt", "a") as file:
                    file.write(f"https://discord.gift/{code}\n")
                return  
            else:
                print(colored(f"[-] Invalid code: {code}", "red"))
        except Exception as e:
            print(colored(f"[-] Error checking code: {code} - {e}", "yellow"))

def main():
    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=check_code)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print("A valid code is found. Program stopped.")

if __name__ == "__main__":
    main()
