<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\SettingController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::get('/ping', function() {
    return response()->json(['status' => 'pong']);
});

// Public Routes
Route::get('/products', [ProductController::class, 'index']);
Route::get('/products/', [ProductController::class, 'index']);
Route::get('/products/{id}', [ProductController::class, 'show']);

Route::get('/categories', [CategoryController::class, 'index']);
Route::get('/categories/{id}', [CategoryController::class, 'show']);

Route::get('/settings', [SettingController::class, 'index']);
Route::get('/settings/', [SettingController::class, 'index']);

Route::post('/auth/register', [AuthController::class, 'register']);
Route::post('/auth/register/', [AuthController::class, 'register']);
Route::post('/auth/login', [AuthController::class, 'login']);
Route::post('/auth/login/', [AuthController::class, 'login']);
Route::post('/auth/admin/login', [AuthController::class, 'adminLogin']);

// Guest Order Route
Route::post('/orders', [OrderController::class, 'store']);
Route::post('/orders/', [OrderController::class, 'store']);

// Protected Routes
Route::middleware('auth:api')->group(function () {
    Route::get('/auth/me', [AuthController::class, 'me']);
    Route::get('/orders/my-orders', [OrderController::class, 'myOrders']);

    // Admin Routes
    Route::middleware('admin')->group(function () {
        // Products
        Route::post('/products', [ProductController::class, 'store']);
        Route::put('/products/{id}', [ProductController::class, 'update']);
        Route::delete('/products/{id}', [ProductController::class, 'destroy']);

        // Categories
        Route::post('/categories', [CategoryController::class, 'store']);
        Route::delete('/categories/{id}', [CategoryController::class, 'destroy']);

        // Settings
        Route::post('/settings', [SettingController::class, 'update']);
        Route::post('/settings/', [SettingController::class, 'update']);

        // Orders
        Route::get('/orders/all', [OrderController::class, 'allOrders']);
        Route::put('/orders/{id}/status', [OrderController::class, 'updateStatus']);

        // Admin - User Management
        Route::get('/auth/all', [AuthController::class, 'listAll']);
        Route::delete('/auth/user/{user_id}', [AuthController::class, 'deleteUser']);
    });
});
