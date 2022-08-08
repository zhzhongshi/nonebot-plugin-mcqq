package com.scareye.mc_qq;


import org.bukkit.configuration.file.FileConfiguration;

class ConfigReader {

    /**
     * 获取配置文件信息
     */
    static FileConfiguration config = MC_QQ.instance.getConfig();

    /**
     * 获取是否启用插件
     * @return Enable
     */
    static boolean getEnable() {
        return config.getBoolean("enable_mc_qq", true);
    }    // 获取地址

    /**
     * 获取地址
     * @return Address
     */
    static String getAddress() {
        return config.getString("websocket_server.address", "127.0.0.1");
    }

    /**
     * 获取端口
     * @return Port
     */
    static int getPort() {
        return config.getInt("websocket_server.port", Integer.parseInt("8765"));
    }

    /**
     * 获取聊天修饰
     * @return SayWay
     */
    static String getSayWay() {
        return config.getString("say_way", " ：");
    }

    /**
     * 获取是否启用 加入/退出 推送
     * @return JoinQuit
     */
    static boolean getJoinQuit() {
        return config.getBoolean("join_quit", true);
    }

}
