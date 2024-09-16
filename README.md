# Directory-Enumeration
# Directory Enumeration Tool

This tool performs **directory enumeration** to discover hidden directories on a web server. It supports multi-threading, HTTP/HTTPS protocols, various file extensions, proxy support, and customizable status code filtering. It is designed to help penetration testers, bug bounty hunters, and security enthusiasts.

## Features

- **Multi-threaded**: Scan multiple directories concurrently for faster results.
- **HTTP/HTTPS Support**: Checks both HTTP and HTTPS protocols.
- **Multiple Extensions**: Enumerates directories with different file extensions (`.html`, `.php`, etc.).
- **Proxy Support**: Route your requests through an HTTP proxy.
- **Custom User-Agent**: Mimics browser requests to avoid being blocked.
- **Timeout Handling**: Set request timeouts to prevent hanging on slow servers.
- **Status Code Filtering**: Displays only relevant HTTP response codes (e.g., 200, 301, 403).
- **Result Logging**: Optionally saves valid results to a log file.

## Prerequisites

- **Python 3.x**: Ensure that Python is installed on your system.
- **Requests Library**: Install the `requests` library using the following command:
    ```bash
    pip install requests
    ```

## Usage

```bash
python directory_enum.py <domain> -w <wordlist.txt> [options]
```
## Command-Line Arguments

| Argument           | Description                                                                 | Default                   |
|--------------------|-----------------------------------------------------------------------------|---------------------------|
| `<domain>`         | The target domain you want to scan (e.g., `example.com`).                    | Required                  |
| `-w`, `--wordlist`  | Path to the wordlist file containing directory names.                       | Required                  |
| `-t`, `--threads`   | Number of threads to use.                                                   | 10                        |
| `-p`, `--protocols` | Protocols to use (`http`, `https`). Accepts multiple values.                | `http https`              |
| `-e`, `--extensions`| File extensions to try (e.g., `.html`, `.php`).                            | `'' .html .php .txt`       |
| `-u`, `--user-agent`| Custom User-Agent string.                                                   | `Mozilla/5.0`             |
| `-T`, `--timeout`   | Timeout for each request (in seconds).                                      | 5                         |
| `--proxy`           | Proxy to route requests through (e.g., `http://127.0.0.1:8080`).            | None                      |
| `-s`, `--status-codes`| Status codes to filter (e.g., `200`, `301`, `403`).                       | `200 301 302 403`         |
| `-l`, `--log-file`  | Log valid results to a file.                                                | None                      |
# Directory Enumeration Tool

## Usage Examples

1. **Basic Directory Enumeration**:
    ```bash
    python directory_enum.py example.com -w wordlist.txt
    ```

2. **Scan with Multiple Extensions**:
    ```bash
    python directory_enum.py example.com -w wordlist.txt -e "" .html .php
    ```

3. **Using a Proxy**:
    ```bash
    python directory_enum.py example.com -w wordlist.txt --proxy http://127.0.0.1:8080
    ```

4. **Save Results to a Log File**:
    ```bash
    python directory_enum.py example.com -w wordlist.txt -l valid_directories.txt
    ```

5. **Increase Threads for Faster Scanning**:
    ```bash
    python directory_enum.py example.com -w wordlist.txt -t 20
    ```

## Example Wordlist (`wordlist.txt`)

Here’s an example of what your `wordlist.txt` might look like:


You can find more comprehensive wordlists online or create your own to target specific environments.

## Output

Valid directories are printed to the console if they return an HTTP status code from the allowed list (200, 301, 302, 403).

If the `--log-file` option is specified, results are also saved to the specified log file.

## License

This tool is released under the MIT License. Feel free to use, modify, and distribute it.

## Contribution

If you'd like to contribute to the project, please submit pull requests or report issues.

## Disclaimer

This tool is meant for educational purposes and authorized penetration testing. Do not use it on systems without proper authorization. Unauthorized usage is illegal and punishable by law.

