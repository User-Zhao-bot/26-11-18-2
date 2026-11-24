package com.example.billing;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BillingServiceTest {
    @Test
    public void testStandardDiscount() {
        BillingService service = new BillingService();
        assertEquals(90.0, service.calculateOrderTotal(100.0, "SUMMER10"), 0.001, "Summer discount must be 10%");
    }

    @Test
    public void testVipSpecialDiscount() {
        BillingService service = new BillingService();
        assertEquals(80.0, service.calculateOrderTotal(100.0, "VIP_SPECIAL"), 0.001, "VIP_SPECIAL must apply 20% discount");
    }
}
