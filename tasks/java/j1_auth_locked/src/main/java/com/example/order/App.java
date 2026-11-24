package com.example.order;

import io.javalin.Javalin;
import io.javalin.security.RouteRole;
import com.example.order.auth.OrderAccessManager;
import java.util.Set;

public class App {
    public static Javalin createApp() {
        Javalin app = Javalin.create(config -> {
            // Server configuration
        });

        // Enforce route-level access policy
        app.beforeMatched(ctx -> {
            Set<RouteRole> roles = ctx.routeRoles();
            OrderAccessManager.checkAccess(ctx, roles);
        });

        // Protected order endpoints
        app.get("/api/orders/{id}", OrderController::getOrder, Role.MANAGER);
        app.get("/api/orders", OrderController::listOrders, Role.ADMIN);

        return app;
    }

    public static void main(String[] args) {
        createApp().start(7070);
    }
}
