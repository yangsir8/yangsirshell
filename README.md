## 简介
    该工具旨在通过rce功能点实现webshell管理功能。目前已实现的功能为通过post或者get请求的功能点实现命令执行和文件上传。
    该工具的亮眼之处在于无需上传一句话木马，而是通过模式匹配串替换实现远程rce。然后通过这种rce实现文件上传和执行的功能。

## 参数介绍
```
  -h, --help            show this help message and exit
  --url rce_url, -u rce_url
                        存在RCE的url功能点
  --cmd_str cmd_str, -cs cmd_str
                        命令字符串的位置，默认为cmd
  --cmd cmd, -c cmd     要执行的命令，默认为whoami
  --method method, -m method
                        请求url的方法，默认为get
  --data data           post方式需要传递数据
  --cookie cookie       传入cookie的文件
  -r txt_burpsuit       传入一个burp的数据包
  -f file               要上传文件
  -o output             上传文件的位置，推荐/tmp

```


## 使用展示
![image.png](https://cdn.nlark.com/yuque/0/2022/png/29354111/1666182251506-67f76365-4c1f-4d78-92fe-4b29541a3a91.png#clientId=u1caf1ffc-89c5-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=293&id=ufd2e1193&margin=%5Bobject%20Object%5D&name=image.png&originHeight=366&originWidth=1455&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18742&status=done&style=none&taskId=u9f2e1e05-a423-4f17-93b8-15b6451ab0a&title=&width=1164)

## 后续功能改善 -- version2

1. 功能增加：
- 增加直接导入burp数据包，然后实现shell的管理功能
- 增加整合已有exp的功能
- 增加windows文件上传功能 -- 通过certil工具实现
2. 功能改善
- 优化shell交互页面，实现伪交互页面
- 优化文件上传过程中linux和windows需要分开考虑的现状，最好实现自动识别 -- 可以通过获取系统信息识别
- 优化文件上传实现方式，比如可以多集合集中上传方法，以避免目标系统无法使用echo导致文件导入失败
- 优化shell执行过程中识别执行结果的准确度。力求在大量http响应中精准识别返回结果，同时希望精简界面，最好做到伪交互。
