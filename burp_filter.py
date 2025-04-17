# encoding: utf-8
# @author: 爱喝水的仙人掌
# @file: burp_filter.py
# @time: 2025/4/16 14:39
import re
import os
import argparse
from urllib.parse import urlparse


def filter_burp_log(input_file, output_file, target_domains):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Optimized regular expression (maintaining original separator length)
    block_pattern = re.compile(
        r'(={20,}\n'  # Starting separator
        r'(\d{2}:\d{2}:\d{2})\s+'  # Timestamp (Group 1)
        r'(https?://[^\s/]+)\s+'  # Domain (Group 2)
        # r'$([^$]+)\]\n'  # IP Address (Group 3)
        r'={20,}\n'  # Separator
        r'((?:.|\n)*?)'  # Request Content (Group 4)
        r'(?=\n={20,}|\Z))',  # Forward-looking termination condition
        re.DOTALL
    )
    blocks = block_pattern.findall(content)

    filtered_blocks = []
    filtered_reasons = []
    domain_cache = set()

    for block in blocks:
        timestamp, domain, request_content = block[1], block[2], block[3]
        request_lines = request_content.strip().split('\n')

        # Domain validation logic (supports subdomain matching)
        parsed_domain = urlparse(domain).hostname
        if not any(d in parsed_domain for d in target_domains):
            filtered_reasons.append(
                f"[{timestamp}] Domain Filtered: {parsed_domain} (Does Not Match Target List)"
            )
            continue

        # Static resource filtering logic (extendable configuration)
        request_line = request_lines[0].strip() if request_lines else ""
        if not request_line:
            continue

        # Enhanced path parsing using regex
        path_match = re.match(r'^(?:GET|POST|PUT|DELETE|OPTIONS)\s+([^\s?]+)', request_line)
        if not path_match:
            continue

        path = path_match.group(1)
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.js', '.css', '.png', '.jpg', '.gif', '.webp', '.svg', '.xml', '.json', '.yml'):
            filtered_reasons.append(
                f"[{timestamp}] Static Resource Filtered: {path} (Type {ext})"
            )
            continue

        # Record unique domains (for debugging purposes)
        if parsed_domain not in domain_cache:
            domain_cache.add(parsed_domain)
            print(f"[+] Found Valid Domain: {parsed_domain}")

        # Preserve original block format
        temp_string = block[0]
        temp_string += "\n" + "=" * 55
        filtered_blocks.append(temp_string)

    # Write results (preserve original separators)
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write('\n\n\n\n'.join(filtered_blocks))
        f.write("=" * 50 + "\n")

    # Output statistics
    print("\n===== Filtering Statistics - Default Display Top 10 Filtering Reasons =====")
    for reason in filtered_reasons[:10]:  # Only display top 10 filtering reasons
        print(reason)
    print(f"\nTotal Retained: {len(filtered_blocks)} | Total Filtered: {len(filtered_reasons)}")


def main():
    parser = argparse.ArgumentParser(
        description='Burp Log Filter Version 0.1 - Filter Requests by Domain and Static Resources',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Usage Examples:\n'
               '  python burp_filter.py -l burp.log -u "bing.com"\n'
               '  python burp_filter.py -uf domains.txt -o results.log'
    )

    parser.add_argument('-l', '--log', dest='input_file', default='burp.log',
                        help='Path to Burp log file (default: burp.log in current directory)')
    parser.add_argument('-u', '--domain', action='append', default=[],
                        help='Target domain(s) (can be used multiple times or comma-separated values)')
    parser.add_argument('-uf', '--domain-file',
                        help='Text file containing target domains (one domain per line)')
    parser.add_argument('-o', '--output', dest='output_file', default='filtered.log',
                        help='Output file path (default: filtered.log)')

    args = parser.parse_args()

    # Domain processing logic
    target_domains = set()

    # Handling -u argument
    if args.domain:
        for d in args.domain:
            target_domains.update([x.strip().lower() for x in d.split(',') if x.strip()])

    # Handling -uf argument
    if args.domain_file:
        try:
            with open(args.domain_file, 'r', encoding='utf-8') as f:
                target_domains.update([line.strip().lower() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"[!] Error: Domain file {args.domain_file} does not exist")
            return

    if not target_domains:
        print("[!] Error: At least one domain must be specified via -u or -uf")
        parser.print_help()
        return

    print(f"[*] Loaded {len(target_domains)} target domains")
    filter_burp_log(args.input_file, args.output_file, target_domains)


if __name__ == '__main__':
    main()