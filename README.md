# Burp Log Filter

A Python script designed to filter Burp Suite logs. This tool allows you to process Burp log files, filtering out requests to non-target domains and static resources (e.g., images, CSS, JavaScript). It supports both direct domain specification and domain file input.

## Features

- Filter requests by target domain, with support for importing a domain file or specifying multiple domains simultaneously.
- Remove static resources such as images, CSS, JavaScript, etc.
- Easy-to-use command-line interface with various options.

## Requirements

- Python 3.x
- `argparse` module (standard library)
- `re` module (standard library)
- `os` module (standard library)
- `urllib.parse` module (standard library)

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/amoy6228/BurplogFilter.git
cd BurplogFilter
```

Ensure that Python 3.x is installed.

## Usage

### Basic Example

```bash
python burp_filter.py -l burp.log -u "bing.com"
```

This command will process the `burp.log` file, filter requests to `bing.com`, and save the results to `filtered.log`.

### Advanced Example with Domain File

```bash
python burp_filter.py -uf domains.txt -o results.log
```

This command will load target domains from the `domains.txt` file (one domain per line) and output the filtered logs to `results.log`.

### Command-Line Options

| Option                | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `-l, --log`           | Path to Burp log file (default: `burp.log` in the current directory) |
| `-u, --domain`        | Target domain(s) to filter (can be used multiple times or comma-separated) |
| `-uf, --domain-file`  | Text file containing target domains (one domain per line) |
| `-o, --output`        | Output file path for filtered logs (default: `filtered.log`) |

### Example with SQLMap

For detailed usage, refer to this link.

Domains not matching the target list and static resources like `.png`, `.css`, etc., will be filtered out.

## Statistics

After processing the log file, the script will display filtering statistics, including the total number of retained and filtered blocks, as well as the top 10 filtering reasons.

## Author

- **爱喝水的仙人掌** (GitHub: [amoy6228](https://github.com/amoy6228))

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/amoy6228/BurplogFilter/blob/main/LICENSE) file for details.
