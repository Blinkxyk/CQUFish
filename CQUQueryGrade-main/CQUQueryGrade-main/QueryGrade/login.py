from requests import Session, Response
import requests
from bs4 import BeautifulSoup
from .encrypt import *
from typing import Dict

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
url = "http://authserver.cqu.edu.cn/authserver/login"


def get_formdata(html: str, username: str, password: str) -> Dict:
    """生成登录表单
    """
    soup = BeautifulSoup(html, 'html.parser')
    lt = soup.find("input", {"name": "lt"})['value']
    dllt = soup.find("input", {"name": "dllt"})['value']
    execution = soup.find("input", {"name": "execution"})['value']
    _eventId = soup.find("input", {"name": "_eventId"})['value']
    rmShown = soup.find("input", {"name": "rmShown"})['value']
    default = soup.find("script", {"type": "text/javascript"}).string
    key = default[57:-3]  # 获取盐，被用来加密
    iv = randomWord(16)
    # 参数使用Encrypt加密
    a = Encrypt(key=key, iv=iv)
    passwordEncrypt = a.aes_encrypt(randomWord(64)+str(password))
    # 传入数据进行统一认证登录
    return {
        'username': str(username),
        'password': passwordEncrypt,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': rmShown
    }


def login(username: str, password: str, service: None) -> Response:
    """单点登录
    """
    session = requests.session()

    # 请求单点登录页面
    login_page = session.get(
        url=url,
        params={"service":service},
        headers=headers,
        timeout=30)
    # 登录
    formdata = get_formdata(login_page.text, username, password)
    login_response = session.post(url=url, data=formdata, headers=headers, allow_redirects=False)
    # 重定向到目标服务
    response = session.get(url=login_response.headers['Location'], headers=headers, allow_redirects=False)
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    return response
# 这行代码执行了一个HTTP GET请求。它的目的是根据登录响应中提供的`Location`头部的URL，进行一个新的请求。
#
# 详细解释如下：
#
# 1. **`session.get(...)`**：使用`session`对象进行HTTP GET请求。`session`对象在这里保留了之前登录过程中获得的所有cookies和其他会话数据，所以这次请求将带上这些数据。
#
# 2. **`url=login_response.headers['Location']`**：从`login_response`的头部中获取`Location`字段的值，并使用它作为GET请求的URL。`Location`头部通常用于HTTP重定向。
#
# 3. **`headers=headers`**：为这次GET请求设置HTTP头部。这些头部通常包含如`User-Agent`之类的信息，模拟特定的浏览器或设备发出的请求。
#
# 4. **`allow_redirects=False`**：这个参数告诉`requests`不要自动处理HTTP重定向。这意味着，如果这次GET请求返回一个重定向响应（如HTTP状态码302），`requests`不会自动发出下一个请求来跟随这个重定向。相反，它会直接返回这个重定向响应。
#
# 这行代码的常见用途是在成功登录后，服务器通常会发送一个重定向，指导客户端（在这里是你的代码）前往一个新的页面，例如用户的主页或仪表板。通过执行这个重定向请求，你的`session`对象将进一步更新，可能会接收到新的cookies或其他会话数据，这些数据可能对后续的操作（如访问用户特有的内容）至关重要。