package com.keii.ssisauth.events;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.TextComponent;
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
            e.getPlayer().kick(Component.text().content("§cOj! Ser ut som att APIet har lite problem. Kontakta 22widi@stockholmscience.se").build());
            return;
        }

        Bukkit.getServer().broadcast(Component.text().content(String.valueOf(response.statusCode())).build());

        if(response.statusCode() == 401) {
            e.getPlayer().kick(Component.text().content("Registrera konto på https://mc.ssis.nu").build());
        } else if(response.statusCode() == 200) {
            String[] result = responseText.split(",");

            //Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(),"nick " + e.getPlayer().getName() + " " + result[3] + result[4].charAt(0));
            Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " meta setprefix " + result[2]);
            //e.getPlayer().setPlayerListName(ChatColor.YELLOW + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0));
            //e.getPlayer().playerListName(Component.text().content(ChatColor.WHITE + result[3] + result[4].charAt(0)).build());

            e.joinMessage(Component.text().content("§e" + result[3] + result[4].charAt(0) + " joined the game").build());

            PlayerProfile oldProfile = e.getPlayer().getPlayerProfile();
            Set<ProfileProperty> old = oldProfile.getProperties();
            var profile = Bukkit.createProfileExact(e.getPlayer().getUniqueId(), result[3] + result[4].charAt(0));
            profile.setProperties(old); // The players previous properties
            e.getPlayer().setPlayerProfile(profile);
        }
    }
}
