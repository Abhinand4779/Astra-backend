<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

try {
    print_r(DB::connection("mongodb")->getMongoClient()->listDatabaseNames()->toArray());
    echo "\nMongoDB Connected Successfully!\n";
} catch (\Exception $e) {
    echo $e->getMessage();
}
