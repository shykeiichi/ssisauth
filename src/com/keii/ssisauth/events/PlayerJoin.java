package com.keii.ssisauth.events;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static com.keii.ssisauth.SSISAuth.apiip;

public class PlayerJoin implements Listener {
    @EventHandler
    public static void onPlayerJoin(PlayerJoinEvent e) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(apiip + "/api/v1/checkuserjava?uuid=" + e.getPlayer().getUniqueId().toString()))
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        String responseText = response.body();

        if(response.statusCode() == 401) {
            e.getPlayer().kickPlayer("Registrera konto på https://mc.ssis.nu");
        } else if(response.statusCode() == 200) {
            String[] result = responseText.split(",");
            
            Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(),"nick " + e.getPlayer().getName() + " " + result[3] + result[4].charAt(0));
            Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "lp user " + e.getPlayer().getName() + " meta setprefix " + result[2]);
            e.getPlayer().setPlayerListName(ChatColor.YELLOW + result[2] + " " + ChatColor.WHITE + result[3] + result[4].charAt(0));
        }
    }
}
