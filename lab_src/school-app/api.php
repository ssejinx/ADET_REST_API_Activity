<?php
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, X-Admin-Token");

// 1. Database Connection
$conn = @new mysqli("localhost", "root", "", "art_db");
if ($conn->connect_error) {
    http_response_code(500);
    exit(json_encode(["error" => "Database Connection Failed"]));
}

$method = $_SERVER['REQUEST_METHOD'];
$ADMIN_TOKEN = "1";
$JSON_FILE = 'verified_artists.json'; //The JSON file 

// YNC FUNCTION: Updates the JSON file with SQL data 
function syncJSON($conn) {
    global $JSON_FILE;
    $result = $conn->query("SELECT username, bio FROM artists");
    $data = $result->fetch_all(MYSQLI_ASSOC);
    file_put_contents($JSON_FILE, json_encode($data, JSON_PRETTY_PRINT));
}

$client_token = $_SERVER['HTTP_X_ADMIN_TOKEN'] ?? '';
$is_admin = ($client_token === $ADMIN_TOKEN);
$input = json_decode(file_get_contents('php://input'), true);
$action = $_GET['action'] ?? '';
$username = $_GET['username'] ?? $input['username'] ?? null;

switch($method) {
    case 'GET':
        if ($action == 'verify') {
            $stmt = $conn->prepare("SELECT username, bio FROM artists WHERE username = ?");
            $stmt->bind_param("s", $username);
            $stmt->execute();
            $res = $stmt->get_result()->fetch_assoc();
            echo json_encode($res ? ["status" => "verified", "user" => $res] : ["error" => "Not found"]);
        } elseif ($is_admin) {
            $table = ($action == 'pending') ? 'pending_requests' : 'artists';
            $result = $conn->query("SELECT * FROM $table");
            echo json_encode($result->fetch_all(MYSQLI_ASSOC));
        } else {
            http_response_code(401);
            echo json_encode(["error" => "Unauthorized"]);
        }
        break;

    case 'POST':
        if ($action == 'request') { 
            $u = trim($input['username'] ?? ''); 
            $b = trim($input['bio'] ?? '');
            if (!$u || !$b) { http_response_code(400); exit(json_encode(["error" => "Missing data"])); }

            $check = $conn->prepare("SELECT username FROM artists WHERE username = ? UNION SELECT username FROM pending_requests WHERE username = ?");
            $check->bind_param("ss", $u, $u);
            $check->execute();
            if ($check->get_result()->num_rows > 0) {
                http_response_code(409);
                exit(json_encode(["error" => "Username taken or pending."]));
            }
            
            $stmt = $conn->prepare("INSERT INTO pending_requests (username, bio) VALUES (?, ?)");
            $stmt->bind_param("ss", $u, $b);
            if ($stmt->execute()) echo json_encode(["message" => "Request sent!"]);
        } 
        elseif ($is_admin && $action == 'approve') { 
            $stmt = $conn->prepare("INSERT INTO artists (username, bio) SELECT username, bio FROM pending_requests WHERE username = ?");
            $stmt->bind_param("s", $username);
            if ($stmt->execute()) {
                $conn->query("DELETE FROM pending_requests WHERE username = '$username'");
                syncJSON($conn); // UPDATE JSON FILE
                echo json_encode(["message" => "Artist approved & JSON updated!"]);
            }
        }
        break;

    case 'PUT':
        if (!$is_admin) { http_response_code(401); exit; }
        $stmt = $conn->prepare("UPDATE artists SET bio = ? WHERE username = ?");
        $stmt->bind_param("ss", $input['bio'], $username);
        $stmt->execute();
        syncJSON($conn); // UPDATE JSON FILE
        echo json_encode(["message" => "Bio updated in SQL & JSON"]);
        break;

    case 'DELETE':
        if (!$is_admin) { http_response_code(401); exit; }
        $table = ($action == 'reject') ? 'pending_requests' : 'artists';
        $stmt = $conn->prepare("DELETE FROM $table WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        if ($table == 'artists') syncJSON($conn); // UPDATE JSON FILE
        echo json_encode(["message" => "Removed successfully"]);
        break;
}
$conn->close();