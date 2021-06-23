import os, sys, random, time
import json, base64, pickle, requests, re
from requests.cookies import RequestsCookieJar
from configparser import ConfigParser
from func import color
from func.dingding import DingDingHandler

def get_appsyspatch():
    application_path = './'
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    return application_path
        
def load_config(nologo = False):
    if nologo == False:
        print("=" * 60 + "\n" + load_logo())
    else:
        pass
    xue_cfg = ConfigParser()
    sys_patch = get_appsyspatch()
    if(not os.path.exists(sys_patch + "/Config")):
        os.mkdir(sys_patch + "/Config")
    if(not os.path.exists(sys_patch + "/User")):
        os.mkdir(sys_patch + "/User")
    if(not os.path.exists(sys_patch + "/Config/config.cfg")):
        print("=" * 60)
        print("@启动失败，缺少配置文件: Config/config.cfg")
        os._exit(0)
    else:
        xue_cfg.read(sys_patch + "/Config/config.cfg", encoding='utf-8')    
    return xue_cfg
    
def save_json_data(filename, filedata):
    with open(filename,'w', encoding = 'utf-8') as j:
        json.dump(filedata, j, indent=4, ensure_ascii=False)

def get_json_data(filename):
    template_json_str = '''{}'''
    if(os.path.exists(filename) and os.path.getsize(filename) != 0):
        with open(filename, 'r', encoding = 'utf-8') as j:
            try:
                json_data = json.load(j)
            except Exception as e:
                print(filename, "解析错误：", str(e))
                print("请检查", filename, "信息")
                exit()
    else:
        json_data = json.loads(template_json_str)
    return json_data

def check_delay(mintime = 2, maxtime = 5):
    delay_time = random.randint(mintime, maxtime)
    print('等待 ', delay_time, ' 秒')
    time.sleep(delay_time)
    
def log_data(datapatch, logdata):
    datapatch = get_appsyspatch() + datapatch
    with open(datapatch, "a", encoding = 'utf-8') as f:
        for i in logdata:
            f.write(str(i) + "\n")

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
def sendDingDing(msg):
    xue_cfg = load_config(True)
    token = xue_cfg["useWS"]["DDtoken"]
    secret = xue_cfg["useWS"]["DDsecret"]
    ddhandler = DingDingHandler(token, secret)
    ddhandler.ddmsgsend(msg, "msg")

def load_logo():
    xue_logo = ("     ____  ___             ________    ________ "+ "\n" +
          r"     \   \/  /__ __   ____ \_____  \  /  _____/ " + "\n" +
          r"      \     /|  |  \_/ __ \ /  / \  \/   \  ___ " + "\n" +
          r"      /     \|  |  /\  ___//   \_/   \    \_\  \ " + "\n" +
          r"     /___/\  \____/  \___  >_____\ \_/\______  /" + "\n" +
          r"           \_/           \/       \__>       \/ ")
    #xue_logo = color.cyan(xue_logo)
    return xue_logo
