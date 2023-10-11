import requests
from QueryGrade.encrypt import *
# 创建一个session对象
session = requests.Session()

# 设置cookie信息
session.cookies.set('route', 'bb286252294179f92ba27a393874b567')
session.cookies.set('iPlanetDirectoryPro', 'KCwpTkthcQwR0Qaf4LcfnM')
session.cookies.set('JSESSIONID', 'FE4Zap-eR1WS0lC5pNRb-XQOnqRMKPFDpSDYEyNsFl5mL274nRpd!1216369982')
session.cookies.set('CASTGC', 'TGT-48725-VI9dnZzpm0aoaLPH5NJt2DuedxytB7KAiMYCXbf4ZxC3hHdvJ51696938500048-NvaQ-cas')
# ... 设置其他的cookie ...

# 使用带有cookie的session访问某个需要登录后才能访问的资源或页面
response = session.get('http://authserver.cqu.edu.cn/authserver/index.do')

# 如果返回的内容是登录后才能看到的，那么就证明您已成功登录
print(response.text)