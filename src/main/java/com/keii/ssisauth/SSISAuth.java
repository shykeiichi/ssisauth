package com.keii.ssisauth;

import com.keii.ssisauth.commands.CommandMaintenance;
import com.keii.ssisauth.events.PlayerJoin;
import org.bukkit.ChatColor;
import org.bukkit.plugin.java.JavaPlugin;

public class SSISAuth extends JavaPlugin {
    //public static String apiip = "https://mc.ssis.nu";
    public static String apiip = "http://192.168.147.230:8080";

    @Override
    public void onEnable() {

        this.getCommand("maintenance").setExecutor(new CommandMaintenance());
        getServer().getPluginManager().registerEvents(new PlayerJoin(), this);
        getServer().getConsoleSender().sendMessage(ChatColor.GREEN + "SSISAuth Enabled");
    }

    @Override
    public void onDisable() {
        getServer().getConsoleSender().sendMessage(ChatColor.RED + "SSISAuth Disabled");
    }
}
