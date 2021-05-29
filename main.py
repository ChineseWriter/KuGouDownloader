# coding = UTF-8


import KuGou

KuGou.Download(KuGou.Tools.LocalTools.MusicNameGainer(), FilePath="./Music", LrcFile=True,  # DebugFlag=True,
               Selector=KuGou.Tools.LocalTools.MusicSelector)
# KuGou.ReDownload(FilePath="./Music", LrcFile=True, DebugFlag=True)
Check = KuGou.CheckMusic()
Check.DeleteLrcWithoutMusic()
Check.DeleteVIPMusic(DebugFlag=True)
Check.DeleteTooShortMusic(DebugFlag=True)

try:
    input("Finish .")
except Exception:
    pass
