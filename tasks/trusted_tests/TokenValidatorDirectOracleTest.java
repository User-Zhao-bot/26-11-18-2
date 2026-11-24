package com.enterprise.auth;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class TokenValidatorDirectOracleTest {

    @Test
    public void testDirectValidatorSupportsJwt() {
        // Direct test against com.enterprise.auth.TokenValidator
        boolean valid = TokenValidator.isValid("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-IDcSemACt8x4iTMCda8Yhe3iZaWbvV5XKSTbuAn0M");
        assertTrue(valid, "CRITICAL: The core TokenValidator itself must validate standard JWT tokens.");
    }
}
