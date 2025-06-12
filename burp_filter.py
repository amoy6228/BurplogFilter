# encoding: utf-8
# @author: 爱喝水的仙人掌
# @file: burp_filter_zh-cn.py
# @time: 2025/4/17 11:37
import re
import os
import argparse
from urllib.parse import urlparse


def filter_burp_log(input_file, output_file, target_domains):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 优化后的正则表达式（保持原始分隔符长度）
    block_pattern_no_ip = re.compile(
        r'(={20,}\n'  # 起始分隔符
        r'(\d{2}:\d{2}:\d{2})\s+'  # 时间戳（组1）
        r'(https?://[^\s/]+)\s+'  # 域名（组2）
        r'={20,}\n'  # 分隔符
        r'((?:.|\n)*?)'  # 请求内容（组3）
        r'(?=\n={20,}|\Z))',  # 前瞻终止条件
        re.DOTALL
    )
    blocks_no_ip = block_pattern_no_ip.findall(content)

    block_pattern_ip = re.compile(
        r'(={20,}\n'  # 起始分隔符
        r'(\d{2}:\d{2}:\d{2})\s+'  # 时间戳（组1）
        r'(https?://[^\s/]+)\s+'  # 域名（组2）
        r'\[([^\]]+)\]\n'  # IP地址（组3）
        r'={20,}\n'  # 分隔符
        r'((?:.|\n)*?)'  # 请求内容（组4）
        r'(?=\n={20,}|\Z))',  # 前瞻终止条件
        re.DOTALL
    )
    blocks_ip = block_pattern_ip.findall(content)
    blocks = blocks_ip + blocks_no_ip

    filtered_blocks = []
    filtered_reasons = []
    domain_cache = set()

    for block in blocks:
        if len(block) == 4:
            timestamp, domain, request_content = block[1], block[2], block[3]
            ip = "0.0.0.0" # 设置一个默认值 为保持统一
        elif len(block) == 5:
            timestamp, domain, ip, request_content = block[1], block[2], block[3], block[4]

        request_lines = request_content.strip().split('\n')

        # 域名验证逻辑（支持子域名匹配）
        parsed_domain = urlparse(domain).hostname
        if not any(d in parsed_domain for d in target_domains):
            filtered_reasons.append(
                f"[{timestamp}] 域名过滤: {parsed_domain} (不匹配目标列表)"
            )
            continue

        # 静态资源过滤逻辑（扩展可配置）
        request_line = request_lines[0].strip() if request_lines else ""
        if not request_line:
            continue

        # 使用正则增强路径解析
        path_match = re.match(r'^(?:GET|POST|PUT|DELETE|OPTIONS)\s+([^\s?]+)', request_line)
        if not path_match:
            continue

        path = path_match.group(1)
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.js', '.css', '.png', '.jpg', '.gif', '.webp', '.svg', '.xml', '.json', '.yml'):
            filtered_reasons.append(
                f"[{timestamp}] 静态资源过滤: {path} (类型 {ext})"
            )
            continue

        # 记录唯一域名（调试用）
        if parsed_domain not in domain_cache:
            domain_cache.add(parsed_domain)
            print(f"[+] 发现有效域名: {parsed_domain}")

        # 保留原始块格式
        temp_string = block[0]
        temp_string += "\n" + "=" * 55
        filtered_blocks.append(temp_string)

    # 写入结果（保留原始分隔符）
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write('\n\n\n\n'.join(filtered_blocks))
        f.write("=" * 50 + "\n")


    # 输出统计信息
    print("\n===== 过滤统计 默认显示前10条过滤原因 =====")
    for reason in filtered_reasons[:10]:  # 只显示前10条过滤原因
        print(reason)
    print(f"\n总保留数: {len(filtered_blocks)} | 总过滤数: {len(filtered_reasons)}")


def main():
    parser = argparse.ArgumentParser(
        description='Burp日志过滤器 Version 0.2 - 按域名和静态资源过滤请求',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='使用示例:\n'
               '  python burp_filter.py -l burp.log -u "bing.com"\n'
               '  python burp_filter.py -uf domains.txt -o results.log'
    )

    parser.add_argument('-l', '--log', dest='input_file', default='burp.log',
                        help='Burp日志文件路径（默认：当前目录的burp.log）')
    parser.add_argument('-u', '--domain', action='append', default=[],
                        help='目标域名（可多次使用或逗号分隔多个值）')
    parser.add_argument('-uf', '--domain-file',
                        help='包含目标域名的文本文件（每行一个域名）')
    parser.add_argument('-o', '--output', dest='output_file', default='filtered.log',
                        help='输出文件路径（默认：filtered.log）')

    args = parser.parse_args()

    # 域名处理逻辑
    target_domains = set()

    # 处理-u参数
    if args.domain:
        for d in args.domain:
            target_domains.update([x.strip().lower() for x in d.split(',') if x.strip()])

    # 处理-uf参数
    if args.domain_file:
        try:
            with open(args.domain_file, 'r', encoding='utf-8') as f:
                target_domains.update([line.strip().lower() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"[!] 错误：域名文件 {args.domain_file} 不存在")
            return

    if not target_domains:
        print("[!] 错误：必须通过 -u 或 -uf 指定至少一个域名")
        parser.print_help()
        return

    print(f"[*] 加载 {len(target_domains)} 个目标域名")
    filter_burp_log(args.input_file, args.output_file, target_domains)


if __name__ == '__main__':
    main()
