from func.common import *

def get_version(verstr):
    vernums = ",".join(verstr)
    vernums = re.findall("v\d+", vernums)
    return vernums

def up_info():
    print(color.yellow("[*] 正在联网获取更新信息..."))

    __Version = "v20210618"

    __INFO = "By Kenf"
    try:
        update_log = requests.get("http://1.15.144.22/Update.html").content.decode("utf8")
        update_log = update_log.split("\n")
        print(color.yellow("[*] " + __INFO))
        print(color.yellow("[*] 程序版本为：{}".format(__Version)))
        print(color.yellow("[*] 最新版本为：{}".format(update_log[1].split("=")[1])))

        update_version = ",".join(re.findall("v\d+", update_log[1]))
        canuse_version = get_version(update_log[2].split(","))

        if __Version in canuse_version and __Version != update_version:
            print(color.red("[*] 检测到当前不是最新版本，此版本仍在支持列表，但即将失效"))
            print(color.red("[*] " * 15))
            print(color.red("[*] 更新提要："))
            for i in update_log[4:]:
                print(color.red("[*] " + i))  
        elif __Version not in canuse_version and __Version != update_version:
            print(color.red("[*] 检测到当前版本已不再支持，请更新后再运行"))
            print(color.red("[*] " * 15))
            print(color.red("[*] 更新提要："))
            for i in update_log[4:]:
                print(color.red("[*] " + i))            
            print(color.red("[*] 程序已中断"))
            os.system("pause")
            os._exit(0)
    except:
        print(color.yellow("[*] 验证版本信息网络错误，程序中断"))
        os._exit(0)

if __name__ == '__main__':
    up_info()
