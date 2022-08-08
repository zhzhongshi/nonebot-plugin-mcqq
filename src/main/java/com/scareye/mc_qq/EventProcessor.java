package com.scareye.mc_qq;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

import static com.scareye.mc_qq.MC_QQ.websocket;

class EventProcessor implements Listener {
    /**
     * 监听玩家聊天
     */
    @EventHandler
    void onPlayerChat(AsyncPlayerChatEvent event) {
        websocket.sendMessage(event.getPlayer().getName() + ConfigReader.getSayWay() + event.getMessage());
    }

    /**
     * 监听玩家加入事件
     */
    @EventHandler
    void onPlayerJoin(PlayerJoinEvent event) {
        if (ConfigReader.getJoinQuit()) {
            websocket.sendMessage(event.getPlayer().getName() + " 加入了服务器");
        }
    }

    /**
     * 监听玩家离开事件
     */
    @EventHandler
    void onPlayerQuit(PlayerQuitEvent event) {
        if (ConfigReader.getJoinQuit()) {
            websocket.sendMessage(event.getPlayer().getName() + " 离开了服务器");
        }
    }
}
