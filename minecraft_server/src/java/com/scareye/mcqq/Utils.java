package com.scareye.mcqq;
/*
正则
    原版服务器 聊天 判定："\[Server thread/INFO]:(.*)<(.*)> (.*)"
    原版服务端 加入/离开 判定："\[Server thread/INFO] :(.*) (.*) the game"

    Forge端 聊天 判定："\[Server thread/INFO] \[net.Minecraft.server.MinecraftServer/]:(.*)<(.*)> (.*)"
    Forge端 加入/离开 判定："\[Server thread/INFO] \[net.Minecraft.server.MinecraftServer/]: (.*) (.*) the game"

    Forge 1.18.2 聊天 判定："\[Server thread/INFO] \[net.Minecraft.server.dedicated.DedicatedServer/]:(.*)<(.*)> (.*)"
    Forge 1.18.2 加入/离开 判定："\[Server thread/INFO] \[net.Minecraft.server.dedicated.DedicatedServer/]: (.*) (.*) the game"

    Fabric端 与原版日志相同

 */

import com.alibaba.fastjson.JSONObject;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.scareye.mcqq.ConfigReader.config;

public class Utils {

    /**
     * 原版端 聊天 正则
     */
    static String minecraftChatRegex = "\\[Server thread/INFO]:(.*)<(.*)> (.*)";

    /**
     * 原版端 加入/离开 服务器 正则
     */
    static String minecraftJoinQuitRegex = "\\[Server thread/INFO]: (.*) (.*) the game";

    /**
     * Forge端 聊天 正则
     */
    static String forgeChatRegex = "\\[Server thread/INFO] \\[net.minecraft.server.MinecraftServer/]:(.*)<(.*)> (.*)";
    static String forgeChatRegex_1182 = "\\[Server thread/INFO] \\[net.minecraft.server.dedicated.DedicatedServer/]:(.*)<(.*)> (.*)";

    /**
     * Forge端 加入/离开 服务器 正则
     */
    static String forgeJoinQuitRegex = "\\[Server thread/INFO] \\[net.minecraft.server.MinecraftServer/]: (.*) (.*) the game";
    static String forgeJoinQuitRegex_1182 = "\\[Server thread/INFO] \\[net.minecraft.server.dedicated.DedicatedServer/]: (.*) (.*) the game";

    /**
     * 向服务器后台发送信息
     *
     * @param msg String 信息
     */
    static void say(String msg) {
        System.out.println(("[MC_QQ]丨" + msg));
    }

    /**
     * 将 日志消息 处理为 Json
     *
     * @param msg String 日志消息
     * @return String Json
     */
    static String processMessageToJson(String msg) {

        JSONObject jsonMessage = new JSONObject();
        JSONObject playerJson = new JSONObject();
        String text_msg = "";

        // 放入服务器名
        jsonMessage.put("server_name", config().get("server_name"));

        Matcher serverLog = null;

        // 判定前缀
        if (getIfForgeChat_1182(msg) || getIfMinecraftChat(msg) || getIfForgeChat(msg)) {
            /*
            聊天
             */
            String playerName;
            String playerMsg;
            if (getIfMinecraftChat(msg)) {
                // 原版聊天
                serverLog = getServerLogMatcher(msg, minecraftChatRegex);
            } else if (getIfForgeChat(msg)) {
                serverLog = getServerLogMatcher(msg, forgeChatRegex);
            } else if (getIfForgeChat_1182(msg)) {
                serverLog = getServerLogMatcher(msg, forgeChatRegex_1182);
            }
            playerName = serverLog.group(2);
            playerMsg = serverLog.group(3);


            // 放入事件名
            jsonMessage.put("post_type", "message");
            jsonMessage.put("event_name", "MinecraftPlayerChatEvent");
            // 放入玩家
            playerJson.put("nickname", playerName);
            jsonMessage.put("player", playerJson);
            jsonMessage.put("sub_type", "chat");

            // message的Json
            jsonMessage.put("message", playerMsg);

            text_msg += playerName + config().get("say_way") + playerMsg;

        } else if ((Boolean) config().get("join_quit") && (getIfForgeJoinQuit_1182(msg) || getIfMinecraftJoinQuit(msg) || getIfForgeJoinQuit(msg))) {
            /*
            加入/离开服务器
             */
            String playerName;
            String join_quit_msg;
            String data = "";
            if (getIfMinecraftJoinQuit(msg)) {
                /*
                原版
                 */
                serverLog = getServerLogMatcher(msg, minecraftJoinQuitRegex);

            } else if (getIfForgeJoinQuit(msg)) {
                /*
                Forge
                 */
                serverLog = getServerLogMatcher(msg, minecraftJoinQuitRegex);

            } else if (getIfForgeJoinQuit_1182(msg)) {
                /*
                Forge 1.18.2
                 */
                serverLog = getServerLogMatcher(msg, forgeJoinQuitRegex_1182);

            }
            playerName = serverLog.group(1);
            join_quit_msg = serverLog.group(2);
            if (join_quit_msg.equals("joined")) {
                jsonMessage.put("event_name", "MinecraftPlayerJoinEvent");
                jsonMessage.put("sub_type", "join");
                data = playerName + " 加入了服务器";
            } else if (join_quit_msg.equals("left")) {
                jsonMessage.put("event_name", "MinecraftPlayerQuitEvent");
                jsonMessage.put("sub_type", "quit");
                data = playerName + " 离开了服务器";
            }

            jsonMessage.put("post_type", "notice");
            // 放入玩家
            playerJson.put("nickname", playerName);
            jsonMessage.put("player", playerJson);
            // 写入message
            jsonMessage.put("message", data);

            text_msg += data;
        }
        say(text_msg);
        return jsonMessage.toJSONString();
    }

    private static boolean getIfForgeJoinQuit_1182(String msg) {
        Pattern pattern = Pattern.compile(forgeJoinQuitRegex_1182);
        Matcher matcher = pattern.matcher(msg);
        return matcher.find();
    }

    private static boolean getIfForgeChat_1182(String msg) {
        Pattern pattern = Pattern.compile(forgeChatRegex_1182);
        Matcher matcher = pattern.matcher(msg);
        return matcher.find();
    }

    /**
     * 获取 是否为 原版端 聊天 消息
     *
     * @param message String 消息
     * @return boolean
     */
    static boolean getIfMinecraftChat(String message) {
        Pattern pattern = Pattern.compile(minecraftChatRegex);
        Matcher matcher = pattern.matcher(message);
        return matcher.find();
    }

    /**
     * 获取 是否为 原版端 加入/离开 消息
     *
     * @param message String 消息
     * @return boolean
     */
    static boolean getIfMinecraftJoinQuit(String message) {
        Pattern pattern = Pattern.compile(minecraftJoinQuitRegex);
        Matcher matcher = pattern.matcher(message);
        return matcher.find();
    }

    /**
     * 获取 是否为 Forge端 聊天 消息
     *
     * @param message String 消息
     * @return boolean
     */
    static boolean getIfForgeChat(String message) {
        Pattern pattern = Pattern.compile(forgeChatRegex);
        Matcher matcher = pattern.matcher(message);
        return matcher.find();
    }

    /**
     * 获取 是否为 Forge端 加入/离开 消息
     *
     * @param message String 消息
     * @return boolean
     */
    static boolean getIfForgeJoinQuit(String message) {
        Pattern pattern = Pattern.compile(forgeJoinQuitRegex);
        Matcher matcher = pattern.matcher(message);
        return matcher.find();
    }

    /**
     * 获取 是否为需要的信息
     *
     * @param message 信息
     * @return boolean
     */
    static boolean getIfNeedMsg(String message) {
        return getIfForgeChat_1182(message) || getIfForgeJoinQuit_1182(message) || getIfMinecraftChat(message) || getIfMinecraftJoinQuit(message) || getIfForgeChat(message) || getIfForgeJoinQuit(message);
    }

    /**
     * 通过正则获取服务器日志
     *
     * @param allText 完整信息
     * @param text    匹配信息 正则
     * @return Matcher
     */
    public static Matcher getServerLogMatcher(String allText, String text) {
        Pattern pattern = Pattern.compile(text);
        Matcher matcher = pattern.matcher(allText);
        if (matcher.find()) {
            return matcher;
        }
        return null;
    }

    /**
     * 字符串转为 unicode 编码
     *
     * @param string 字符串
     * @return unicode编码
     */
    static String unicodeEncode(String string) {
        char[] utfBytes = string.toCharArray();
        StringBuilder unicodeBytes = new StringBuilder();
        for (char utfByte : utfBytes) {
            String hexB = Integer.toHexString(utfByte);
            if (hexB.length() <= 2) {
                hexB = "00" + hexB;
            }
            unicodeBytes.append("\\u").append(hexB);
        }
        return unicodeBytes.toString();
    }
}
