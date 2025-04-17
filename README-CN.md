# Burp Log Filter

一款用于过滤 Burp Suite 日志的 Python 脚本。该工具允许你处理 Burp 日志文件，过滤掉非目标域名的请求以及静态资源（例如图像、CSS、JavaScript）。它支持直接指定域名和通过域名文件输入。

## 功能特点

- 根据目标域名过滤请求，支持导入目标域名文件或同时指定多个域名。
- 移除静态资源，如图像、CSS、JavaScript 等。
- 易于使用的命令行界面，提供多种选项。

## 需求

- Python 3.x
- `argparse` 模块（标准库）
- `re` 模块（标准库）
- `os` 模块（标准库）
- `urllib.parse` 模块（标准库）

## 安装

将本仓库克隆到本地：

```bash
git clone https://github.com/amoy6228/BurplogFilter.git
cd BurplogFilter
```

确保你安装了 Python 3.x。

## 使用方法

### 基本示例

```bash
python burp_filter.py -l burp.log -u "bing.com"
```

此命令将处理 `burp.log` 文件，过滤出对 `bing.com` 的请求，并将结果保存到 `filtered.log`。

### 使用域名文件的高级示例

```bash
python burp_filter.py -uf domains.txt -o results.log
```

此命令将从 `domains.txt` 文件中加载目标域名（每行一个域名），并将过滤后的日志输出到 `results.log`。

### 命令行选项

| 选项                 | 描述                                                 |
| -------------------- | ---------------------------------------------------- |
| `-l, --log`          | Burp 日志文件的路径（默认：当前目录下的 `burp.log`） |
| `-u, --domain`       | 要过滤的目标域名（可以多次使用或用逗号分隔多个域名） |
| `-uf, --domain-file` | 包含目标域名的文本文件（每行一个域名）               |
| `-o, --output`       | 输出过滤后的日志文件路径（默认：`filtered.log`）     |

### 搭配 sqlmap 使用示例

详细使用方法请参考该链接。

不匹配目标列表的域名以及像 `.png`、`.css` 等静态资源将被过滤掉。

## 统计信息

处理完日志文件后，脚本将显示过滤统计信息，包括保留的和过滤掉的日志块总数，以及前 10 条过滤原因。

## 作者

- **爱喝水的仙人掌** (GitHub: [amoy6228](https://github.com/amoy6228))

## 许可证

此项目采用 MIT 许可证 - 请参阅 [LICENSE](https://github.com/amoy6228/BurplogFilter/blob/main/LICENSE) 文件以了解更多详情。
