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
    - `aio-mc-rcon`

更多帮助 [正在不断装修的文档](https://17theword.github.io/mc_qq)

## 命令

- 帮助
    - 为防止与其他插件冲突
    - 请使用 `mcqq帮助` 来获取帮助


- 获取已连接至 WebSocket 的 MineCraft服务器
    - `服务器列表`


- 动态控制需要互通的群聊
    - `开启互通 Server1`
    - `开启互通 Server2`
    - `关闭互通 Server1`
    - `关闭互通 Server2`


- 获取当前群聊开启互通的服务器
    - `互通列表`


- 为当前群聊设置是否在发送消息到MC时携带群聊名称
    - `开启发送群名`
    - `关闭发送群名`


- 服务器在发送消息至群聊时，是否携带服务器名
    - `开启服务器名`
    - `关闭服务器名`


- 服务器是否启用Rcon来发送消息或命令
    - Rcon发送 消息和命令 适用于非插件端服务器
    - Rcon发送命令适用于纯插件端
    - `开启rcon消息 服务器名` 丨 `关闭rcon消息 服务器名`
    - `开启rcon命令 服务器名` 丨 `关闭rcon命令 服务器名`


- 修改服务器Rcon连接信息的IP、端口、密码
    - 为保障安全，仅限 `超级用户` 与 `Bot` 私聊使用
    - 为保障安全，若rcon密码为默认密码，将不会连接服务器的Rcon
    - `修改rconip 服务器名 新ip`
    - `修改rcon端口 服务器 新端口`
    - `修改rcon密码 服务器 新密码`


- 查看数据库中服务器列表
    - `服务器列表`


- 查看已经连接至 WebSocket 的服务器列表
    - `已连接服务器列表`

## 特别感谢

- [@SK-415](https://github.com/SK-415) ：感谢SK佬给予许多优秀的建议和耐心的解答。
- [@zhz-红石头](https://github.com/zhzhongshi) ：感谢红石头在代码上的帮助
- [SK-415/HarukaBot](https://github.com/SK-415/HarukaBot) ：感谢HarukaBot如此优雅的各类方法
- [NoneBot2](https://github.com/nonebot/nonebot2)： 插件使用的开发框架。
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)： 稳定完善的 CQHTTP 实现。

## 贡献与支持

觉得好用可以给这个项目点个 `Star` 或者去 [爱发电](https://afdian.net/a/17TheWord) 投喂我。

有意见或者建议也欢迎提交 [Issues](https://github.com/17TheWord/nonebot-plugin-mcqq/issues)
和 [Pull requests](https://github.com/17TheWord/nonebot-plugin-mcqq/pulls)。

## 许可证

本项目使用 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 作为开源许可证。
