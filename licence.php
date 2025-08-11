<?php
class DotEnv {
    protected $path;

    public function __construct(string $path) {
        if (!file_exists($path)) {
            // Hentikan dengan pesan error
            die("File .env tidak ditemukan di: {$path}");
        }
        $this->path = $path;
    }

    public function load(): void {
        if (!is_readable($this->path)) {
            die("File .env tidak bisa dibaca.");
        }

        $lines = file($this->path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            if (strpos(trim($line), '#') === 0) continue;
            if (!str_contains($line, '=')) continue;

            list($name, $value) = explode('=', $line, 2);
            $name = trim($name);
            $value = trim($value);

            if (!array_key_exists($name, $_SERVER) && !array_key_exists($name, $_ENV)) {
                putenv("{$name}={$value}");
                $_ENV[$name] = $value;
                $_SERVER[$name] = $value;
            }
        }
    }
}

// Muat .env
$env_path = $_SERVER['DOCUMENT_ROOT'] . '/.env';
(new DotEnv($env_path))->load();

// Ambil data lisensi
$license = getenv('LICENSE_KEY') ?: '';

if (empty($license)) {
    header('Location: /licence-error.php?error=missing_key');
    exit();
}

$params = [
    'license_key' => $license,
    'domain' => $_SERVER['SERVER_NAME'] ?? 'unknown'
];

// Kirim ke API lisensi
$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => 'https://api-list.seaker877.workers.dev/license/verify',
    CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded'],
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query($params),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true
]);

$response = curl_exec($ch);
$curl_error = curl_error($ch);
curl_close($ch);

// Jika gagal koneksi
if (!$response) {
    header('Location: /licence-error.php?error=curl_failed');
    exit();
}

// Cek response JSON
$data = json_decode($response, true);
if (!is_array($data)) {
    header('Location: /licence-error.php?error=invalid_response');
    exit();
}

// Validasi status lisensi
switch ((int) $data['code']) {
    case 200:
        if ($data['license_status'] !== 'active') {
            header('Location: /licence-error.php?error=expired');
            exit();
        }
        break;
    case 404:
        header('Location: /licence-error.php?error=not_found');
        exit();
    case 400:
        header('Location: /licence-error.php?error=domain_invalid');
        exit();
    default:
        header('Location: /licence-error.php?error=unknown');
        exit();
}
