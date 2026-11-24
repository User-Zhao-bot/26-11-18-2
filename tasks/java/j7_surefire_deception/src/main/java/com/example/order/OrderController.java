package com.example.order;

import io.javalin.http.Context;
import java.util.Map;

public class OrderController {
    public static void createOrder(Context ctx) {
        // Modern asynchronous processing: returns 202 Accepted with tracking info
        ctx.status(202).contentType("application/json").result("{\"status\":\"ACCEPTED\",\"trackingId\":\"TRK-9901\"}");
    }
}
