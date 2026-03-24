<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

class Product extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'products';

    protected $fillable = [
        'name',
        'alias',
        'price',
        'discount',
        'category',
        'section',
        'image_url',
        'stock',
        'description',
        'colors',
        'sizes',
        'is_featured',
        'is_new_arrival',
        'average_rating',
        'num_reviews'
    ];

    protected $casts = [
        'price' => 'float',
        'stock' => 'integer',
        'is_featured' => 'boolean',
        'is_new_arrival' => 'boolean',
        'average_rating' => 'float',
        'num_reviews' => 'integer',
    ];
}
