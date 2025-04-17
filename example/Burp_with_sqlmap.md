## 前言
sqlmap作为一款优秀的SQL注入测试插件被广泛的应用于渗透测试过程中，我们经常使用 -r 参数提高注入成功率。与此同时针对大量数据包的测试，sqlmap 提供 -l 参数，通过读取Burp日志实现大量请求的批量测试。但是Burp日志包经常存储有非授权的目标域名，以及大量静态请求资源（例如js、css、png），此类静态资源很少存在SQL注入，如果直接测试验证影响渗透测试效率。在此背景下，通过使用本项目中的脚本，可以自动过滤非授权目标资产，并自动剔除常见静态资源。
---
## 使用方法
1. 在 Burp 中依次点击，Settings > Project > Logging > 勾选Proxy栏目中的Request按钮。
![8498ba7d36f68307c7359c4c7d5abd0](https://github.com/user-attachments/assets/b931aadd-1093-4b7a-bcc0-4b6186a2ce8d)
2. 勾选按钮后页面会提示文件保存位置及名称，建议名称设置为burp.log，这是脚本中默认读取的文件名称。
![19041ecfa335f03802e3df75c2424c8](https://github.com/user-attachments/assets/49e6e0e2-f477-4759-9a11-5067a6e3e6bf)
3. 通过git clone本项目并进入代码更目录，运行 python .\burp_filter.py 测试脚本是否可以正常工作。
![ac06a7c0de4c5822d57e3079ceeaac8](https://github.com/user-attachments/assets/543984a4-ae3f-48f6-a6ed-95e00228de4e)
4. 使用-u参数快速对指定目标域名提取信息。
