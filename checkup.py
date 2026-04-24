import requests
import sys

def check_target(url):
    try:
        response = requests.get(url, timeout=5)

        print(f"[+] Target: {url}")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Server: {response.headers.get('Server', 'Unknown')}")

        if response.status_code == 200:
            print("[+] Target is reachable")
        else:
            print("[-] Target responded but may have issues")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkup.py <target_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    check_target(target_url)
