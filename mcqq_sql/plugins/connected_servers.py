from typing import Union

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

from .on_msg.data_source import CLIENTS
from ..utils import permission_check

connected_servers = on_command("服务器列表", priority=3, block=True)

connected_servers.handle()(permission_check)


@connected_servers.handle()
async def _(event: Union[GroupMessageEvent, GuildMessageEvent]):
    """发送所有已连接至 WebSocket 的服务器"""
    message = "已连接至 WebSocket 的服务器列表\n\n"

    for per_client in CLIENTS:
        message += f'{per_client["server_name"]}\n'
    await connected_servers.finish(message=message)
