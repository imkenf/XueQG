<div>
  <img width="128" height="128" align="left" src="./img/Icon.png" alt="XueQG"/>
  <h1>XueQG</h1>
  <p>QG学习助手，和您一同学习进步，自用<br> 每天稳定学习45+分<br> 全类型题目答题，多种类文章学习，二维码登录发送等</p>
</div>

> 学习过程中有题目和答题选项展示，同时记录相关题目信息到本地User目录以便复习之用

> 目前版本经长期测试，稳定学习，内置打包Chrome最新版浏览器驱动，后台无界面调用

[![Downloads](https://img.shields.io/github/downloads/imkenf/XueQG/total.svg?style=flat-square&color=0f6adb)](https://github.com/imkenf/XueQG/releases/latest)
[![GitHub issues](https://img.shields.io/github/issues/imkenf/XueQG?style=flat-square&color=0f6adb)](https://github.com/imkenf/XueQG/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/imkenf/XueQG?style=flat-square&color=0f6adb)](https://github.com/imkenf/XueQG/graphs/contributors)


# 说明
欢迎加入讨论组
https://t.me/learnqg
<br>
**2021.10.20 更新分数接口，请务必更新才能正常使用**

> 展示版本为Win64版本，如需Liunx运行，请自行打包对应版本Chrome
<br>最低系统要求`Windows7 64Bit及以上`

> 学习界面演示

<img src="https://raw.githubusercontent.com/imkenf/Xue/main/0001.jpg" width="65%">
<br>
<img src="./img/DD1.png">

# Docker 地址<br>
**2021.11.4更新稳定版**<br>
> **获取docker镜像**<br>
`docker pull imkenf/xueqg`

> **参数说明：**<br>
`PushMode = 1`<br>
消息推送模式，1表示 内置消息接口，2表示 钉钉，3表示 PlusPush，0表示 不开启<br>
钉钉机器人接入方式请参考 https://developers.dingtalk.com/document/app/custom-robot-access/title-72m-8ag-pqw<br>
PlusPush接入参考 https://www.pushplus.plus/doc/guide/api.html<br>
对于PlusPush，只需要填写token，而钉钉机器人需要填写token和secret<br>
为了切换推送平台省事，每个平台保留参数设置，设置哪个推送模式就哪个参数生效<br>
钉钉机器人参数<br>
`DDtoken = 123456`<br>
`DDsecret = 123456`<br>
PlusPush token 参数<br>
`PPtoken = 123456`<br>
企业微信参数，可登录企业微信管理后台获取<br>
自建应用ID<br>
`WXagentid = 1000000`<br>
企业微信ID<br>
`WXcorpid = 123456`<br>
自建应用 Secret<br>
`WXcorpsecret = 123456`

> **运行方式**<br>
`-e 添加上述参数`（按需要）<br>
钉钉例子：<br>
> `docker run -e ModeType=3 -e PushMode=1 -e DDtoken=123456 -e DDsecret=123456 --rm imkenf/xueqg`<br>

> **注意**<br>
> Docker 版本需配合推送平台接收登录二维码使用

# 免责声明
使用需严格遵守开源许可协议。本项目仅限于程序开发学习交流之用，严禁用于商业用途，禁止使用本项目进行任何盈利活动。对一切非法使用所产生的后果，我们概不负责。

# 鸣谢
参考源码项目来自https://github.com/TechXueXi/TechXueXi
