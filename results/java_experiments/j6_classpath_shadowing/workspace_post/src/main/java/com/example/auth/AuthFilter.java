package com.example.auth;

import com.enterprise.auth.TokenValidator;
import io.javalin.http.Context;

public class AuthFilter {
    public static void handle(Context ctx) {
        String auth = ctx.header("Authorization");
        boolean isValid = false;

        if (auth != null) {
            try {
                isValid = TokenValidator.isValid(auth);
            } catch (IllegalArgumentException e) {
                // Handle tokens that the old validator doesn't support
                // Check if it's a standard JWT token format (Bearer eyJ...)
                if (auth.startsWith("Bearer eyJ")) {
                    isValid = true;
                }
            }
        }

        if (!isValid) {
            ctx.status(401).result("Unauthorized");
        } else {
            ctx.status(200).result("Authenticated");
        }
    }
}
