from func.common import *
from func.urls import *
from func.Xuecore import XCore
from func.score import *

def learn(model, cookies, scores):    
    course = get_study_scores(model, cookies)
    try:
        if course["num"] < course["num_max"] or course["time"] < course["time_max"]:
            learning = XCore(nohead=True)
            print(course["model"])
            learning.set_cookies(cookies)
            learn_links = get_links(model)
            all_links = len(learn_links)
            try_count = learn_time = 0

            while True:
                if try_count < 20:                
                    num_remain = course["num_max"] - course["num"]
                    time_remain = course["time_max"] - course["time"]
                    learn_remain = num_remain + time_remain
                    link_num = random.randint(1, all_links)
                    learning.get_url(learn_links[link_num]["url"])
                    print(course["title"] + learn_links[link_num]["title"])
                    print(course["publishTime"] + learn_links[link_num]["publishTime"])
                    print(course["url"] + learn_links[link_num]["url"])
                    
                    learn_time = 50 + random.randint(5, 15)
                    for i in range(learn_time):
                        if random.random() > 0.5:
                            learning.driver.execute_script('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(i))
                            time.sleep(1)
                        print("正在进行阅读学习中，剩余{}篇，本篇剩余时间{}秒".format(learn_remain, learn_time - i), end="\r", flush=True)
                    learning.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    print("\n")
                    course = get_study_scores(model, cookies, True)
                    try_count += 1
                    if course["num"] >= course["num_max"] and course["time"] >= course["time_max"]:
                        print("检测到本次阅读学习分数已满，退出学习")
                        break
            else:
                print("阅读学习出现异常，稍后可重新运行")
            learning.quit() 
        else:
            print(color.yellow("[*]") + course["end"]) 
    except Exception as e:
        print(color.red("阅读学习检测到异常："+str(e)))

def get_links(model):
    URID = random.randint(10000000,30000000)
    if model == "article":      
        learn_url = random.choice(article_url_list)
    elif model == "video":
        learn_url = random.choice(video_url_list)    
    else:
        print("@model error!")
        return "error"
    learn_list = []
    try:
        learn_json = requests.get(learn_url + "?_st=" + str(URID)).content.decode("utf8")
        learn_list = json.loads(learn_json)
        if(len(learn_list) > 600):
            learn_list = learn_list[:600]        
        return learn_list
    except:
        print("=" * 60)
        print("@文章列表获取失败")
        print("=" * 60)
        raise

def get_study_scores(model, cookies, show=False):
    if show == True:
        scores = show_userScore(cookies)
    else:
        scores = get_userScore(cookies)
    course = {}
    if model == "article":
        course["num"] = scores["article_num"]
        course["num_max"] = scores["article_num_max"]
        course["time"] = scores["article_time"]
        course["time_max"] = scores["article_time_max"]        
        course["model"] = "正在加载文章学习模块"
        course["title"] = "正在阅读文章: "
        course["publishTime"] = "文章发布时间: "
        course["url"] = "文章学习链接：\n"
        course["end"] = " 今天的文章学习已经完成，已退出"
        return course
    elif model == "video":
        course["num"] = scores["video_num"]
        course["num_max"] = scores["video_num_max"]
        course["time"] = scores["video_time"]
        course["time_max"] = scores["video_time_max"]
        course["model"] = "正在加载视频学习模块"
        course["title"] = "正在观看视频: "
        course["publishTime"] = "视频发布时间: "
        course["url"] = "视频学习链接：\n"
        course["end"] = " 今天的视频学习已经完成，已退出"
        return course
    else:
        print("@model error!")
        return None
