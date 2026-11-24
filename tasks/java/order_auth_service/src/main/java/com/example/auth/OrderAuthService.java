package com.example.auth;

public class OrderAuthService {
    public boolean authorizeOrder(String token, String orderId) {
        if (!TokenPolicy.isValid(token)) {
            return false;
        }
        return orderId != null && !orderId.trim().isEmpty();
    }
}
