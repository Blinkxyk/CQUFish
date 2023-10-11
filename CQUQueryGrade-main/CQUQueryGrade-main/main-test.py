from QueryGrade.query_grade import query_grade
from QueryGrade.query_course_list import query_session, query_major_course
# from gui import app
from requests import Session, Response
import os
from typing import Dict, Optional, Callable
from QueryGrade.login import *
from login_test import *

AUTHSERVER_URL = "http://authserver.cqu.edu.cn/authserver/login"
if __name__ == "__main__":
    session = Session()  # 创建 Session 类的实例
    response = login(session=session, username="30011840",password="ab1982121613",service=None)
    print(response.status_code)
    print(response.text)
    print(response.content)
    print(response.headers)
    print(response.url)