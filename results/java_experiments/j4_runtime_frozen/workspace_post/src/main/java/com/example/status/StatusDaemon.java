package com.example.status;

import io.javalin.Javalin;

public class StatusDaemon {
    public static void main(String[] args) {
        Javalin app = Javalin.create().start(8080);
        app.get("/api/health", ctx -> {
            ctx.json("{\"status\":\"UP\"}");
        });
        System.out.println("StatusDaemon successfully started on port 8080");
    }
}
