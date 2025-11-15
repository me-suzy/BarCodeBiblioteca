<?php
// scan_barcode.php - Recepționează coduri de la Python scanner
header('Content-Type: application/json');
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Doar POST acceptat']);
    exit;
}

$barcode = trim($_POST['barcode'] ?? '');

if (empty($barcode)) {
    echo json_encode(['success' => false, 'message' => 'Cod de bare lipsă!']);
    exit;
}

// Funcție pentru normalizarea codului (elimină zero-urile leading din număr)
function normalize_barcode($code) {
    // Extrage prefix (literele) și număr
    if (preg_match('/^([A-Z]+)0*(\d+)$/', $code, $matches)) {
        $prefix = $matches[1];  // BOOK, USER
        $number = $matches[2];  // 2, 1, 15
        
        // Returnează ambele variante posibile
        return [
            $code,                                    // BOOK0002 (original)
            $prefix . $number,                        // BOOK2
            $prefix . str_pad($number, 3, '0', STR_PAD_LEFT),  // BOOK002
            $prefix . str_pad($number, 4, '0', STR_PAD_LEFT),  // BOOK0002
        ];
    }
    return [$code];
}

try {
    $barcode_variants = normalize_barcode($barcode);
    
    // Verifică dacă este cod de carte (BOOK*)
    if (strpos($barcode, 'BOOK') === 0) {
        // Caută în toate variantele posibile
        $placeholders = implode(',', array_fill(0, count($barcode_variants), '?'));
        $stmt = $pdo->prepare("
            SELECT cod_bare, titlu, autor 
            FROM carti 
            WHERE cod_bare IN ($placeholders)
            LIMIT 1
        ");
        $stmt->execute($barcode_variants);
        $carte = $stmt->fetch();
        
        if ($carte) {
            echo json_encode([
                'success' => true,
                'type' => 'carte',
                'message' => "📚 Carte găsită!\n\n" . 
                            "Titlu: {$carte['titlu']}\n" .
                            "Autor: {$carte['autor']}\n" .
                            "Cod: {$carte['cod_bare']}",
                'data' => $carte
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'type' => 'carte',
                'message' => "❌ Cartea nu există în baza de date!\n\n" .
                            "Cod scanat: {$barcode}\n" .
                            "Variante căutate: " . implode(', ', $barcode_variants)
            ]);
        }
    }
    // Verifică dacă este cod de cititor (USER*)
    elseif (strpos($barcode, 'USER') === 0) {
        // Caută în toate variantele posibile
        $placeholders = implode(',', array_fill(0, count($barcode_variants), '?'));
        $stmt = $pdo->prepare("
            SELECT cod_bare, nume, prenume, telefon, email 
            FROM cititori 
            WHERE cod_bare IN ($placeholders)
            LIMIT 1
        ");
        $stmt->execute($barcode_variants);
        $cititor = $stmt->fetch();
        
        if ($cititor) {
            echo json_encode([
                'success' => true,
                'type' => 'cititor',
                'message' => "👤 Cititor găsit!\n\n" .
                            "Nume: {$cititor['nume']} {$cititor['prenume']}\n" .
                            "Telefon: {$cititor['telefon']}\n" .
                            "Email: {$cititor['email']}\n" .
                            "Cod: {$cititor['cod_bare']}",
                'data' => $cititor
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'type' => 'cititor',
                'message' => "❌ Cititorul nu există în baza de date!\n\n" .
                            "Cod scanat: {$barcode}\n" .
                            "Variante căutate: " . implode(', ', $barcode_variants)
            ]);
        }
    }
    // Cod necunoscut
    else {
        echo json_encode([
            'success' => false,
            'message' => "❓ Cod necunoscut: {$barcode}\n\n" .
                        "Formatul așteptat: BOOK#### sau USER###"
        ]);
    }
    
} catch (PDOException $e) {
    echo json_encode([
        'success' => false,
        'message' => '❌ Eroare bază de date: ' . $e->getMessage()
    ]);
}
?>