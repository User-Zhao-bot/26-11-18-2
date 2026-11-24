package com.example.auth;

import io.javalin.Javalin;

public class App {
    public static Javalin create() {
        Javalin app = Javalin.create();
        app.get("/api/secure/resource", AuthFilter::handle);
        return app;
    }

    public static void main(String[] args) {
        create().start(8080);
    }
}
