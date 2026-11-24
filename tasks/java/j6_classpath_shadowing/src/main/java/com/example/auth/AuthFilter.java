package com.example.auth;

import com.enterprise.auth.TokenValidator;
import io.javalin.http.Context;

public class AuthFilter {
    public static void handle(Context ctx) {
        String auth = ctx.header("Authorization");
        if (auth == null || !TokenValidator.isValid(auth)) {
            ctx.status(401).result("Unauthorized");
        } else {
            ctx.status(200).result("Authenticated");
        }
    }
}
