package com.keii.ssisauth.events;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.TextComponent;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Color;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

import java.awt.*;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Set;

import static com.keii.ssisauth.SSISAuth.apiip;
import static com.keii.ssisauth.global.playerClass;
import static com.keii.ssisauth.global.playerPermission;

public class PlayerJoin implements Listener {
    @EventHandler
    public static void onPlayerJoin(PlayerJoinEvent e) throws IOException, InterruptedException {
        HttpRequest request;
        HttpResponse<String> response;
        String responseText;
        try {
            HttpClient client = HttpClient.newHttpClient();
            request = HttpRequest.newBuilder()
                    .uri(URI.create(apiip + "/api/v1/checkuserjava?uuid=" + e.getPlayer().getUniqueId().toString()))
                    .build();

            response = client.send(request,
                    HttpResponse.BodyHandlers.ofString());

            responseText = response.body();
        } catch(Exception error) {
            e.getPlayer().kick(Component.text().content("§cOj! Ser ut som att APIet har lite problem. Kontakta 22widi@stockholmscience.se. " + error.getMessage()).build());
            return;
        }

        //Bukkit.getServer().broadcast(Component.text().content(String.valueOf(response.statusCode())).build());

        if(response.statusCode() == 400) {
            e.getPlayer().kick(Component.text().content(responseText).build());
        } else if(response.statusCode() == 200) {
            String[] result = responseText.split(",");

            //Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(),"nick " + e.getPlayer().getName() + " " + result[3] + result[4].charAt(0));
            if(Integer.parseInt(result[5]) == 1) {
                Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " meta setprefix &6[" + result[2] + "]");
                Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " group add staff");
            } else {
                Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " meta setprefix &e[" + result[2] + "]");
                Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " group remove staff");
            }

            if(Integer.parseInt(result[5]) != 1) {
                e.getPlayer().playerListName(Component.text().content(ChatColor.YELLOW + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0)).build());
            } else {
                e.getPlayer().playerListName(Component.text().content(ChatColor.GOLD + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0) + " " + ChatColor.GOLD + "Staff").build());
            }
            //e.getPlayer().playerListName(Component.text().content(ChatColor.WHITE + result[3] + result[4].charAt(0)).build());

            e.joinMessage(Component.text().content("§e" + result[2] + " " + result[3] + result[4].charAt(0) + " joined the game").build());
            e.getPlayer().sendMessage(Component.text("Glöm inte att du kan använda /map för att claima mark.").color(NamedTextColor.YELLOW));

            if(playerClass.containsKey(result[3] + result[4].charAt(0)))
                playerClass.remove(result[3] + result[4].charAt(0));
            playerClass.put(result[3] + result[4].charAt(0), result[2]);

            if(playerPermission.containsKey(result[3] + result[4].charAt(0)))
                playerPermission.remove(result[3] + result[4].charAt(0));
            playerPermission.put(result[3] + result[4].charAt(0), Integer.parseInt(result[5]));

            e.getPlayer().displayName(Component.text(result[3] + result[4].charAt(0)));
//            PlayerProfile oldProfile = e.getPlayer().getPlayerProfile();
//            Set<ProfileProperty> old = oldProfile.getProperties();
//            var profile = Bukkit.createProfileExact(e.getPlayer().getUniqueId(), result[3] + result[4].charAt(0));
//            profile.setProperties(old); // The players previous properties
//            e.getPlayer().setPlayerProfile(profile);
        }
    }
}
