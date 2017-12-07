# coding=utf-8
from iHome.libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser

# ���ʺ�
accountSid = '8aaf07086010a0eb01602e79e58f0bea';

# ���ʺ�Token
accountToken = '69c99afcba844f718397bbec6dbcd2f2';

# Ӧ��Id
appId = '8aaf07086010a0eb01602e79e5df0bf0';

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com';

# ����˿�
serverPort = '8883';

# REST�汾��
softVersion = '2013-12-26';


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

def sendTemplateSMS(to, datas, tempId):
    # ��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)


sendTemplateSMS("18561523250", ["123123", "3"], "1")