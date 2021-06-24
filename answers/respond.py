from func.urls import *
from func.Xuecore import XCore
from func.score import *


def respond(model, cookies, scores):
    score = {}
    score["mypoints_url"] = "https://pc.xuexi.cn/points/my-points.html" #我的分数
    
    if model == "daily":
        score["now"] = scores["daily"]
        score["max"] = scores["daily_max"]
        score["loading_model"] = "正在加载每日答题网页模块，请稍等..."
        score["loaded_model"] = "已加载每日答题模块"        
        score["model_xpath"] = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div' #每日答题的 答题按钮
    
    elif model == "weekly":
        score["now"] = scores["weekly"]
        score["max"] = scores["weekly_max"]
        score["loading_model"] = "正在加载每周答题网页模块，请稍等..."
        score["loaded_model"] = "已加载每周答题模块"
        score["model_xpath"] = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div' #每周答题的 答题按钮
    
    elif model == "special":
        score["now"] = scores["special"]
        score["max"] = scores["special_max"]
        score["loading_model"] = "正在加载专项答题网页模块，请稍等..."
        score["loaded_model"] = "已加载专项答题模块"
        score["model_xpath"] = '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div' #专项答题的 答题按钮
    
        
    if score["now"] < score["max"]:
    
        respond_drv = XCore(nohead=True)
        respond_drv.set_cookies(cookies)
        
        try_count = 1
        check_button_next_num = 0
        letters = list("ABCDEFGHIJKLMN")
        #正在加载模块
        print(score["loading_model"])
        #模块入口网页
        respond_drv.get_url(score["mypoints_url"])
        #respond_drv.driver.find_element_by_xpath(score["model_xpath"])
        respond_drv.click_xpath(score["model_xpath"])
        time.sleep(1)
        #加载模块完成
        print(score["loaded_model"])
        
        #检测答题模块页码
        #try:
            #if xue_cfg["base"]["checkallEQ"] == 1:
                #respond_drv.select_answer_page(model, "all")
        #except:
            #respond_drv.select_answer_page(model)            
        respond_drv.select_answer_page(model)
        
        while True:
            #检测是否还在题目中, 通过按钮判断是否答题未提交
            try:
                button_xpath = respond_drv.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[2]/button')
                #如果出现滑块验证且无法解锁情况下，无法提交成功
                if button_xpath.is_enabled() == True and check_button_next_num < 3:
                    try:
                        print("检测到答案未成功提交，重新提交中")
                        button_xpath.click()
                        time.sleep(1)
                    except Exception as e:
                        print("提交答案操作失败: " + str(e))
                    check_button_next_num += 1
                    continue
            except Exception as e:
                if check_button_next_num >= 3:
                    print("检测到答案无法提交，此次答题已中断！")
                    break
            #获取题目类型
            try:
                category = respond_drv.driver.find_element_by_css_selector("#app .detail-body .q-header").text
                time.sleep(1)
            except Exception as e:
                print("DEBUG-1001#1: 没有找到题目类型元素") #+ str(e))
                #os.system("pause")
                break
            #获取题目
            try:
                q_body = respond_drv.driver.find_element_by_css_selector("#app .q-body")
                time.sleep(1)
            except Exception as e:
                print("DEBUG-1001#2: 没有找到题目问题元素")
                break
            #获取每周答题和专项答题题目名称
            if model == "special" or model == "weekly":
                try:
                    title_name = respond_drv.driver.find_element_by_css_selector("#app .header-row .title")
                    #time.sleep(1)
                    print('正在进行： ' + title_name.text + ' 第 ' + str(try_count) + ' 题')
                except Exception as e:
                    print(e)
                    print('获取答题标题失败！')
                
            #获取题目框架html
            q_log = []
            q_html = q_body.get_attribute('innerHTML')
            q_text = respond_drv.format_answer(q_html)
            #打印题目类型
            print("★" + category)
            #打印题目
            print(q_text)
            
            #保存题目日志
            q_log.extend(("\n=====================", 
                        get_time(), 
                        "【"+category+"】",
                        "【题干】",
                        q_html,
                        "【提示信息】"))
                                
            #获取答题提示
            tips, tip_full_text = respond_drv.get_tips()
            
            #保存答题提示日志
            q_log.extend((tips, tip_full_text))
            
            #开始答题
            if "填空题" in category:
                if "请观看视频" in tips:
                    #必须为List
                    answer = mv_log = []
                    answer.append("不知道")
                    print("DEBUG-1001#3: 检测到观影题目，正在尝试答题...")
                    print(color.red("AI程序还没学会看电影，暂时自动回答: 不知道"))
                    mv_log = []
                    #另外记录视频题目，以后再说
                    #答案另外记录
                    mv_log.extend(("\n=====================", 
                                   get_time(), 
                                   "【"+category+"】（视听题）",
                                   "【题干】",
                                   q_html))
                    #注意视频答题框位置和普通答题位置不一样
                    #respond_drv.fill_in_blank(answer, movie=True)
                    respond_drv.fill_in_blank(answer)
                    log_data("/User/QS_Movie.log", mv_log)
                else:
                    answer = tips
                    respond_drv.fill_in_blank(answer)
                    log_answer(model, q_log)
                try_count += 1
            elif "多选题" in category:
                options = respond_drv.radio_get_options()
                q_log.extend(("【多选题选项】", options))
                radio_in_tips, radio_out_tips = "", ""
                for letter, option in zip(letters, options):
                    for tip in tips:
                        if tip in option:
                            # print(f'{option} in tips')
                            if letter not in radio_in_tips:
                                radio_in_tips += letter
                radio_out_tips = [letter for letter, option in zip(letters, options) if(letter not in radio_in_tips)]
                print('包含提示的选项 ', radio_in_tips, '，不包含提示的选项 ', radio_out_tips)
                q_log.extend(("包含提示的选项 "+ str(radio_in_tips), "不包含提示的选项 " + str(radio_out_tips)))
                log_answer(model, q_log)
                
                if len(radio_in_tips) > 1:  # and radio_in_tips not in respond_drv.excludes:
                    print('根据提示', radio_in_tips)
                    respond_drv.radio_check(radio_in_tips)
                elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                    print('根据提示', radio_out_tips)
                    respond_drv.radio_check(radio_out_tips)
                    # return respond_drv._search(content, options, excludes)
                else:
                    print('无法根据提示判断，正在继续答题……')
                
                try_count += 1    
            elif "单选题" in category:
                options = respond_drv.radio_get_options()
                q_log.extend(("【单选题选项】", options))
                if '因此本题选' in tips: #提示类型1
                    check = [x for x in letters if x in tips]
                    #log_daily("根据提示类型1，选择答案："+str(check))
                    respond_drv.radio_check(check)
                else:                    
                    radio_in_tips, radio_out_tips = "", ""
                    for letter, option in zip(letters, options):
                    
                        for tip in tips:
                            if tip in option:
                                # print(f'{option} in tips')
                                if letter not in radio_in_tips:
                                    radio_in_tips += letter
                            else:
                                # print(f'{option} out tips')
                                if letter not in radio_out_tips:
                                    radio_out_tips += letter

                    #如果因特殊字符分隔答案的情况或多个关键字答案情况，进行合并操作
                    if len(radio_in_tips) > 1:
                        for check_radio_in in radio_in_tips:
                            if check_radio_in not in radio_out_tips:
                                radio_in_tips = check_radio_in
                                break

                    print('包含提示的选项 ', radio_in_tips, '，不包含提示的选项 ', radio_out_tips)
                    q_log.extend(("包含提示的选项 "+ str(radio_in_tips), "不包含提示的选项 " + str(radio_out_tips)))
                    log_answer(model, q_log)
                    if 1 == len(radio_in_tips):  # and radio_in_tips not in respond_drv.excludes:
                        print('根据提示', radio_in_tips)
                        respond_drv.radio_check(radio_in_tips)
                    elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                        print('根据提示', radio_out_tips)
                        respond_drv.radio_check(radio_out_tips)
                        # return respond_drv._search(content, options, excludes)
                    else:
                        print(color.red('无法根据提示判断，自动选择 A选项'))                        
                        respond_drv.radio_check("A")
                try_count += 1
        scores = show_userScore(cookies)
        print("完成此次答题，正在退出...")
            
def log_answer(logtype, logdata):
    if logtype == "daily":
        datapatch = "/User/QS_Daily.log"
    elif logtype == "weekly":
        datapatch = "/User/QS_Weekly.log"
    elif logtype == "special":
        datapatch = "/User/QS_Special.log"
    log_data(datapatch, logdata)
    
