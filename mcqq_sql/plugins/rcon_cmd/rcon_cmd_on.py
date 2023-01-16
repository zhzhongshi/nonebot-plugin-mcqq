from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.params import ArgPlainText

from ..rcon import change_rcon_status
from ...database import DB as db
from ...utils import permission_check, handle_server_name, server_name_check, to_me

rcon_cmd_on = on_command("开启rcon命令", rule=to_me(), priority=3)
rcon_cmd_on.__doc__ = """开启rcon命令 Server（管理员）"""

rcon_cmd_on.handle()(permission_check)

rcon_cmd_on.handle()(handle_server_name)

rcon_cmd_on.got("server_name", prompt="请输入要开启 Rcon_CMD 的服务器")(server_name_check)


@rcon_cmd_on.handle()
async def _(event: MessageEvent, server_name: str = ArgPlainText("server_name")):
    """根据 服务器名 开启 Rcon_CMD"""
    if await db.update_server(
            "rcon_cmd",
            True,
            server_name=server_name,
    ):
        await change_rcon_status(server_name=server_name)
        server = await db.get_server(server_name=server_name)
        assert server is not None
        await rcon_cmd_on.finish(f"已开启 [{server.server_name}] 的Rcon_CMD")
    await rcon_cmd_on.finish(f"服务器（{server_name}）未互通，请先互通后再操作")
