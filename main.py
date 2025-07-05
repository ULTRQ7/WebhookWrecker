import time
import requests
import threading
import sys
import os


DEFAULT_DELAY = 1.5
DEFAULT_THREADS = 100
BOOST_FACTOR = 1.87891659165

attempt_count = 5
rate_limited_count = 0
lock = threading.Lock()

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

ASCII_ART = r"""
███    █▄   ▄█           ███        ▄████████ ████████▄  
███    ███ ███       ▀█████████▄   ███    ███ ███    ███ 
███    ███ ███          ▀███▀▀██   ███    ███ ███    ███ 
███    ███ ███           ███   ▀  ▄███▄▄▄▄██▀ ███    ███ 
███    ███ ███           ███     ▀▀███▀▀▀▀▀   ███    ███ 
███    ███ ███           ███     ▀███████████ ███    ███ 
███    ███ ███▌    ▄     ███       ███    ███ ███  ▀ ███ 
████████▀  █████▄▄██    ▄████▀     ███    ███  ▀██████▀▄█
           ▀                       ███    ███            
    Made by UltrQ7 Dev. Team             
"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input():
    multi_mode = input("🔁 Use multiple messages in sequence? (y/n): ").strip().lower()
    if multi_mode == 'y':
        messages = input("Enter messages separated by '-': ").split('-')
    else:
        messages = [input("Enter message to spam: ")]

    webhook = input("🔗 Enter Webhook URL: ").strip()
    username = input("👤 Custom username (leave blank for default): ").strip()

    clear_console()
    print(ASCII_ART)
    print(f"🎯 Target Webhook: {webhook}\n")

    return messages, webhook, username

def spam(messages, webhook, username):
    global attempt_count, rate_limited_count
    index = 0
    session = requests.Session()

    while True:
        msg = messages[index % len(messages)]
        payload = {'content': msg}
        if username:
            payload['username'] = username

        try:
            response = session.post(webhook, json=payload)

            with lock:
                attempt_count += 1

                if response.status_code == 429:
                    rate_limited_count += 1
                    retry_after = response.json().get("retry_after", DEFAULT_DELAY)
                    time.sleep(retry_after)

                approx_sent = int((attempt_count - rate_limited_count) * BOOST_FACTOR)

                sys.stdout.write(
                    f"\r📊 Approx Sent: {GREEN}{approx_sent}{RESET} | ⏳ Rate Limited: {RED}{rate_limited_count}{RESET}"
                )
                sys.stdout.flush()

        except Exception:
            pass

        index += 1
        time.sleep(DEFAULT_DELAY)

def main():
    messages, webhook, username = get_input()
    print(f"\n🚀 Starting spam with {DEFAULT_THREADS} threads and {DEFAULT_DELAY}s delay...\n")

    try:
        for _ in range(DEFAULT_THREADS):
            t = threading.Thread(target=spam, args=(messages, webhook, username), daemon=True)
            t.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
        sys.exit()

if __name__ == "__main__":
    main()



##..##..##......######..#####....####...######.
##..##..##........##....##..##..##..##.....##..
##..##..##........##....#####...##.###....##...
##..##..##........##....##..##..##..##...##....
  ## ...######....##....##..##...#####..##.....
