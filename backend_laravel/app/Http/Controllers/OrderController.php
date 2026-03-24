<?php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Models\User;
use App\Services\EmailService;
use App\Services\StripeService;
use Illuminate\Http\Request;
use Exception;

class OrderController extends Controller
{
    public function store(Request $request)
    {
        $orderData = $request->all();
        $user = null;

        try {
            if ($token = \Tymon\JWTAuth\Facades\JWTAuth::getToken()) {
                $user = \Tymon\JWTAuth\Facades\JWTAuth::parseToken()->authenticate();
            }
        } catch (Exception $e) {
            $user = null;
        }

        if ($user) {
            $orderData['user_id'] = (string) $user->_id;
            $userEmail = $user->email;
        } else {
            $orderData['user_id'] = 'guest';
            $userEmail = $orderData['shipping_address']['email'] ?? null;
        }

        if (!$userEmail) {
            return response()->json(['detail' => 'Customer email is required for the order'], 400);
        }

        $orderData['created_at'] = now();
        $orderData['status'] = 'Pending';
        $order = Order::create($orderData);

        // Send Confirmation Email
        EmailService::sendOrderConfirmation($order, $userEmail);

        // Generate Stripe Checkout URL
        try {
            $numeric_total_str = preg_replace('/[^0-9]/', '', (string) $orderData['total_amount']);
            if ($numeric_total_str) {
                $numericTotal = (int) $numeric_total_str;
                $customerName = $orderData['shipping_address']['firstName'] ?? 'Customer';
                $customerPhone = $orderData['shipping_address']['phone'] ?? '';

                $checkoutUrl = \App\Services\StripeService::createCheckoutSession(
                    $order->_id,
                    $numericTotal,
                    $userEmail,
                    $customerName,
                    $customerPhone
                );

                if ($checkoutUrl) {
                    return response()->json([
                        '_id' => $order->_id,
                        'checkout_url' => $checkoutUrl
                    ], 201);
                }
            }
        } catch (Exception $e) {
            \Log::error("Stripe Checkout Link Generation Failed: " . $e->getMessage());
        }

        return response()->json($order, 201);
    }

    public function myOrders()
    {
        $user = auth()->user();
        if (!$user) {
            return response()->json(['detail' => 'Not authenticated'], 401);
        }

        $orders = Order::where('user_id', (string) $user->_id)->get();
        return response()->json($orders);
    }

    public function allOrders()
    {
        $admin = auth()->user();
        if (!$admin || !$admin->is_admin) {
            return response()->json(['detail' => 'Unauthorized'], 403);
        }

        $orders = Order::all();
        return response()->json($orders);
    }

    public function updateStatus(Request $request, $id)
    {
        $admin = auth()->user();
        if (!$admin || !$admin->is_admin) {
            return response()->json(['detail' => 'Unauthorized'], 403);
        }

        $order = Order::find($id);
        if (!$order) {
            return response()->json(['detail' => "Order $id not found"], 404);
        }

        $orderStatus = $request->query('order_status');
        $trackingId = $request->query('tracking_id');
        $trackingUrl = $request->query('tracking_url');

        $updateData = ['status' => $orderStatus];
        if ($trackingId)
            $updateData['tracking_id'] = $trackingId;
        if ($trackingUrl)
            $updateData['tracking_url'] = $trackingUrl;

        $order->update($updateData);

        // If shipped, send notification
        if (in_array(strtolower($orderStatus), ['shipped', 'delivered'])) {
            $customerEmail = $order->shipping_address['email'] ?? null;
            if ($order->user_id !== 'guest') {
                $user = User::find($order->user_id);
                if ($user) {
                    $customerEmail = $user->email;
                }
            }

            if ($customerEmail) {
                EmailService::sendShippingNotification($id, $customerEmail, $trackingId ?? 'N/A', $trackingUrl ?? '#');
            }
        }

        return response()->json(['message' => 'Order status updated successfully']);
    }
}
