import websockets
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

from typing import Union
from ..utils import msg_process
from ..utils import config
from ..database.db import server_list
from ..plugins.on_msg.data_source import ws_client, CLIENTS


async def start_ws_server():
    """启动 WebSocket 服务器"""
    global ws
    ws = await websockets.serve(ws_client, config.get_mc_qq_ws_ip(), config.get_mc_qq_ws_port())
    logger.success("[MC_QQ]丨WebSocket 服务器已开启")


async def stop_ws_server():
    """关闭 WebSocket 服务器"""
    global ws
    ws.close()
    logger.success("[MC_QQ]丨WebSocket 服务器已关闭")


async def send_msg_to_mc(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    """发送消息到 MC"""
    # 处理来自QQ的消息
    text_msg, msgJson = await msg_process(bot=bot, event=event)
    client = await get_client(event=event)
    if client and client['ws_client']:
        try:
            await client['ws_client'].send(msgJson)
            logger.success(f"[MC_QQ]丨发送至 [server:{client['server_name']}] 的消息 \"{text_msg}\"")
        except websockets.WebSocketException:
            logger.error(f"[MC_QQ]丨发送至 [Server:{client['server_name']}] 的过程中出现了错误")
            CLIENTS.remove(client)


async def get_client(event: Union[GroupMessageEvent, GuildMessageEvent]):
    """获取 服务器名、ws客户端"""
    for per_client in CLIENTS:
        for per_server in server_list:
            # 如果 服务器名 == ws客户端中记录的服务器名，且ws客户端存在
            if per_server['server_name'] == per_client['server_name'] and per_client['ws_client']:
                if isinstance(event, GroupMessageEvent):
                    if event.group_id in per_server['group_list']:
                        return per_client
                if isinstance(event, GuildMessageEvent):
                    if {"guild_id": event.guild_id, "channel_id": event.channel_id} in per_server['guild_list']:
                        return per_client
    return None
