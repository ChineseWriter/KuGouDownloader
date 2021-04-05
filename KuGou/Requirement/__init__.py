# coding = UTF-8


from KuGou.Requirement.JavaScript import Key, GetSign, GetSignFunction


with open("./KuGou/Requirement/KuGouRequirement.txt", "r", encoding="UTF-8") as File:
    KuGouRequirements = File.read()
with open("./KuGou/Requirement/logo.ico", "rb") as File:
    KuGouLogo = File.read()

del File
