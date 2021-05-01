# coding = UTF-8


from KuGou.Tools.WebTools import WangYiYunMusicList as ML

Result1 = ML()
# Result2 = Result1.GetMusicList("所念皆星河 CMJ")
Result2 = Result1.GetMusicList("大鱼 周深")
for i in Result2:
    print(i.Name)
