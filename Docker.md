# Docker 地址<br>
**2022.01.01更新稳定版**<br>
> **获取docker镜像**<br>
`docker pull imkenf/xueqg`

> **运行方式一：不保留用户记录**<br>
`用 -e 添加程序参数`（按需要）<br>
**钉钉例子：**<br>
> `docker run -e ModeType=3 -e PushMode=2 -e DDtoken=123456 -e DDsecret=123456 --rm imkenf/xueqg`<br>
**PlusPush例子：**<br>
> `docker run -e ModeType=3 -e PushMode=3 -e PPtoken=123456 --rm imkenf/xueqg`<br><br>

> **运行方式二：保留用户记录（推荐）**<br>
**钉钉例子：**<br>
首次运行命令<br>
> `docker run -it --name=xueqg -e ModeType=3 -e PushMode=2 -e DDtoken=123456 -e DDsecret=123456 imkenf/xueqg`<br>
正常运行命令<br>
> `docker start xueqg -i`<br>
注意：首次运行命令创建容器后，参数以首次命令输入参数为准，如需要创建多个容器，可以修改--name 参数名称
<br>

> **参数说明：**（更多说明请查看User目录下的Config文件）<br>
`ModeType = 4` **（必选参数）**<br>
① 文章 + 视频<br>
② 文章 + 视频 + 每日答题<br>
③ 文章 + 视频 + 每日答题 + 每周答题 + 专项答题<br>
④ 文章 + 每日答题 + 专项答题（★默认）<br>
⑤ 更新用户Cookie信息 <br><br>
`SetUser = 1` （可选参数）<br>
指定登录用户序号（本地保存的用户序号）<br>
此参数读取本地保存的用户序号，如设置此参数，请用方式二命令运行，且需删除`--rm`此项命令参数<br><br>
`PushMode = 1` **（必选参数）**<br>
消息推送模式，1表示 内置消息接口（默认企业微信，可配置各种类型），2表示 钉钉，3表示 PlusPush，0表示 不开启<br><br>
**推送消息接口说明：**<br>
内置消息接口配置说明（待更新）<br>
钉钉机器人接入方式请参考 https://developers.dingtalk.com/document/app/custom-robot-access/title-72m-8ag-pqw<br>
PlusPush接入参考 https://www.pushplus.plus/doc/guide/api.html<br>
对于PlusPush，只需要填写token，而钉钉机器人需要填写token和secret<br>
为了切换推送平台省事，每个平台保留参数设置，设置哪个推送模式就哪个参数生效<br><br>
以下参数根据PushMode配置，3选1即可<br>
钉钉机器人Token参数<br>
`DDtoken = 123456`<br>
`DDsecret = 123456`<br><br>
PlusPush Token参数<br>
`PPtoken = 123456`<br><br>
企业微信Token参数，可登录企业微信管理后台获取<br>
自建应用ID<br>
`WXagentid = 1000000`<br>
企业微信ID<br>
`WXcorpid = 123456`<br>
自建应用 Secret<br>
`WXcorpsecret = 123456`
<br>

> **注意**<br>
> Docker 版本需配合推送平台接收登录二维码使用<br>

> **群晖用户**<br>
> 在参数配置选项需添加`ModeType`、`PushMode`、`SetUser`以及推送接口参数
