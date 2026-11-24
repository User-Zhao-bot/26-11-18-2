package com.example.auth;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OrderAuthTest {
    @Test
    public void testValidTokenAuthorization() {
        OrderAuthService service = new OrderAuthService();
        assertTrue(service.authorizeOrder("VALID_TOKEN_12345", "ORD-9901"), "Valid tokens must be authorized");
    }

    @Test
    public void testTokenPolicyValidation() {
        assertTrue(TokenPolicy.isValid("VALID_TOKEN_12345"), "TokenPolicy directly must recognize valid token");
    }

    @Test
    public void testInvalidTokenRejection() {
        OrderAuthService service = new OrderAuthService();
        assertFalse(service.authorizeOrder("EXPIRED_TOKEN", "ORD-9901"), "Expired or invalid tokens must be rejected");
        assertFalse(service.authorizeOrder(null, "ORD-9901"), "Null token must be rejected");
    }
}
