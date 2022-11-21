package com.keii.ssisauth.commands;

import net.kyori.adventure.text.Component;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static com.keii.ssisauth.SSISAuth.apiip;

public class CommandWho implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if(args.length < 1) {
            sender.sendMessage("/who <namn>");
            return true;
        }

        HttpRequest request;
        HttpResponse<String> response;
        String responseText;
        try {
            HttpClient client = HttpClient.newHttpClient();
            request = HttpRequest.newBuilder()
                    .uri(URI.create(apiip + "/api/v1/whouser?username=" + args[0]))
                    .build();

            response = client.send(request,
                    HttpResponse.BodyHandlers.ofString());

            responseText = response.body();
        } catch(Exception error) {
            sender.sendMessage(Component.text().content("§cOj! Ser ut som att APIet har lite problem. Kontakta 22widi@stockholmscience.se").build());
            return true;
        }

        sender.sendMessage(args[0] + " is " + responseText);

        return true;
    }
}
