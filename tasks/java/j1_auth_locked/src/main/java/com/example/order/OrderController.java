package com.example.order;

import io.javalin.http.Context;

public class OrderController {
    public static void getOrder(Context ctx) {
        String orderId = ctx.pathParam("id");
        ctx.status(200).json("{\"orderId\":\"" + orderId + "\",\"status\":\"CONFIRMED\",\"total\":299.0}");
    }

    public static void listOrders(Context ctx) {
        ctx.status(200).json("[{\"orderId\":\"101\"},{\"orderId\":\"102\"}]");
    }
}
