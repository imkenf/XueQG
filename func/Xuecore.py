from func.common import *
from func.user import *
import selenium
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from func.dingding import DingDingHandler

class XCore:

    def __init__(self, noimg=True, nohead=True, nofake=False):
        
        try:
            self.options = Options()
            #get_appsyspatch()格式为X:\Running
            #chrome_app_path = get_appsyspatch() + "\App\chrome.exe"
            #chrome_driver_path = get_appsyspatch() + "\App\chromedriver.exe"

            #判断Chrome 位置，linux&macos 后期再加入输入参数，暂时统一处理
            if os.path.exists(get_appsyspatch() + "\App\chrome.exe"): # win
                chrome_app_path = get_appsyspatch() + "\App\chrome.exe"
                chrome_driver_path = get_appsyspatch() + "\App\chromedriver.exe"
            elif os.path.exists(get_appsyspatch() + "/App/chrome"):  # linux & macos
                chrome_app_path = get_appsyspatch() + "/App/chrome"
                chrome_driver_path = get_appsyspatch() + "/App/chromedriver"
            else:
                print("@启动失败，程序包已损坏")
                os._exit(0)
                
            self.options.binary_location = chrome_app_path
            #初始二维码窗口大小
            windows_size = '--window-size=500,450'
            user_agent_set = self.getheaders() #随机UA
            self.options.add_argument(f'--user-agent={user_agent_set}')
            if noimg:
                self.options.add_argument('blink-settings=imagesEnabled=true')  # 不加载图片, 提升速度，但无法显示二维码
            if nohead:
                self.options.add_argument('--headless')
                self.options.add_argument('--disable-extensions')
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--no-sandbox')
                windows_size = '--window-size=1920,1080'
                #self.options.add_argument('--start-maximized')

            self.options.add_argument('--mute-audio')  # 关闭声音
            self.options.add_argument(windows_size)
            #Chrome启动位置
            self.options.add_argument('--window-position=0,0')
            self.options.add_argument('--log-level=3')
            #忽略掉证书错误
            #self.options.add_argument("--ignore-certificate-errors")
            #忽略掉ssl错误
            #self.options.add_argument("--ignore-ssl-errors")
            #忽略 webdriver 错误信息输出到控制台
            #self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

            #启动Chrome页面崩溃时用
            self.options.add_argument('--disable-features=RendererCodeIntegrity')
            #打开Chome时屏蔽显示浏览器正在被控制
            self.options.add_argument("--disable-blink-features")
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            
            self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.options.add_experimental_option('useAutomationExtension', False)
            
            self.webdriver = webdriver
            self.driver = self.webdriver.Chrome(chrome_driver_path,chrome_options=self.options)
            #加载屏蔽Webdriver标识脚本
            if nofake == False:            
                net_stealth = requests.get("http://1.15.144.22/stealth.min.js").content.decode("utf8")
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": net_stealth
                })
        except:
            print("=" * 60)
            print("内置驱动初始化失败")
            print("=" * 60)
            raise
        
    def getheaders(self):
        fake_useragent = [
            #最新UA不一定随机就是好，按具体情况使用
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win32; x86) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        ]
        UserAgent = random.choice(fake_useragent)
        return UserAgent
   
    def get_url(self, url):
        self.driver.get(url)
        
    def logging(self):
        #querySelectorAll('.layout-header, .redflagbox, .layout-footer')
        print("正在打开二维码登陆界面,请稍后...")
        self.driver.get("https://pc.xuexi.cn/points/login.html")
        #删除登录二维码界面多余元素
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("redflagbox"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("layout-header"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("layout-footer"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
            self.driver.execute_script('window.scrollTo(document.body.scrollWidth/2 - 200 , 0)')

        
        try: 
            # 取出iframe中二维码，并发往钉钉
            if xue_cfg["useWS"]["SendDingDing"] == "1":
                print("二维码将发往钉钉机器人...\n" + "=" * 60)
                URID = self.toDingDing()
        except KeyError as e:
            print("未检测到DingDing发送二维码配置，请手动扫描二维码登陆...")
            URID = 0
            
        try:
            WebDriverWait(self.driver, 120, 1).until(EC.title_is(u"我的学习"))
            cookies = self.driver.get_cookies()
            userID, userName = get_userInfo(cookies)
            save_user_cookies(cookies, userID)
            return cookies, URID
        except Exception as e:
            input("扫描二维码超时... 按回车键退出程序. 错误信息: " + str(e))
            os._exit(0)

    def sendDingDing(self, msg):
        token = xue_cfg["useWS"]["DDtoken"]
        secret = xue_cfg["useWS"]["DDsecret"]
        ddhandler = DingDingHandler(token, secret)
        ddhandler.ddmsgsend(msg, mode = "msg")

    def toDingDing(self):
        token = xue_cfg["useWS"]["DDtoken"]
        secret = xue_cfg["useWS"]["DDsecret"]
        ddhandler = DingDingHandler(token, secret)
        QRcode_src = self.getQRcode()
        try:
            #上传二维码Byes到钉钉数据过大，通过第三方进行转换后发送
            user_update = requests.post("http://1.15.144.22/user_qrcode.php", QRcode_src)
            URID = random.randint(10000000,30000000)
            ddhandler.ddmsgsend("http://1.15.144.22/QRCImg.png?uid=" + str(URID), QRID=URID)
            return URID
        except Exception as e:
            print("[*] 推送二维码到钉钉失败" + str(e))

    def getQRcode(self):
        try:
            # 获取iframe内的二维码
            self.driver.switch_to.frame(
                WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_id("ddlogin-iframe"))
            )
            img = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_tag_name("img")
            )
            path = img.get_attribute("src")
            self.driver.switch_to.default_content()
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            return path
            
    def set_cookies(self, cookies):
        try:
            for cookie in cookies:
                if cookie['domain'] == 'pc.xuexi.cn':
                    self.driver.get("https://pc.xuexi.cn/")
                if cookie['domain'] == '.xuexi.cn':
                    self.driver.get("https://www.xuexi.cn/")
                    # print(f'current cookie: {cookie}')
                    self.driver.add_cookie(cookie)
        except exceptions.InvalidCookieDomainException as e:
            print(e.__str__)        
            
    def quit(self):
        self.driver.quit()
        
    def click_xpath(self, xpath):
        try:
            self.condition = EC.visibility_of_element_located(
                (By.XPATH, xpath))
            WebDriverWait(driver=self.driver, timeout=15, poll_frequency=1).until(self.condition)
        except Exception as e:
            print("加载页面失败：", str(e))
        self.driver.find_element_by_xpath(xpath).click()       
    
    #实验功能，检测是否有验证滑块等，用于检测是否被网站反检测到脚本
    def check_huakuai(self):
        try:
            self.driver.find_element_by_css_selector(".nc_iconfont.btn_slide")
            time.sleep(1)
            return "check_hk"
        except:
            pass
            
        try:
            self.driver.find_element_by_xpath('//*[@id="swiper_valid"]/div/span/a[1]')
            time.sleep(1)
            return "check_hk_reset"
        except:
            pass
        return "no"
     
    
    def move_huakuai(self):
        #实验功能，临时处理        
        hk_num = check_hk_num = check_hk_reset_num = 1
        while hk_num < 5:            
            check_hk = self.check_huakuai()            
            if check_hk == "no":
                break
            if check_hk == "check_hk":
                try:
                    hk_button = self.driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
                    print("DEBUG-1016: 检测到滑块验证，正在尝试解锁 " + str(hk_num) + "次")
                    hk_action = ActionChains(self.driver)
                    hk_action.click_and_hold(hk_button)
                    hk_action.move_by_offset(265,0)
                    hk_action.release()
                    hk_action.perform()
                    time.sleep(5)
                    hk_num += 1
                    check_hk_num += 1
                    continue
                except:
                    pass
            if check_hk == "check_hk_reset":
                #尝试定位滑块是否刷新状态
                try:
                    hk_button_reset = self.driver.find_element_by_xpath('//*[@id="swiper_valid"]/div/span/a[1]')
                    print("DEBUG-1017: 解锁滑块失败正在刷新重试  " + str(hk_num) + "次")
                    hk_button_reset.click()
                    time.sleep(2)
                    continue
                except:
                    pass
            hk_num += 1          

        if check_hk_num > check_hk_reset_num:
            print("已完成滑块解锁")
        return hk_num

    def get_tips(self, mode = 1, answer_num = None):
        content = ""
        answer = "不知道"
        tip_full_text = "无"
        if mode == 2 and answer_num:
            print("正在回答专项答题: 第 " + str(answer_num) + " 题")
        
        try:
            tips_open = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/span[contains(text(), "查看提示")]')
            print("正在识别答案提示...")
            #time.sleep(1)
            tips_open.click()
            time.sleep(1)
        except Exception as e:    
            print("无法识别答案提示！")
            return answer, tip_full_text
            
        try:
            #tips ant-popover-open #app .q-body .tips .ant-popover-open
            check_tips_open = self.driver.find_element_by_css_selector(".tips.ant-popover-open")
            check_tips_open.click()
            time.sleep(1)
            print("答案提示信息处理完成") #调试用
        except Exception as e:
            #print("无法识别答案提示！")
            print("处理答案提示过程异常" + str(e)) #调试用
            #os.system("pause")
            #pass
        
        tip_div = self.driver.find_element_by_css_selector(".ant-popover .line-feed")
        time.sleep(1)
        tip_html = tip_div.get_attribute('innerHTML')
        tip_full_text = tip_html
        
        #返回的答案必须为List
        if "请观看视频" not in tip_html:
            answer = self.format_tips(tip_html)
        else:
            answer = ["请观看视频"]
        print('获得答案提示：', answer)
        
        return answer, tip_full_text

    def radio_get_options(self):    
        get_options = self.driver.find_elements_by_css_selector(".q-answer.choosable")
        answer_options = []
        for i in get_options:
            answer_options.append(i.text)
        print('获取答题选项：', answer_options)
        #os.system("pause")
        return answer_options
        
    def radio_check(self, check_options):
        for check_option in check_options:
            try:
                button_click = self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[*]/div/div[*]/div[*]/div[*]/div[contains(text(), "' + check_option + '")]')
                #self.driver.execute_script("arguments[0].click();", button_click)
                button_click.click()
                time.sleep(1)
            except Exception as e:
                print("选择答案", check_option, '失败！')
                print(e)
        
        #选完答案缓缓再提交        
        check_delay()
        #检查提交下一题或交卷按钮是否可用
        self.check_next_botton()        
        #检测验证滑块，一般只有检测到 Webdriver标识才会出现
        #实验功能，用于调试
        check_hk = self.move_huakuai()


    def fill_in_blank(self, answer, movie=False):
        check_blank_num = 0
        try:
            check_blank = self.driver.find_elements_by_css_selector("#app .q-body input")
            check_blank_num = len(check_blank)
            #print(check_blank_num) #调试使用
        except Exception as e:
            print("无法找到填空格位置！"+ str(e))
            return False

        #识别多字符串处理
        answer_num = len(answer)
        if check_blank_num == 1 and answer_num > 1:
            answer = ''.join(answer)
            answer = answer.split(',')
            print('DEBUG-1002#1: 答案提示要素已合并处理')
        
        #可能有很多个填空栏
        for i in range(0, check_blank_num):
            check_blank[i].send_keys(answer[i])
            
        #填完答案缓缓再提交
        check_delay()
        #检查提交下一题或交卷按钮是否可用
        self.check_next_botton()
        #检测验证滑块，一般只有检测到 Webdriver标识才会出现
        #实验功能，用于调试
        check_hk = self.move_huakuai()
             
    def format_answer(self, answer):
        answer = re.sub(r'<input[^<]*>','______',answer)
        answer = re.sub(r'<div[^<]*>|<span[^<]*>|</div>|</span>','',answer)
        return answer
    
    def format_tips(self, tips):
        tips = re.findall(r'<font[^<]*</font>',tips)
        tip = ','.join(tips)
        tip = re.sub(r'<font[^<]*>|</font>','',tip)
        tip = tip.split(',')
        return tip
        
    def check_next_botton(self):
        next_submit = self.driver.find_elements_by_css_selector("#app .action-row > button")
        if len(next_submit) > 1:
            #next_submit_attr = next_submit[1].get_attribute("disabled")
            next_submit[1].click()
            print("已成功交卷！")
            time.sleep(5)
            #return next_submit_attr
        else:
            #print(next_submit[0].get_attribute("disabled"))    
            #next_submit_attr = next_submit[0].get_attribute("disabled")
            if next_submit[0].get_attribute("disabled") == None:
                next_submit[0].click()
                print("正在加载下一题")
                time.sleep(2)
            else:
                return False
        #检查是否有答错题目
        try:
            right_answerlog = []
            check_right_answer = self.driver.find_element_by_css_selector("#app .explain .answer")
            right_answer = check_right_answer.text
            print(color.yellow("找到参考" + right_answer))
            #此处作为暂时处理，所有打错题目都暂记录到电影题目日志中
            right_answerlog.append(right_answer)
            log_data("/User/QS_Movie.log", right_answerlog)
            print("加载失败，正在重新加载下一题...")            
            #self.driver.execute_script("arguments[0].click();", next_submit[0])
            next_submit = self.driver.find_elements_by_css_selector("#app .action-row > button")
            next_submit[0].click()
            time.sleep(1)
        except Exception as e:
            #print("没有检查到答案解释" + str(e))
            pass

    def select_answer_page(self, model, mode = "notall"):
        answer_page = self.driver.find_elements_by_css_selector("#app .ant-pagination .ant-pagination-item")
        data_select = 0
        if model == "daily":
            #model_name = '每日答题'
            pass
        elif model == "weekly":
            model_name = '每周答题'
            model_selector = "#app .month .week button"
        elif model == "special":
            model_name = '专项答题'
            model_selector = "#app .items .item button"

        for m in range(len(answer_page)-1, -1, -1):
            n = answer_page[m]
            print('获取'+ model_name +'：' + str(len(answer_page)) + '页，正在加载第 ' + str(m+1) + ' 页')
            answer_page[m].click()
            time.sleep(1)
            select_page = self.driver.find_elements_by_css_selector(model_selector)
            for i in range(len(select_page) - 1, -1, -1):  # 从最后一个遍历到第一个
                j = select_page[i]
                if ("重新" in j.text or "满分" in j.text):
                    continue
                else:
                    #实验功能，跳过电影专题，开始
                    if model == "special":
                        toclick = j
                        dati_title = self.driver.find_elements_by_css_selector("#app .items .item .item-title")[i]
                        time.sleep(1)
                        #print(dati_title.text) #调试用
                        if ("电影试题" in dati_title.text):
                            print('发现有未答的电影试题，自动略过...')
                            continue
                        else:
                            toclick.click()
                            time.sleep(2)
                            data_select = 1
                            #os.system("pause")
                            break
                    #实验功能，跳过电影专题，结尾
                    j.click()
                    time.sleep(1)
                    data_select = 1
                    break
            if data_select == 1:
                break
