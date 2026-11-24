package com.example.order.legacy_fixed;

import com.example.order.App;
import io.javalin.Javalin;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class OrderLegacyIntegrationTest {

    private static Javalin app;
    private static int port;
    private static HttpClient client;

    @BeforeAll
    public static void setup() {
        app = App.create().start(0);
        port = app.port();
        client = HttpClient.newHttpClient();
    }

    @AfterAll
    public static void teardown() {
        if (app != null) app.stop();
    }

    @Test
    public void testSynchronousOrderCreationLegacyAssertion() throws Exception {
        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/orders"))
                .POST(HttpRequest.BodyPublishers.ofString("{}"))
                .build();
        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        // Updated to match async migration: Expects 202 Accepted with async processing
        assertEquals(202, resp.statusCode(), "Order placement returns 202 Accepted with async processing");
    }
}
