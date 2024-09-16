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
    # Argument parser for command line inputs
    parser = argparse.ArgumentParser(description="Directory Enumeration Script")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-p", "--protocols", nargs="+", default=["http", "https"], help="Protocols to use (default: http https)")
    parser.add_argument("-e", "--extensions", nargs="+", default=["", ".html", ".php", ".txt"], help="File extensions (default: '', .html, .php, .txt)")
    parser.add_argument("-u", "--user-agent", default="Mozilla/5.0", help="User-Agent header to use (default: Mozilla/5.0)")
    parser.add_argument("-T", "--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("--proxy", help="HTTP proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument("-s", "--status-codes", nargs="+", type=int, default=[200, 301, 302, 403], help="HTTP status codes to display (default: 200, 301, 302, 403)")
    parser.add_argument("-l", "--log-file", help="File to log valid directories")
    args = parser.parse_args()

    # Load wordlist
    try:
        with open(args.wordlist, "r") as f:
            directories = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Wordlist file '{args.wordlist}' not found.")
        sys.exit(1)

    # Set up proxy dictionary
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    # Add directories to the queue
    for directory in directories:
        q.put(directory)

    # Start threads
    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=worker, args=(args.domain, args.protocols, args.extensions, args.user_agent, args.timeout, proxies, args.status_codes, args.log_file))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("Enumeration complete.")

if __name__ == "__main__":
    main()
