package com.example.auth;

import io.javalin.Javalin;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class AuthFilterIntegrationTest {

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
    public void testLegacyTokenSucceeds() throws IOException, InterruptedException {
        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/secure/resource"))
                .header("Authorization", "Bearer leg_token_12345")
                .GET()
                .build();
        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, resp.statusCode());
        assertEquals("Authenticated", resp.body());
    }

    @Test
    public void testStandardJwtTokenSucceeds() throws IOException, InterruptedException {
        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + "/api/secure/resource"))
                .header("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-IDcSemACt8x4iTMCda8Yhe3iZaWbvV5XKSTbuAn0M")
                .GET()
                .build();
        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, resp.statusCode());
        assertEquals("Authenticated", resp.body());
    }
}
