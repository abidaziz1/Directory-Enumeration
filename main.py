import requests
import sys
import threading
import argparse
from queue import Queue

# Global Queue to hold tasks
q = Queue()

# Function to check each directory
def check_directory(domain, directory, protocols, extensions, user_agent, timeout, proxies, status_codes, log_file):
    try:
        # Try for each protocol (http/https) and extensions
        for protocol in protocols:
            for extension in extensions:
                url = f"{protocol}://{domain}/{directory}{extension}"
                try:
                    r = requests.get(url, headers={"User-Agent": user_agent}, timeout=timeout, proxies=proxies)
                    if r.status_code in status_codes:
                        print(f"Valid directory [{r.status_code}]: {url}")
                        # Log valid directories to file
                        if log_file:
                            with open(log_file, "a") as f:
                                f.write(f"{r.status_code}: {url}\n")
                    elif r.status_code == 403:
                        print(f"Forbidden directory (403): {url}")
                except requests.ConnectionError:
                    pass
                except requests.Timeout:
                    print(f"Timeout for {url}")
                except Exception as e:
                    print(f"Error checking {url}: {str(e)}")
    except Exception as e:
        print(f"Error processing directory: {directory}, Error: {str(e)}")

# Worker thread function to process directories from the queue
def worker(domain, protocols, extensions, user_agent, timeout, proxies, status_codes, log_file):
    while not q.empty():
        directory = q.get()
        check_directory(domain, directory, protocols, extensions, user_agent, timeout, proxies, status_codes, log_file)
        q.task_done()

# Main function to set up arguments, create threads and initiate enumeration
def main():
    # Take user inputs instead of using argparse
    domain = input("Enter the target domain (e.g., example.com): ")
    wordlist_path = input("Enter the path to the wordlist file: ")

    # Input examples for threads, protocols, etc.
    try:
        threads = int(input("Enter the number of threads (default is 10): ") or "10")
    except ValueError:
        threads = 10

    protocols = input("Enter the protocols (e.g., http https) [default: http https]: ").split() or ["http", "https"]
    
    extensions = input("Enter the file extensions separated by space (e.g., '', .html, .php) [default: '', .html, .php, .txt]: ").split() or ["", ".html", ".php", ".txt"]
    
    user_agent = input("Enter the User-Agent (default is Mozilla/5.0): ") or "Mozilla/5.0"
    
    try:
        timeout = int(input("Enter the request timeout in seconds (default is 5): ") or "5")
    except ValueError:
        timeout = 5

    proxy = input("Enter the HTTP proxy (e.g., http://127.0.0.1:8080), or press Enter to skip: ") or None
    
    status_codes_input = input("Enter the status codes separated by space (e.g., 200 301 302 403) [default: 200 301 302 403]: ").split()
    status_codes = [int(code) for code in status_codes_input] if status_codes_input else [200, 301, 302, 403]
    
    log_file = input("Enter the path to the log file, or press Enter to skip: ") or None

    # Load wordlist
    try:
        with open(wordlist_path, "r") as f:
            directories = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_path}' not found.")
        sys.exit(1)

    # Set up proxy dictionary
    proxies = {"http": proxy, "https": proxy} if proxy else None

    # Add directories to the queue
    for directory in directories:
        q.put(directory)

    # Start threads
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=worker, args=(domain, protocols, extensions, user_agent, timeout, proxies, status_codes, log_file))
        threads_list.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads_list:
        t.join()

    print("Enumeration complete.")


if __name__ == "__main__":
    main()
