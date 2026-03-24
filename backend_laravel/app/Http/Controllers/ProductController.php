<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ProductController extends Controller
{
    public function index(Request $request)
    {
        $query = Product::query();

        if ($request->has('category')) {
            $query->where('category', $request->category);
        }

        if ($request->has('section')) {
            $query->where('section', $request->section);
        }

        if ($request->has('has_discount')) {
            $query->whereNotNull('discount')->where('discount', '!=', '');
        }

        if ($request->has('min_price')) {
            $query->where('price', '>=', (float) $request->min_price);
        }

        if ($request->has('max_price')) {
            $query->where('price', '<=', (float) $request->max_price);
        }

        $sortBy = $request->get('sort_by', 'created_at');
        $order = (int) $request->get('order', -1) === 1 ? 'asc' : 'desc';

        $products = $query->orderBy($sortBy, $order)->get();

        return response()->json($products);
    }

    public function show($id)
    {
        $product = Product::find($id);
        if (!$product) {
            return response()->json(['detail' => "Product $id not found"], 404);
        }
        return response()->json($product);
    }

    public function store(Request $request)
    {
        // Admin middleware usually handles auth check, but we could add it here too
        $data = $request->all();
        $product = Product::create($data);
        return response()->json($product, 201);
    }

    public function update(Request $request, $id)
    {
        $product = Product::find($id);
        if (!$product) {
            return response()->json(['detail' => "Product $id not found"], 404);
        }

        $data = $request->all();
        unset($data['_id']); // Avoid MongoDB errors

        $product->update($data);
        return response()->json($product);
    }

    public function destroy($id)
    {
        $product = Product::find($id);
        if (!$product) {
            return response()->json(['detail' => "Product $id not found"], 404);
        }

        $product->delete();
        return response()->json(null, 204);
    }
}
