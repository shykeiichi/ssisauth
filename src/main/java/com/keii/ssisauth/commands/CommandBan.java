package com.keii.ssisauth.commands;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Arrays;

import static com.keii.ssisauth.SSISAuth.apiip;
import static com.keii.ssisauth.global.getClassOfPlayer;
import static com.keii.ssisauth.global.getPermissionOfPlayer;

public class CommandBan implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {

        if(args.length < 1) {
            sender.sendMessage("/ban <player> <anledning>");
            return true;
        }

        sender.sendMessage("Bans är inte implementerade för tillfället");

        return true;

//        HttpRequest request;
//        HttpResponse<String> response;
//        String responseText;
//        HttpClient client = HttpClient.newHttpClient();
//        request = HttpRequest.newBuilder()
//                .uri(URI.create(apiip + "/api/v1/helpop/add?username=" + sender.getName() + "&message=" + String.join("+", args) + "&class=" + getClassOfPlayer(player)))
//                .build();
//
//        try {
//            response = client.send(request,
//                    HttpResponse.BodyHandlers.ofString());
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        } catch (InterruptedException e) {
//            throw new RuntimeException(e);
//        }
//
//        responseText = response.body();
//        if(response.statusCode() != 200) {
//            player.sendMessage(ChatColor.RED + String.valueOf(response.statusCode()) + " Error: " + responseText);
//        } else {
//            player.sendMessage(ChatColor.YELLOW + "Skickat meddelande till Staff");
//            for(Player _player : Bukkit.getServer().getOnlinePlayers()) {
//                if(getPermissionOfPlayer(_player) == 1) {
//                    player.sendMessage(ChatColor.YELLOW + "[StaffHjälp] " + ChatColor.WHITE + "<" + player.getName() + "> " + String.join(" ", args));
//                }
//            }
//        }
//        return true;
    }
}
