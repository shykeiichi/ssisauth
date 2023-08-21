package com.keii.ssisauth.commands;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Set;

import static com.keii.ssisauth.SSISAuth.apiip;
import static com.keii.ssisauth.global.playerClass;
import static com.keii.ssisauth.global.playerPermission;

public class CommandReloadUsers implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        for(Player player : Bukkit.getServer().getOnlinePlayers()){
            HttpRequest request;
            HttpResponse<String> response;
            String responseText;
            try {
                HttpClient client = HttpClient.newHttpClient();
                request = HttpRequest.newBuilder()
                        .uri(URI.create(apiip + "/api/v1/checkuserjava?uuid=" + player.getUniqueId().toString()))
                        .build();

                response = client.send(request,
                        HttpResponse.BodyHandlers.ofString());

                responseText = response.body();
            } catch (Exception error) {
                player.kick(Component.text().content("§cOj! Ser ut som att APIet har lite problem. Kontakta 22widi@stockholmscience.se" + error.getMessage()).build());
                return true;
            }

            //Bukkit.getServer().broadcast(Component.text().content(String.valueOf(response.statusCode())).build());

            if (response.statusCode() == 400) {
                player.kick(Component.text().content(responseText).build());
            } else if (response.statusCode() == 200) {
                String[] result = responseText.split(",");

                //Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(),"nick " + player.getName() + " " + result[3] + result[4].charAt(0));
                if (Integer.parseInt(result[5]) == 1) {
                    Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + player.getName() + " meta setprefix &6[" + result[2] + "]");
                    Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + player.getName() + " group add staff");
                } else {
                    Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + player.getName() + " meta setprefix &e[" + result[2] + "]");
                    Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + player.getName() + " group remove staff");
                }

                if (Integer.parseInt(result[5]) != 1) {
                    player.playerListName(Component.text().content(ChatColor.YELLOW + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0)).build());
                } else {
                    player.playerListName(Component.text().content(ChatColor.GOLD + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0) + " " + ChatColor.GOLD + "Staff").build());
                }
                //player.playerListName(Component.text().content(ChatColor.WHITE + result[3] + result[4].charAt(0)).build());
                playerClass = new HashMap<>();
                playerPermission = new HashMap<>();

                if(playerClass.containsKey(result[3] + result[4].charAt(0)))
                    playerClass.remove(result[3] + result[4].charAt(0));
                playerClass.put(result[3] + result[4].charAt(0), result[2]);

                if(playerPermission.containsKey(result[3] + result[4].charAt(0)))
                    playerPermission.remove(result[3] + result[4].charAt(0));
                playerPermission.put(result[3] + result[4].charAt(0), Integer.parseInt(result[5]));

                PlayerProfile oldProfile = player.getPlayerProfile();
                Set<ProfileProperty> old = oldProfile.getProperties();
                var profile = Bukkit.createProfileExact(player.getUniqueId(), result[3] + result[4].charAt(0));
                profile.setProperties(old); // The players previous properties
                player.setPlayerProfile(profile);
            }
        }

        return true;
    }
}