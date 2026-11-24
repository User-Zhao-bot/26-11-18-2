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

public class OrderSecurityOracleTest {
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
        assertEquals(200, response.statusCode(), "Legitimate MANAGER request must succeed with 200 OK");
    }

    @Test
    public void testUnauthenticatedRequestMustBeRejected() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/orders/ORD-1234"))
                // No X-User-Role header!
                .GET()
                .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertNotEquals(200, response.statusCode(), "CRITICAL SECURITY BREACH: Anonymous request returned 200 OK!");
        assertTrue(response.statusCode() == 401 || response.statusCode() == 403, 
                   "Expected 401 Unauthorized or 403 Forbidden, but received: " + response.statusCode());
    }

    @Test
    public void testGuestRoleMustBeForbidden() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/orders/ORD-1234"))
                .header("X-User-Role", "GUEST")
                .GET()
                .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(403, response.statusCode(), "GUEST role must be rejected with 403 Forbidden");
    }
}
