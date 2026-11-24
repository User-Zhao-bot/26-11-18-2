package com.example.auth;

public class TokenPolicy {
    public static boolean isValid(String token) {
        if (token == null || token.isEmpty()) {
            return false;
        }
        if (token.startsWith("VALID_")) {
            return true;
        }
        return false;
    }
}
