<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

class Order extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'orders';

    protected $fillable = [
        'user_id',
        'items',
        'total_amount',
        'status',
        'shipping_address',
        'payment_id',
        'tracking_id',
        'tracking_url',
        'created_at',
        'updated_at'
    ];

    protected $casts = [
        'items' => 'array',
        'shipping_address' => 'array'
    ];
}
