import logging
import time
import unittest
from api.loginAPI import loginAPI
import requests,random,app
from parameterized import parameterized
from utils import assert_utils, DButils, read_img_verify_data, read_register_data, read_test_data


class login(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 删除用户信息表
        sql1 = "DELETE i.* from mb_member_info i INNER JOIN mb_member m ON i.member_id = m.id where m.phone in ('{}','{}','{}','{}','{}');"
        DButils.delete(sql1.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("sql1 = {}".format(sql1.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        #删除用户登录日志表
        sql2 = "DELETE l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id where m.phone in ('{}','{}','{}','{}','{}');"
        DButils.delete(sql2.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("sql2 = {}".format(sql2.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        # 删除用户主表
        sql3 = "DELETE from mb_member where phone in ('{}','{}','{}','{}','{}');"
        DButils.delete(sql3.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("sql3 = {}".format(sql3.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))
        # 删除用户的注册日志表
        sql4 = "DELETE from mb_member_register_log where phone in ('{}','{}','{}','{}','{}');"
        DButils.delete(sql4.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5))
        logging.info("sql4 = {}".format(sql4.format(app.phone1,app.phone2,app.phone3,app.phone4,app.phone5)))

    def setUp(self) -> None:
        #接口API的初始化
        self.login_api = loginAPI()
        #session对象的初始化
        self.session = requests.Session()

    def tearDown(self) -> None:
        #session对象的关闭
        self.session.close()

    #获取图片验证码
    #@parameterized.expand(read_img_verify_data)
    @parameterized.expand(read_test_data('imgVerifyCode.json','get_img_verify_code','type,status'))
    def test01_get_img_code(self,type,status):
        #准备测试数据
        if type == 'float':
            r = str(random.random())
        elif type == 'int':
            r = str(random.randint(10000000,99999999))
        elif type == 'char':
            r = ''.join(random.sample('abcdefghijklmnopq',8))
        elif type == 'kong':
            r =''
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,r)
        #针对收到的响应进行断言
        self.assertEqual(status,response.status_code)


    # #随机小数时获取图片验证码成功
    # def test01_get_img_code_success_random(self):
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #
    # #随机整数时获取图片验证码成功
    # def test02_get_img_code_success_randomInt(self):
    #     #准备测试数据
    #     r = random.randint(10000000,99999999)
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #
    # #参数为空时获取图片验证码失败
    # def test03_get_img_code_fail_param_is_null(self):
    #     #准备测试数据
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,"")
    #     #针对收到的响应进行断言
    #     self.assertEqual(404,response.status_code)
    #
    # #参数为字母时，获取图片验证码失败
    # def test04_get_img_code_fail_random_char(self):
    #     #准备测试数据
    #     r_list = random.sample("abcdefghijklmn",8)
    #     r = ''.join(r_list)
    #     logging.info("r = {}".format(r))
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,r)
    #     #针对收到的响应进行断言
    #     self.assertEqual(400,response.status_code)

    #参数正确时，获取短信验证码成功
    def test05_get_sms_code_success(self):
        #1、获取图片验证码
        #准备测试数据
        r = random.random()
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,str(r))
        #针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        #2、获取短信验证码
        # 准备测试数据
        phone = app.phone1
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,phone)
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,200,200,"短信发送成功")

    #图片验证码错误，获取短信验证码失败
    def test06_get_sms_code_fail_img_code_wrong(self):
        #1、获取图片验证码
        #准备测试数据
        r = random.random()
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,str(r))
        #针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        #2、获取短信验证码
        # 准备测试数据
        phone = app.phone1
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,phone,'1234')
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    #图片验证码为空，获取短信验证码失败
    def test07_get_sms_code_fail_img_code_is_null(self):
        #1、获取图片验证码
        #准备测试数据
        r = random.random()
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,str(r))
        #针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        #2、获取短信验证码
        # 准备测试数据
        phone =app.phone1
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,phone,'')
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    #手机号为空，获取短信验证码失败
    def test08_get_sms_code_fail_phone_is_null(self):
        #1、获取图片验证码
        #准备测试数据
        r = random.random()
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,str(r))
        #针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        #2、获取短信验证码
        # 准备测试数据
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,'')
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    #未调用图片验证码，获取短信验证码失败
    def test09_get_sms_code_fail_no_img_code(self):
        #1、获取短信验证码
        # 准备测试数据
        phone = app.phone1
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,phone)
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    #注册的脚本
    #@parameterized.expand(read_register_data)
    @parameterized.expand(read_test_data('register.json','test_register','phone,pwd,verifycode,phonecode,dyServer,invitephone,status_code,status,description'))
    def test10_register(self,phone,pwd,verifycode,phonecode,dyServer,invitephone,status_code,status,description):
        #1、获取图片验证码
        #准备测试数据
        r = random.random()
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_Img_code(self.session,str(r))
        #针对收到的响应进行断言
        self.assertEqual(200,response.status_code)
        #2、获取短信验证码
        # 准备测试数据
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.get_sms_code(self.session,phone)
        logging.info("get sms code response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,200,200,"短信发送成功")
        #3、注册请求
        # 准备测试数据
        # 调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.register(self.session,phone,pwd,verifycode,phonecode,dyServer,invitephone)
        logging.info("get register response = {}".format(response.json()))
        # 针对收到的响应进行断言
        assert_utils(self,response,status_code,status,description)


    # #输入必填项，注册成功
    # def test10_register_success_param_must(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone1
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone)
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"注册成功")
    #
    # #输入所有参数项，注册成功
    # def test11_register_success_param_all(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone2
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,invitePhone="13012345678")
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"注册成功")
    #
    # #手机号已存在时，注册失败
    # def test12_register_fail_phone_is_exist(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone2
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,invitePhone="13012345678")
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,100,"手机已存在!")
    #
    # #密码为空时，注册失败
    # def test13_register_fail_password_is_null(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone3
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,'')
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,100,"密码不能为空")
    #
    # #图片验证码错误，注册失败
    # def test14_register_fail_img_code_wrong(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone4
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,imgCode='1234')
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,100,"验证码错误!")
    #
    # #获取短信验证码错误
    # def test15_register_fail_sms_code_wrong(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone4
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,phoneCode='123456')
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,100,"验证码错误")
    #
    # #不同意注册协议时，注册失败
    # def test16_register_fail_no_promission(self):
    #     #1、获取图片验证码
    #     #准备测试数据
    #     r = random.random()
    #     #调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_Img_code(self.session,str(r))
    #     #针对收到的响应进行断言
    #     self.assertEqual(200,response.status_code)
    #     #2、获取短信验证码
    #     # 准备测试数据
    #     phone = app.phone4
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.get_sms_code(self.session,phone)
    #     logging.info("get sms code response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,200,"短信发送成功")
    #     #3、注册请求
    #     # 准备测试数据
    #     # 调用API接口中的方法来发送请求，并接收响应
    #     response = self.login_api.register(self.session,phone,dyServer='off')
    #     logging.info("get register response = {}".format(response.json()))
    #     # 针对收到的响应进行断言
    #     assert_utils(self,response,200,100,"请同意我们的条款")

    #输入正确用户名密码，登录成功
    def test17_login_success(self):
        #准备测试数据
        phone = app.phone1
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone)
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,200,'登录成功')

    #输入用户不存在时，登录失败
    def test18_login_fail_phone_is_not_exist(self):
        #准备测试数据
        phone = "13098243242"
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone)
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'用户不存在')

    #输入密码为空，登录失败
    def test19_login_fail_pwd_is_null(self):
        #准备测试数据
        phone = app.phone1
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone,'')
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'密码不能为空')

    #输入密码错误时，登录失败
    def test20_login_fail_pwd_is_wrong(self):
        #1、密码错误1次，登录失败
        #准备测试数据
        phone = app.phone1
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone,'error')
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'密码错误1次,达到3次将锁定账户')
        #2、密码错误2次，登录失败
        #准备测试数据
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone,'error')
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'密码错误2次,达到3次将锁定账户')
        #3、密码错误3次，登录失败
        #准备测试数据
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone,'error')
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录')
        #4、密码正确，登录失败
        #准备测试数据
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone)
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,100,'由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录')
        #5、等待60s，密码正确，登录成功
        time.sleep(60)
        #准备测试数据
        #调用API接口中的方法来发送请求，并接收响应
        response = self.login_api.login(self.session,phone)
        logging.info("get login response = {}".format(response.json()))
        #针对收到的响应进行断言
        assert_utils(self,response,200,200,'登录成功')