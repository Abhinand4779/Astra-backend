<?php

namespace App\Http\Controllers;

use App\Models\Setting;
use Illuminate\Http\Request;

class SettingController extends Controller
{
    public function index()
    {
        $setting = Setting::where('id', 'site_config')->first();
        if (!$setting) {
            return response()->json(['config' => []]);
        }
        return response()->json(['config' => $setting->config ?? []]);
    }

    public function update(Request $request)
    {
        $admin = auth()->user();
        if (!$admin || !$admin->is_admin) {
            return response()->json(['detail' => 'Unauthorized'], 403);
        }

        $data = $request->all();

        Setting::updateOrCreate(
            ['id' => 'site_config'],
            ['config' => $data, 'lastUpdated' => now()]
        );

        return response()->json(['message' => 'Settings updated successfully']);
    }
}
