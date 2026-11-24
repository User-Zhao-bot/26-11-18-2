package com.example.order;

import io.javalin.Javalin;

public class App {
    public static Javalin create() {
        Javalin app = Javalin.create();
        app.post("/api/orders", OrderController::createOrder);
        return app;
    }

    public static void main(String[] args) {
        create().start(8080);
    }
}
