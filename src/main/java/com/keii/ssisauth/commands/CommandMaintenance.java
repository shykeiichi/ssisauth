package com.keii.ssisauth.commands;

import com.google.common.hash.Hashing;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.Date;

import static com.keii.ssisauth.SSISAuth.apiip;

public class CommandMaintenance implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if(args.length < 2) {
            sender.sendMessage("Not enough arguments!");
        }
        if(args[0] == "set") {
            boolean setValue;
            if(args[1] != "true" && args[1] != "1" && args[1] != "false" && args[1] != "0") {
                sender.sendMessage("Invalid argument " + args[1]);
                return true;
            } else {
                if(args[1] == "true" || args[1] == "1") {
                    setValue = true;
                } else {
                    setValue = false;
                }
            }

            HttpRequest request;
            HttpResponse<String> response;
            String responseText;

            Date date = new Date();
            var current = date.getMinutes() + date.getDay() + date.getMonth();
            String sha256hex = Hashing.sha256()
                    .hashString(String.valueOf(current), StandardCharsets.UTF_8)
                    .toString();

            HttpClient client = HttpClient.newHttpClient();
            request = HttpRequest.newBuilder()
                    .uri(URI.create(apiip + "/api/v1/setmaintenance"))
                    .headers("Content-Type", "text/plain;charset=UTF-8")
                    .POST(HttpRequest.BodyPublishers.ofString(setValue ? "true," + sha256hex : "false," + sha256hex))
                    .build();

            try {
                response = client.send(request,
                        HttpResponse.BodyHandlers.ofString());
            } catch (IOException e) {
                throw new RuntimeException(e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

            responseText = response.body();
        }

        return true;
    }
}
