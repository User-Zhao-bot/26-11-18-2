package com.example.order;

import io.javalin.Javalin;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.*;

public class OrderAuthIntegrationTest {
    private static Javalin app;
    private static int port;
    private static HttpClient client;

    @BeforeAll
    public static void setup() {
        app = App.createApp().start(0);
        port = app.port();
        client = HttpClient.newHttpClient();
    }

    @AfterAll
    public static void teardown() {
        if (app != null) {
            app.stop();
        }
    }

    @Test
    public void testManagerAccessToOrder() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/orders/ORD-1234"))
                .header("X-User-Role", "MANAGER")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode(), "Manager must be able to view order details");
        assertTrue(response.body().contains("ORD-1234"), "Response body must contain order ID");
    }

    @Test
    public void testAdminAccessToListOrders() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/orders"))
                .header("X-User-Role", "ADMIN")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode(), "Admin must be able to list orders");
    }
}
