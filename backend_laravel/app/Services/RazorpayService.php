<?php

namespace App\Services;

use Razorpay\Api\Api;
use Exception;

class RazorpayService
{
    protected static $api;

    public static function init()
    {
        $keyId = env('RAZORPAY_KEY_ID');
        $keySecret = env('RAZORPAY_KEY_SECRET');

        if ($keyId && $keySecret && !str_contains($keyId, 'Here')) {
            try {
                self::$api = new Api($keyId, $keySecret);
            } catch (Exception $e) {
                \Log::error("Razorpay Init Error: " . $e->getMessage());
            }
        }
    }

    public static function createCheckoutSession($orderId, $amountInRupees, $customerEmail, $customerName = "", $customerPhone = "")
    {
        try {
            if (!self::$api) {
                self::init();
            }

            if (!self::$api) {
                return null;
            }

            if ($amountInRupees <= 0) {
                return null;
            }

            $amountInPaise = (int) ($amountInRupees * 100);
            $callbackUrl = env('FRONTEND_URL', 'http://localhost:5173') . '/orders?success=true';

            $paymentLink = self::$api->paymentLink->create([
                "amount" => $amountInPaise,
                "currency" => "INR",
                "accept_partial" => false,
                "description" => "Order #$orderId",
                "customer" => [
                    "email" => $customerEmail,
                    "name" => $customerName,
                    "contact" => $customerPhone
                ],
                "notify" => [
                    "sms" => false,
                    "email" => true
                ],
                "reminder_enable" => true,
                "callback_url" => $callbackUrl,
                "callback_method" => "get"
            ]);

            return $paymentLink['short_url'];
        } catch (Exception $e) {
            \Log::error("Razorpay Checkout Error: " . $e->getMessage());
            return null;
        }
    }
}
