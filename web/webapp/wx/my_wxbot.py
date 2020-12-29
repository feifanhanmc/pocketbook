# -*- coding: utf-8 -*-
from wxpy import *
from unipath import Path
import os
from uuid import uuid1

class MyBot(Bot):
    # 继承Bot()，以便加入更多属性
    def __init__(self, wx_account, wx_password):
        self.wxpuid_path = self.load_wxpuid_path()

        self.wxbot_id = wxbot_id
        self.if_enable_puid = if_enable_puid

        self.puid_path = None
        self.qr_path = None
        self.console_qr = False
        self.cache_path = None
        self.qr_callback = None
        self.login_callback = None
        self.data_path = os.path.join(os.getcwd(), wx_xnr_data_path)
        self.logger = None  # 负责将相关信息log等发送到微信监管群中, 有bug
        self.qiniu = Auth(qiniu_access_key, qiniu_secret_key)
        self.groups_list = []  # 需要监听的群组的puid
        self.status = None  # 记录wxbot的登陆、listen状态等

        # 开启缓存登录
        if self.if_cache_path:
            self.cache_path = os.path.join(self.data_path, self.wxbot_id + '.pkl')
        # 登录方式
        if self.if_console_qr:
            # 使用控制台二维码登陆
            self.console_qr = True
        else:
            # 使用二维码图片登陆
            path2 = os.path.dirname(path1)
            qr_path = os.path.join(path2, wx_xnr_qrcode_path)
            self.qr_path = os.path.join(qr_path, self.wxbot_id + '_' + hashlib.md5(
                str(int(time.time()))).hexdigest() + '_qrcode.png')
            # self.qr_path = os.path.join(os.path.join(os.getcwd(), wx_xnr_qrcode_path), self.wxbot_id + '_' + hashlib.md5(str(int(time.time()))).hexdigest() + '_qrcode.png')
            if os.path.isfile(self.qr_path):  # 确保上次登录使用的二维码图片被清除掉
                os.remove(self.qr_path)
            self.change_wxxnr_redis_data({'qr_path': self.qr_path})
            # print 'qr_path', self.qr_path
            self.qr_callback = self.my_qr_callback
        if self.if_login_callback:
            self.login_callback = self.my_login_callback
        if self.if_logout_callback:
            self.if_logout_callback = self.my_logout_callback
        # 初始化需要监听的群组
        if self.init_groups_list:
            for group_puid in self.init_groups_list.split(','):
                self.groups_list.append(group_puid)

        # 登陆
        # print 'starting %s ...' % self.wxbot_id
        # print 'before login'
        # print self.cache_path
        # print self.console_qr
        # print self.qr_path
        # print u'#如果下面没有SUCCESS打印出来，多半是该账号网页版被封了……还可能是因为certifi==2015.04.28被替换掉了'
        Bot.__init__(self, self.cache_path, self.console_qr, self.qr_path, self.qr_callback, self.login_callback,
                     self.if_logout_callback)
        # print 'SUCCESS'

    def load_wxpuid_path(self):
        base_path = self.getRunDir()
        wxpuid_path = "%s/wxpuid/" % base_path
        if not Path(wxpuid_path).exists():
            Path(wxpuid_path).mkdir(True)
        return wxpuid_path

    def getRunDir(self):
        scriptPath = sys.argv[0]
        if scriptPath[0] != "/":
            fullPath = "%s/%s" % (os.getcwd(), scriptPath)
        else:
            fullPath = scriptPath
        return os.path.dirname(fullPath)

    def load_(self):