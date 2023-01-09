# MC_QQ 数据库版本 测试版

> 提示： 该版本没有经过充分测试, 不建议在生产环境使用, 如果发现任何问题请自行解决，  
> 或  
> 提交 [Issues](https://github.com/17TheWord/nonebot-plugin-mcqq/issues) （因个人能力有限不保证百分百解决）。

在原有功能上加入了动态数据

## 改动

使用 `tortoise-orm` 及 `sqlite` 数据库存储数据

数据库参考 [`HarukaBot`](https://github.com/SK-415/HarukaBot)

数据库文件会在 `Bot` 的 `src` 目录下生成，名为 `mcqq.sqlite3`

## 安装

注意！若使用该版本，请务必对各个MC服务器设置**不同**的服务器名，即使只有一个MC服务器

暂时只支持 **纯插件** 版本的安装方式，不支持 `Rcon`

手动下载该分支 `git` 文件，将 `mcqq_sql` 放入 `Bot` 的 `plugins`

- 需要手动安装的依赖
    - `websockets`
    - `tortoise-orm`

更多帮助 [正在不断装修的文档](https://17theword.github.io/mc_qq)

## 命令

- 获取已连接至 WebSocket 的 MineCraft服务器
    - `服务器列表`


- 动态控制需要互通的群聊
    - `开启互通 Server1`
    - `开启互通 Server2`
    - `关闭互通 Server1`
    - `关闭互通 Server2`


- 获取当前群聊开启互通的服务器
    - `互通列表`

## 后续功能

- 不同群聊自定义是否发送群聊名称


- 不同服务器或不同群聊内的互通列表是否发送服务器名称


- 自定义选择通过 `WebSocket` 或 `MCRcon` 发送消息至MC
