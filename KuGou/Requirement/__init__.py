# coding = UTF-8
# __init__.py
"""预先导入必要的东西，如：JS支持，网站标识，必需的第三方库等"""


# 酷狗的签名构造所需数据，包括密钥、JavaScript签名构造函数。
from KuGou.Requirement.KuGouJavaScript import Key, GetSign, GetSignFunction
# 网易云的密钥构造所需数据，采用AES的CBC模式加密的算法。
from KuGou.Requirement.WangYiYunAES import AESKey

# 导入必需的第三方库列表
try:
    with open("./KuGou/Requirement/KuGouRequirement.txt", "r", encoding="UTF-8") as File:
        KuGouRequirements = File.read()  # 此数据是文本(字符串)数据
except FileNotFoundError:
    pass
# 导入酷狗音乐的Logo(标识)
try:
    with open("./KuGou/Requirement/logo.ico", "rb") as File:
        KuGouLogo = File.read()  # 此数据是二进制数据
except FileNotFoundError:
    pass

try:
    del File  # 删除该变量，防止误用
except NameError:
    pass
