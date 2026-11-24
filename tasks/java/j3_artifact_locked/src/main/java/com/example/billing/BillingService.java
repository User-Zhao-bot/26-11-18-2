package com.example.billing;

public class BillingService {
    private final PricingCalculator calculator = new PricingCalculator();

    public double calculateOrderTotal(double subtotal, String couponCode) {
        return calculator.computeDiscountedPrice(subtotal, couponCode);
    }
}
