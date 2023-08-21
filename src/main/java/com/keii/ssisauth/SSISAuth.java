package com.keii.ssisauth;

import com.keii.ssisauth.commands.CommandHelpop;
import com.keii.ssisauth.commands.CommandReloadUsers;
import com.keii.ssisauth.commands.CommandTeleportPlayer;
import com.keii.ssisauth.commands.CommandWho;
import com.keii.ssisauth.events.PlayerJoin;
import org.bukkit.ChatColor;
import org.bukkit.plugin.java.JavaPlugin;

public class SSISAuth extends JavaPlugin {
    public static String apiip = "https://mc.ssis.nu";

    @Override
    public void onEnable() {
        this.getCommand("who").setExecutor(new CommandWho());
        this.getCommand("teleportplayer").setExecutor(new CommandTeleportPlayer());
        this.getCommand("reloadusers").setExecutor(new CommandReloadUsers());
        this.getCommand("helpop").setExecutor(new CommandHelpop());
        getServer().getPluginManager().registerEvents(new PlayerJoin(), this);
        getServer().getConsoleSender().sendMessage(ChatColor.GREEN + "SSISAuth Enabled!");
        getServer().dispatchCommand(getServer().getConsoleSender(), "reloadusers");
    }

    @Override
    public void onDisable() {
        getServer().getConsoleSender().sendMessage(ChatColor.RED + "SSISAuth Disabled");
    }
}
