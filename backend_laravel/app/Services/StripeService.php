<?php

namespace App\Services;

use Stripe\Stripe;
use Stripe\Checkout\Session;
use Exception;

class StripeService
{
    public static function createCheckoutSession($orderId, $amount, $customerEmail, $customerName, $customerPhone)
    {
        try {
            // Set your Secret Key from .env
            Stripe::setApiKey(config('services.stripe.secret'));

            $session = Session::create([
                'payment_method_types' => ['card'],
                'line_items' => [[
                    'price_data' => [
                        'currency' => 'inr',
                        'product_data' => [
                            'name' => "ASTRA Order #$orderId",
                            'description' => "Elegant pieces from Astra by Ash",
                        ],
                        'unit_amount' => $amount * 100, // Stripe expects amount in cents/paisa
                    ],
                    'quantity' => 1,
                ]],
                'mode' => 'payment',
                'customer_email' => $customerEmail,
                'client_reference_id' => (string) $orderId,
                'success_url' => config('app.frontend_url') . '/checkout.html?status=success&session_id={CHECKOUT_SESSION_ID}',
                'cancel_url' => config('app.frontend_url') . '/checkout.html?status=cancel',
            ]);

            return $session->url;
        } catch (Exception $e) {
            \Log::error("Stripe Checkout Session Failed: " . $e->getMessage());
            return null;
        }
    }
}
