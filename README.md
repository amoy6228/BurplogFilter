# Burp Log Filter
README Version: \[[English](README.md) | [简体中文](README_CN.md)\]

A Python script for filtering Burp Suite logs. This tool allows you to process Burp log files, filtering out requests not targeting specified domains as well as static resources (e.g., images, CSS, JavaScript). It supports direct domain specification and importing target domains from a file.

> Significantly improve the efficiency of sqlmap -l parameter testing by filtering logs, avoiding unauthorized target domain testing.

## Features

- Filter requests based on target domains, supporting import of target domain files or specifying multiple domains simultaneously.
- Remove static resources such as images, CSS, JavaScript, etc.
- Perfectly compatible with the sqlmap -l parameter, avoiding unauthorized targets, significantly improving testing efficiency.
- Easy-to-use command-line interface with various options.

## Requirements

- Python 3.x
- `argparse` module (standard library)
- `re` module (standard library)
- `os` module (standard library)
- `urllib.parse` module (standard library)

## Installation

Clone this repository locally:

```bash
git clone https://github.com/amoy6228/BurplogFilter.git
cd BurplogFilter
```

Ensure you have Python 3.x installed.

## Usage

### Basic Example

```bash
python burp_filter.py -l burp.log -u "bing.com"
```

This command processes the `burp.log` file, filters out requests to `bing.com`, and saves the results to `filtered.log`.

### Advanced Example Using Domain File

```bash
python burp_filter.py -uf domains.txt -o results.log
```

This command loads target domains from `domains.txt` (one domain per line) and outputs filtered logs to `results.log`.

### Command Line Options

| Option                 | Description                                                 |
| ---------------------- | ------------------------------------------------------------ |
| `-l, --log`            | Path to the Burp log file (default: `burp.log` in the current directory) |
| `-u, --domain`         | Target domains to filter (can be used multiple times or separate multiple values with commas) |
| `-uf, --domain-file`   | Text file containing target domains (one domain per line)    |
| `-o, --output`         | Path to output the filtered log file (default: `filtered.log`) |

### Example with sqlmap Integration

For detailed usage instructions, refer to the linked documentation.
Burpsuit with sqlmap: \[[Usage Document](example/Burp_with_sqlmap.md)\]

## Statistics

After processing the log file, the script will display statistics including the total number of retained and filtered log blocks, along with the top 10 reasons for filtering.

## Author

- **Cactus that loves drinking water** (GitHub: [amoy6228](https://github.com/amoy6228))

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/amoy6228/BurplogFilter/blob/main/LICENSE) file for details. 
