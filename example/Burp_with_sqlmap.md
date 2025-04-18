## 前言
sqlmap作为一款优秀的SQL注入测试插件被广泛的应用于渗透测试过程中，我们经常使用 -r 参数以此来提高注入成功率。与此同时针对大量数据包的测试，sqlmap提供 -l 参数，通过读取Burp日志实现大量请求的批量测试。但是Burp日志包经常存储有非授权的目标域名，以及大量静态请求资源（例如js、css、png等），此类静态资源很少存在SQL注入，如果直接测试日志验证，影响渗透测试效率。在此背景下，通过使用本项目中的脚本，可以自动过滤非授权目标资产，并自动过滤常见静态资源。

---
## 使用方法
1. 在 Burp 中依次点击，Settings > Project > Logging > 勾选Proxy栏目中的Request按钮。
![8498ba7d36f68307c7359c4c7d5abd0](https://github.com/user-attachments/assets/b931aadd-1093-4b7a-bcc0-4b6186a2ce8d)

3. 勾选按钮后页面会提示文件保存位置及名称，建议名称设置为burp.log，这是脚本中默认读取的文件名称。
![19041ecfa335f03802e3df75c2424c8](https://github.com/user-attachments/assets/49e6e0e2-f477-4759-9a11-5067a6e3e6bf)

5. 通过git clone本项目并进入代码更目录，运行 python .\burp_filter.py 测试脚本是否可以正常工作。
![ac06a7c0de4c5822d57e3079ceeaac8](https://github.com/user-attachments/assets/543984a4-ae3f-48f6-a6ed-95e00228de4e)

7. 使用 -u 参数快速对指定目标域名提取信息，在指定多个域名时可以使用 , 分割不同的请求参数，或者通过读取文件的方式获得域名地址。（注意：域名地址不需要使用通配符，例如http://github.com 仅需写入github即可）。
![225e2b2b18711aa800195b0ec1eb4a8](https://github.com/user-attachments/assets/3304bd72-9e3c-40aa-acd1-fd3f676e95c7)

---
## 页面交互
- 脚本运行后提示加载的目标域名数量，以及在日志过滤过程中发现符合条件的目标域名
![51f7bdbe9ec7ba4cad87b91d3fc3f19](https://github.com/user-attachments/assets/d987f3cb-78d2-43fc-a011-1a400a3d645c)

- 过滤结束后会显示前10条日志不匹配的原因，可以通过修改代码增加显示数目
![d0cf3bccb076798f56f3ae24fd91a4a](https://github.com/user-attachments/assets/2c7dddc4-8c29-4619-bdf0-55313ba82789)

---
## sqlamp的一些使用技巧
- 通过 --batch 参数自动化的进行测试，官方的参数说明如下：
> Act in non-interactive mode
Switch: --batch

If you want sqlmap to run as a batch tool, without any user's interaction when sqlmap requires it, you can force that by using switch --batch. This will leave sqlmap to go with a default behaviour whenever user's input would be required.

