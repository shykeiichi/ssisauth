package com.keii.ssisauth.commands;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class CommandTeleportPlayer implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if(!(sender instanceof Player)) {
            sender.sendMessage("§cYou must run this command as player!");
            return true;
        }

        if(args.length < 1) {
            sender.sendMessage("/teleportplayer <spelare>");
            return true;
        }

        if(args.length == 1) {
            Player player = (Player) sender;

            Player target = Bukkit.getServer().getPlayer(args[0]);
            if (target == null) {
                sender.sendMessage("§cOgiltig spelare");
                return true;
            }

            player.teleport(target.getLocation());
            sender.sendMessage("§eTeleportera dig till " + target.getName());
        } else {
            Player victim = Bukkit.getServer().getPlayer(args[0]);
            Player target = Bukkit.getServer().getPlayer(args[1]);
            if (victim == null) {
                sender.sendMessage("§cOgiltigt victim " + args[0]);
                return true;
            }
            if (target == null) {
                sender.sendMessage("§cOgiltig target " + args[1]);
                return true;
            }

            victim.teleport(target.getLocation());
            sender.sendMessage("§eTeleportera " + victim.getName() + " till " + target.getName());
        }

        return true;
    }
}
