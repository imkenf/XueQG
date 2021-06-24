import os, time, math
from func.Xuecore import XCore
from func import score, user, version, threads
from study import reader
from answers.respond import *

if __name__ == '__main__':

    #初始化，读取配置文件
    start_time = time.time()
    xue_cfg = load_config()
    QRID = 0
    
    if(xue_cfg['display']['banner'] != "false"):
        print("=" * 60 + \
        '\n使用本项目，必须接受以下内容，否则请立即退出：' + \
        '\n   - 仅额外提供给“爱党爱国”且“工作学业繁重”的人' + \
        '\n   - 此项目运行过程中自动记录学习内容，可过后再次学习' + \
        '\n   - 项目开源协议 LGPL-3.0' + \
        '\n   - 仅限内部交流，不允许外传' + \
        '\n   - 不得利用本项目盈利' + 
        "\n" + "=" * 60)
    #获取版本更新信息
    version_thread = threads.MyThread("获取版本更新信息", version.up_info)
    version_thread.run()
  
    #读取用户登录信息Cookie
    cookies = user.check_user_cookie()
    user_list = user.list_user()
    if user_list == 1:
        cookies = user.check_user_cookie()

    if not cookies or user_list == 2:
        print("\n未找到有效登录信息，需要登录。按任意键继续")
        os.system("pause")
        driver_login = XCore(nohead=False)
        cookies, QRID = driver_login.logging()
        driver_login.quit()
    

    uid, nick = user.get_userInfo(cookies)
    user.update_last_user(uid)
    #查询用户今天分数
    scores = score.show_userScore(cookies)    
    #学习情况发送到钉钉
    try:
        if xue_cfg["useWS"]["SendDingDing"] == "1":
            if QRID == 0:
                QRmsg = ""
            else:
                QRmsg = "\n > ###### 使用二维码ID:" + str(QRID)
            #QRmsg = "###### 使用二维码ID:" + str(QRID)
            send_msg = "#### " + nick + "开始学习" + \
                    "\n > ##### 目前学习总积分: " + str(scores["total"]) + "\t今日得分: " + str(scores["today"]) + \
                    "\n > ###### 阅读文章: " + str(scores["article_num"]) + "/" + str(scores["article_num_max"]) + \
                    ", 视听学习:" + str(scores["video_num"]) + "/" + str(scores["video_num_max"]) + \
                    "\n > ###### 文章时长: " + str(scores["article_time"]) + "/" + str(scores["article_time_max"]) + \
                    ", 视听时长:" + str(scores["video_time"]) + "/" + str(scores["video_time_max"]) + \
                    "\n > ###### 每日答题: " + str(scores["daily"]) + "/" + str(scores["daily_max"]) + \
                    ", 每日登陆:" + str(scores["login"]) + "/" + str(scores["login_max"]) + \
                    "\n > ###### 每周答题: " + str(scores["weekly"]) + "/" + str(scores["weekly_max"]) + \
                    ", 专项答题:" + str(scores["special"]) + "/" + str(scores["special_max"]) + \
                    QRmsg
            sendDingDing(send_msg)
    except Exception as e:
        pass
    print("=" * 60, '\n本程序 现支持以下模式（如未达到当日满分状态可重新运行）')
    print(xue_cfg['base']['ModeText'] + '\n' + "-" * 60) # 模式提示文字请在 ./config/config.cfg 处修改。
    try:
        if xue_cfg["base"]["ModeType"] is not None:
            print("读取到配置文件...选择模式: " + xue_cfg["base"]["ModeType"])
            XueQG_mode = xue_cfg["base"]["ModeType"]
    except Exception as e:
        XueQG_mode = input("请选择模式（输入对应数字）并回车: ") or 2
        
    
    print(xue_cfg['base']['multiThreadingText'] + '\n' + "-" * 60) 
    try:
        if xue_cfg["base"]["multiThreading"]:
            print("读取到配置文件...选择模式: " + xue_cfg["base"]["multiThreading"])
            print("=" * 60)
            multiThreading_mode = xue_cfg["base"]["multiThreading"]
    except Exception as e:
        multiThreading_mode = input("请选择模式（输入对应数字）并回车: ") or 1
        print("=" * 60)
           
    article_thread = threads.MyThread("文章学习", reader.learn, "article", cookies, scores)
    video_thread = threads.MyThread("视频学习", reader.learn, "video", cookies, scores)

    if XueQG_mode in ["1", "2", "3"]:
        #文章学习线程模式
        #print(article_thread.enumerate())
        if multiThreading_mode == "2" or multiThreading_mode == 2:
            #print("DEBUG:" + multithreading_mode)
            article_thread.start()
            time.sleep(2)
            video_thread.start()
            time.sleep(1)
            #Join
            article_thread.join()
            time.sleep(1)
            video_thread.join()
        else:
            article_thread.run()
            video_thread.run()   
        
    if XueQG_mode in ["2", "3", "4"]:
        print(color.yellow("[*]") + ' 开始每日答题……')
        respond("daily", cookies, scores)
    if XueQG_mode in ["3","4"]:
        if scores["weekly"] == 0:
            print(color.yellow("[*]") + ' 开始每周答题……')
            respond("weekly", cookies, scores)
        elif scores["weekly_max"] > scores["weekly"] > 0 :
            print(color.magenta("[*]") +' 检测到今天每周已答题但未满分，已退出')
        elif scores["weekly_max"] == scores["weekly"]:
            print(color.yellow("[*] ") + "每周答题已经满分")
        
        if scores["special"] == 0:
            print(color.yellow("[*]") +' 开始专项答题……')
            respond("special", cookies, scores)
        elif scores["special_max"] > scores["special"] > 0 :
            print(color.magenta("[*]") +' 检测到今天专项已答题但未满分，已退出')
        elif scores["special_max"] == scores["special"]:
            print(color.yellow("[*] ") + "专项答题已经满分")

    
    #已在答题中执行刷新分数
    scores = score.get_userScore(cookies)
    #学习结束情况发送到钉钉
    try:
        if xue_cfg["useWS"]["SendDingDing"] == "1":    
            send_msg = "#### " + nick + "学习结束 \n > ##### 学习总积分: " + str(scores["total"]) + "\t今日得分: " + str(scores["today"]) + \
                    "\n > ###### 阅读文章: " + str(scores["article_num"]) + "/" + str(scores["article_num_max"]) + \
                    ", 视听学习:" + str(scores["video_num"]) + "/" + str(scores["video_num_max"]) + \
                    "\n > ###### 文章时长: " + str(scores["article_time"]) + "/" + str(scores["article_time_max"]) + \
                    ", 视听时长:" + str(scores["video_time"]) + "/" + str(scores["video_time_max"]) + \
                    "\n > ###### 每日答题: " + str(scores["daily"]) + "/" + str(scores["daily_max"]) + \
                    ", 每日登陆:" + str(scores["login"]) + "/" + str(scores["login_max"]) + \
                    "\n > ###### 每周答题: " + str(scores["weekly"]) + "/" + str(scores["weekly_max"]) + \
                    ", 专项答题:" + str(scores["special"]) + "/" + str(scores["special_max"])            
            sendDingDing(send_msg)
    except Exception as e:
        pass            
            
    seconds_used = int(time.time() - start_time)
    print("总计用时 " + str(math.floor(seconds_used / 60)) + " 分 " + str(seconds_used % 60) + " 秒")
    print("本次学习已执行完成，2分钟后窗口将自动关闭")
    os.system("timeout 120")
