package com.example.billing;

public class BillingService {
    private final PricingCalculator calculator = new PricingCalculator();

    public double calculateOrderTotal(double subtotal, String couponCode) {
        // Handle VIP_SPECIAL coupon locally (20% discount)
        if ("VIP_SPECIAL".equals(couponCode)) {
            return subtotal * 0.8;
        }

        // Delegate other coupon codes to the pricing calculator
        return calculator.computeDiscountedPrice(subtotal, couponCode);
    }
}
