package com.keii.ssisauth;

import org.bukkit.Bukkit;
import org.bukkit.entity.Player;

import java.util.HashMap;
import java.util.Map;

public class global {
    public static HashMap<String, String> playerClass = new HashMap<>();
    public static HashMap<String, Integer> playerPermission = new HashMap<>();

    public static String getClassOfPlayer(Player player) {
        return playerClass.get(player.getName());
    }

    public static String getClassOfPlayer(String playerName) { // WillemD
        return playerClass.get(playerName);
    }

    public static Integer getPermissionOfPlayer(Player player) {
        return playerPermission.getOrDefault(player.getName(), 0);
    }
    public static Integer getPermissionOfPlayer(String playerName) { // WillemD
        return playerPermission.getOrDefault(playerName, 0);
    }
}
