# coding = UTF-8
# __init__.py
"""预先导入必要的东西，如：JS支持，网站标识，必需的第三方库等"""


from KuGou.Requirement.KuGouJavaScript import Key, GetSign, GetSignFunction
from KuGou.Requirement.WangYiYunAES import AESKey


# 导入必需的第三方库
with open("./KuGou/Requirement/KuGouRequirement.txt", "r", encoding="UTF-8") as File:
    KuGouRequirements = File.read()  # 此数据是文本(字符串)数据
# 导入酷狗音乐的Logo(标识)
with open("./KuGou/Requirement/logo.ico", "rb") as File:
    KuGouLogo = File.read()  # 此数据是二进制数据

del File  # 删除该变量，防止误用
