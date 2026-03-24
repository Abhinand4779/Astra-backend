<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Models\Order;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Tymon\JWTAuth\Facades\JWTAuth;
use Exception;

class AuthController extends Controller
{
    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users,email',
            'password' => 'required|string|min:6',
        ]);

        if ($validator->fails()) {
            return response()->json($validator->errors(), 400);
        }

        try {
            $user = User::create([
                'name' => $request->name,
                'email' => $request->email,
                'password' => Hash::make($request->password),
                'role' => $request->role ?? 'user',
                'is_admin' => $request->is_admin ?? false,
                'cart' => [],
                'wishlist' => [],
                'created_at' => now(),
            ]);

            return response()->json($user, 201);
        } catch (Exception $e) {
            \Log::error("Registration Failed: " . $e->getMessage());
            return response()->json(['detail' => 'Could not create account. Please try again.'], 500);
        }
    }

    public function login(Request $request)
    {
        $email = $request->input('email') ?? $request->input('username');
        $credentials = ['email' => $email, 'password' => $request->input('password')];

        try {
            if (!$token = JWTAuth::attempt($credentials)) {
                return response()->json(['detail' => 'Incorrect email or password'], 401);
            }
        } catch (Exception $e) {
            return response()->json(['error' => 'Could not create token'], 500);
        }

        return response()->json([
            'access_token' => $token,
            'token_type' => 'bearer'
        ]);
    }

    public function adminLogin(Request $request)
    {
        $credentials = $request->only('email', 'password');

        try {
            if (!$token = JWTAuth::attempt($credentials)) {
                return response()->json(['detail' => 'Incorrect email or password'], 401);
            }

            $user = auth()->user();
            if (!$user->is_admin) {
                return response()->json(['detail' => 'Unauthorized. Admin access required.'], 403);
            }
        } catch (Exception $e) {
            return response()->json(['error' => 'Could not create token'], 500);
        }

        return response()->json([
            'access_token' => $token,
            'token_type' => 'bearer',
            'user' => $user
        ]);
    }

    public function me()
    {
        return response()->json(auth()->user());
    }

    public function listAll(Request $request)
    {
        $admin = auth()->user();
        if (!$admin || !$admin->is_admin) {
            return response()->json(['detail' => 'Unauthorized'], 403);
        }

        try {
            $users = User::all()->map(function ($user) {
                // Simplified calculations to mirror FastAPI logic
                $userIdStr = (string) $user->_id;
                $orderCount = Order::where('user_id', $userIdStr)->count();
                $orders = Order::where('user_id', $userIdStr)->get();

                $totalSpent = 0;
                foreach ($orders as $ord) {
                    $amount_str = preg_replace('/[^0-9]/', '', (string) $ord->total_amount);
                    $totalSpent += $amount_str ? intval($amount_str) : 0;
                }

                return [
                    '_id' => $userIdStr,
                    'id' => $userIdStr,
                    'name' => $user->name ?? 'Unknown',
                    'email' => $user->email,
                    'is_admin' => (bool) $user->is_admin,
                    'orders' => $orderCount,
                    'spent' => "₹" . number_format($totalSpent),
                    'joining' => $user->created_at ? $user->created_at->format('d M Y') : now()->format('d M Y'),
                    'status' => 'Active'
                ];
            });

            return response()->json($users);
        } catch (Exception $e) {
            return response()->json(['detail' => 'Error fetching customer directory'], 500);
        }
    }

    public function deleteUser($user_id)
    {
        $admin = auth()->user();
        if (!$admin || !$admin->is_admin) {
            return response()->json(['detail' => 'Unauthorized'], 403);
        }

        if ((string) $admin->_id === $user_id) {
            return response()->json(['detail' => 'Safety Guard: You cannot delete your own administrator account while logged in.'], 400);
        }

        $user = User::find($user_id);
        if (!$user) {
            return response()->json(['detail' => 'User not found'], 404);
        }

        if ($user->email === 'admin@astra.in') {
            return response()->json(['detail' => 'The primary administrator account is protected and cannot be deleted.'], 403);
        }

        $user->delete();
        return response()->json(['message' => 'User deleted successfully']);
    }
}
