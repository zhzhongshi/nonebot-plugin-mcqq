import json

import websockets
from nonebot import get_bot, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

from typing import Union
from ...utils import msg_process, send_msg_to_qq, get_type_id
from ...database.db import server_list

CLIENTS = []
"""客户端列表"""


async def ws_client(websocket):
    """WebSocket"""
    msg = {}
    try:
        async for message in websocket:
            msg = json.loads(message)
            if msg['event_name'] == "ConnectEvent":
                CLIENTS.append({"server_name": msg['server_name'], "ws_client": websocket})
                logger.success(f"[MC_QQ]丨[Server:{msg['server_name']}] 已连接至 WebSocket 服务器")
            # 发送消息到QQ
            else:
                await send_msg_to_qq(bot=get_bot(), json_msg=msg)
    except websockets.WebSocketException:
        # 移除当前客户端
        CLIENTS.remove({"server_name": msg['server_name'], "ws_client": websocket})
    if websocket.closed:
        logger.error(f"[MC_QQ]丨[Server:{msg['server_name']}] 的 WebSocket 连接已断开")


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
            if per_client['ws_client'] and per_server['server_name'] == per_client['server_name']:
                if isinstance(event, GroupMessageEvent):
                    if event.group_id in per_server['group_list']:
                        return per_client
                if isinstance(event, GuildMessageEvent):
                    if await get_type_id(event) in per_server['guild_list']:
                        return per_client
    return None
