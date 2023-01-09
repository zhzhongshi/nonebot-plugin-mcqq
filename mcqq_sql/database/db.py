from typing import Optional, List

from nonebot import get_driver
from tortoise import Tortoise, connections
from .models import Sub, Server, Group, Guild

server_list = []


class DB:
    """数据库交互类，与增删改查无关的部分不应该在这里面实现"""

    @classmethod
    async def init(cls):
        """初始化数据库"""
        from . import models  # noqa: F401

        await Tortoise.init(
            db_url=f"sqlite://src/mcqq.sqlite3",
            modules={"models": [locals()["models"]]},
        )
        await Tortoise.generate_schemas()
        await cls.update_server_list()

    @classmethod
    async def get_server(cls, **kwargs):
        """获取 Server 信息"""
        return await Server.get(**kwargs).first()

    # 服务器 相关操作
    @classmethod
    async def add_server(cls, **kwargs):
        """添加 Server 信息"""
        return await Server.add(**kwargs)

    @classmethod
    async def delete_server(cls, server_name) -> bool:
        """删除 Server 信息"""
        if await cls.get_server(server_name=server_name):
            # 还存在该 UP 主订阅，不能删除
            return False
        await Server.delete(server_name=server_name)
        return True

    @classmethod
    async def update_server(cls, server_name: str) -> bool:
        """更新 Server 信息"""
        if await cls.get_server(server_name=server_name):
            await Server.update(server_name=server_name)
            return True
        return False

    # 群 相关操作
    @classmethod
    async def get_group(cls, **kwargs):
        """获取群设置"""
        return await Group.get(**kwargs).first()

    @classmethod
    async def add_group(cls, **kwargs):
        """创建群设置"""
        return await Group.add(**kwargs)

    @classmethod
    async def delete_group(cls, type_id) -> bool:
        """删除群设置"""
        if await cls.get_sub(type="group", type_id=type_id):
            # 当前群还有订阅，不能删除
            return False
        await Group.delete(group_id=type_id)
        return True

    # 频道 相关操作
    @classmethod
    async def get_guild(cls, **kwargs):
        """获取频道设置"""
        return await Guild.get(**kwargs).first()

    @classmethod
    async def add_guild(cls, **kwargs):
        """创建频道设置"""
        return await Guild.add(**kwargs)

    @classmethod
    async def delete_guild(cls, type_id) -> bool:
        """删除子频道设置"""
        if await cls.get_sub(type="guild", type_id=type_id):
            # 当前频道还有订阅，不能删除
            return False
        await Guild.delete(id=type_id)
        return True

    @classmethod
    async def get_guild_type_id(cls, guild_id, channel_id) -> Optional[int]:
        """获取频道订阅 ID"""
        guild = await Guild.get(guild_id=guild_id, channel_id=channel_id).first()
        return guild.id if guild else None

    # 列表 相关操作
    @classmethod
    async def get_sub(cls, **kwargs):
        """获取指定位置的 互通列表"""
        return await Sub.get(**kwargs).first()

    @classmethod
    async def add_sub(cls, *, server_name, **kwargs) -> bool:
        """添加互通服务器"""
        if not await Sub.add(type=kwargs["type"], type_id=kwargs["type_id"], server_name=server_name):
            return False
        if kwargs["type"] == "group":
            await cls.add_group(group_id=kwargs["type_id"])
        await cls.add_server(server_name=server_name)
        await cls.update_server_list()
        return True

    @classmethod
    async def set_sub(cls, **kwargs):
        """开关互通设置"""
        return await Sub.update(**kwargs)

    @classmethod
    async def delete_sub(cls, server_name, type, type_id) -> bool:
        """删除指定互通记录"""
        if await Sub.delete(server_name=server_name, type=type, type_id=type_id):
            await cls.delete_server(server_name=server_name)
            await cls.update_server_list()
            return True
        # 订阅不存在
        return False

    @classmethod
    async def get_subs(cls, **kwargs):
        return await Sub.get(**kwargs)

    @classmethod
    async def get_sub_list(cls, type, type_id) -> List[Sub]:
        """获取指定位置的互通列表"""
        return await cls.get_subs(type=type, type_id=type_id)

    @classmethod
    async def delete_sub_list(cls, type, type_id):
        """删除指定位置的互通列表"""
        async for sub in Sub.get(type=type, type_id=type_id):
            await cls.delete_sub(server_name=sub.server_name, type=sub.type, type_id=sub.type_id)
        await cls.update_server_list()

    @classmethod
    async def update_server_list(cls):
        """更新需要推送的 服务器 主列表"""
        subs = Sub.all()
        servers = Server.all()
        server_list.clear()
        async for server in servers:
            server_list.append(
                {
                    "server_name": server.server_name,
                    "group_list": [],
                    "guild_list": []
                }
            )

        for per_server in server_list:
            async for sub in subs:
                if per_server["server_name"] == sub.server_name:
                    if sub.type == "group":
                        per_server["group_list"].append(sub.type_id)
                    elif sub.type == "guild":
                        per_server["guild_list"].append(sub.type_id)


get_driver().on_startup(DB.init)
get_driver().on_shutdown(connections.close_all)
