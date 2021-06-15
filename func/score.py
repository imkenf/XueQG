from func.common import *
from func.urls import *

def get_userScore(cookies):
    jar = RequestsCookieJar()
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])
        
    #获取当前用户总分API
    user_totalScore_json = requests.get(user_totalScore_url, cookies=jar, headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    userInfo_totalScore = int(json.loads(user_totalScore_json)["data"]["score"])
    #获取当前用户今天已取得分API
    user_todayTotalScore_json = requests.get(user_todayTotalScore_url, cookies=jar, headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    userInfo_todayTotalScore = int(json.loads(user_todayTotalScore_json)["data"]["score"])
    #获取当前用户今天学习分数API
    user_rateScore_json = requests.get(user_rateScore_url, cookies=jar, headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
    userInfo_rateScore = json.loads(user_rateScore_json)["data"]["dayScoreDtos"]
    
    rule_list = [1, 2, 9, 1002, 1003, 6, 5, 4] #显示得分模块
    score_list= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #获取今天得分列表
    score_max = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #获取今天得分上限列表
    for i in userInfo_rateScore:
       for j in range(len(rule_list)):
            if i["ruleId"] == rule_list[j]:
                score_list[j] = int(i["currentScore"])
                score_max[j] = int(i["dayMaxScore"])
            
    # 阅读文章，视听学习，登录，文章时长，视听学习时长，每日答题，每周答题，专项答题
    userInfo_scores = {}
    userInfo_scores["article_num"]  = score_list[0] # 0阅读文章
    userInfo_scores["video_num"]    = score_list[1] # 1视听学习
    userInfo_scores["login"]        = score_list[2] # 7登录
    userInfo_scores["article_time"] = score_list[3] # 6文章时长
    userInfo_scores["video_time"]   = score_list[4] # 5视听学习时长
    userInfo_scores["daily"]        = score_list[5] # 2每日答题
    userInfo_scores["weekly"]       = score_list[6] # 3每周答题
    userInfo_scores["zhuanxiang"]   = score_list[7] # 4专项答题
    
    userInfo_scores["today"] = userInfo_todayTotalScore # 今日得分
    userInfo_scores["total"] = userInfo_totalScore      # 总分
    
    userInfo_scores["article_num_max"]  = score_max[0] # 0阅读文章
    userInfo_scores["video_num_max"]    = score_max[1] # 1视听学习
    userInfo_scores["login_max"]        = score_max[2] # 7登录
    userInfo_scores["article_time_max"] = score_max[3] # 6文章时长
    userInfo_scores["video_time_max"]   = score_max[4] # 5视听学习时长
    userInfo_scores["daily_max"]        = score_max[5] # 2每日答题
    userInfo_scores["weekly_max"]       = score_max[6] # 3每周答题
    userInfo_scores["zhuanxiang_max"]   = score_max[7] # 4专项答题
    
    return userInfo_scores

def show_userScore(cookies):
    #userInfo_totalScore, userInfo_scores = get_userScore(cookies)
    print("当前学习总积分：" + str(userInfo_scores["total"]) + "\t" + "今日得分：" + str(userInfo_scores["today"]))
    print("阅读文章:", userInfo_scores["article_num"], "/", userInfo_scores["article_num_max"], ",",
        "视听学习:", userInfo_scores["video_num"], "/", userInfo_scores["video_num_max"], ",",
        "文章时长:", userInfo_scores["article_time"], "/", userInfo_scores["article_time_max"], ",",
        "视听时长:", userInfo_scores["video_time"], "/", userInfo_scores["video_time_max"], ",",
        "\n每日登陆:", userInfo_scores["login"], "/", userInfo_scores["login_max"], ",",
        "每日答题:", userInfo_scores["daily"], "/", userInfo_scores["daily_max"], ",",
        "每周答题:", userInfo_scores["weekly"], "/", userInfo_scores["weekly_max"], ",",
        "专项答题:", userInfo_scores["zhuanxiang"], "/", userInfo_scores["zhuanxiang_max"])
    return userInfo_scores
