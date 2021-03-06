#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
from Crypto.Cipher import AES


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        
        decrypted_str = self.unpad(cipher.decrypt(encryptedData))
        print('decrypted_str', [decrypted_str])

        decrypted = json.loads(decrypted_str)

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    @staticmethod
    def unpad(s):
        return s[:-ord(s[len(s)-1:])]

