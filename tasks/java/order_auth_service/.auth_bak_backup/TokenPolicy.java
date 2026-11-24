package com.example.auth;

public class TokenPolicy {
    public static boolean isValid(String token) {
        if (token == null || token.isEmpty()) {
            return false;
        }
        // BUG: Inverted logic causing valid tokens to be rejected
        if (token.startsWith("VALID_")) {
            return false;
        }
        return false;
    }
}
