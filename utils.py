import logging
import pymysql
import requests
from bs4 import BeautifulSoup
import app
import json

def assert_utils(self,response,status_code,status,desc):
    # 针对收到的响应进行断言
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get('status'))
    self.assertEqual(desc, response.json().get("description"))

def third_request_api(form_data):
    #解析form表单中的内容，并提取参数发送第三方请求
    soup = BeautifulSoup(form_data, 'html.parser')
    third_request_url = soup.form['action']
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third request data = {}".format(data))
    # 调用响应中的url和参数来发送请求，并接收响应
    response = requests.post(third_request_url, data=data)
    logging.info("third response data={}".format(response.text))
    return response

class DButils():
    @classmethod
    def get_conn(cls):
        conn = pymysql.connect(app.DATABASE_HOST,app.DATABASE_USER,app.BATABASE_PWD,app.DATABASE_NAME,app.DATABASE_PORT,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor,conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,sql):
        try:
            conn = DButils.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            DButils.close(cursor,conn)

#解析图片验证码的参数化数据文件
def read_img_verify_data():
    #打开文件
    file_name = app.BASE_DIR + '/data/imgVerifyCode.json'
    #读取数据文件中的数据
    test_data_list = []
    with open(file_name,encoding='utf-8') as f:
        #将json数据文件转化为字典格式
        img_verify_data = json.load(f)
        #提取参数化中的所有的数据
        data_list = img_verify_data.get("get_img_verify_code")
        for data in data_list:
            test_data_list.append((data.get("type"),data.get("status")))
    #返回列表数据
    print(test_data_list)
    return test_data_list

#解析注册的参数化数据文件
def read_register_data():
    #打开文件
    file_name = app.BASE_DIR + "/data/register.json"
    #读取文件中的数据
    test_data_list = []
    with open(file_name,encoding='utf-8') as f:
        #将json格式的文件转化为字典格式
        register_data = json.load(f)
        #提取参数化中所有的数据
        data_list = register_data.get("test_register")
        for data in data_list:
            test_data_list.append((data.get("phone"),data.get("pwd"),data.get("verifycode"),data.get("phonecode"),data.get("dyServer"),data.get("invitephone"),data.get("status_code"),data.get("status"),data.get("description")))
    #返回列表数据
    print(test_data_list)
    return test_data_list

#定义方法统一读取所有的参数化数据文件
def read_test_data(filename,methodname,params):
    #filename：每个接口的测试数据文件的名称。如：register.json
    #methodname: 每个接口的测试数据文件中对应数据列表的键名。如：test_register
    #params: 一个字符串，包含每个接口的测试数据中所有的参数名（请求和响应断言结果的参数名）。如："phone,pwd,verifycode,phonecode,dyServer,invitephone,status_code,status,description"
    #打开文件
    file_path = app.BASE_DIR + "/data/" + filename
    #读取文件中的数据
    test_data_list = []
    with open(file_path,encoding='utf-8') as f:
        #将json数据文件转化为字典格式
        json_test_data = json.load(f)
        #提取参数化中的所有测试数据
        data_list = json_test_data.get(methodname)
        for data in data_list:
            data_list = []
            for param in params.split(','):
                data_list.append(data.get(param))
            test_data_list.append(data_list)
    #返回列表数据
    print(test_data_list)
    return test_data_list