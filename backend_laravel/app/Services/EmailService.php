<?php

namespace App\Services;

use Illuminate\Support\Facades\Mail;
use Exception;

class EmailService
{
    public static function sendOrderConfirmation($order, $customerEmail)
    {
        try {
            $itemsHtml = "";
            foreach ($order['items'] as $item) {
                $itemsHtml .= "<li>{$item['name']} - {$item['price']} (x{$item['quantity']})</li>";
            }

            $html = "
            <div style=\"font-family: Arial, sans-serif; padding: 20px; color: #333;\">
                <h2 style=\"color: #9c844a;\">Thank you for choosing ASTRA!</h2>
                <p>Dear Customer,</p>
                <p>Your order <strong>#{$order['_id']}</strong> has been successfully placed. We are preparing it with care.</p>
                
                <h3>Order Summary:</h3>
                <ul>{$itemsHtml}</ul>
                <p><strong>Total: {$order['total_amount']}</strong></p>
                
                <p>We'll notify you as soon as your items are shipped!</p>
                <hr>
                <p style=\"font-size: 12px; color: #999;\">ASTRA by Ash - Elegance in Every Detail.</p>
            </div>";

            Mail::html($html, function ($message) use ($customerEmail) {
                $message->to($customerEmail)
                    ->subject("Thank you for your Order! - ASTRA by Ash");
            });

            return true;
        } catch (Exception $e) {
            \Log::error("Email Error: " . $e->getMessage());
            return false;
        }
    }

    public static function sendShippingNotification($orderId, $customerEmail, $trackingId, $trackingUrl)
    {
        try {
            $html = "
            <div style=\"font-family: Arial, sans-serif; padding: 20px; color: #333;\">
                <h2 style=\"color: #9c844a;\">Your Order is Shipped!</h2>
                <p>Great news! Your order <strong>#{$orderId}</strong> is now on its way to you.</p>
                
                <p><strong>Tracking ID:</strong> {$trackingId}</p>
                <p><a href=\"{$trackingUrl}\" style=\"background: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;\">Track Shipment</a></p>
                
                <p>We hope you love your new ASTRA pieces!</p>
                <hr>
                <p style=\"font-size: 12px; color: #999;\">ASTRA by Ash</p>
            </div>";

            Mail::html($html, function ($message) use ($customerEmail) {
                $message->to($customerEmail)
                    ->subject("Your ASTRA Order is on its way! 🚀");
            });

            return true;
        } catch (Exception $e) {
            \Log::error("Email Error: " . $e->getMessage());
            return false;
        }
    }
}
