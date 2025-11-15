<?php
// index.php - Pagina principală cu scanare coduri de bare
require_once 'config.php';
session_start();

// Procesare formular
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $actiune = $_POST['actiune'] ?? '';
    $cod_cititor = trim($_POST['cod_cititor'] ?? '');
    $cod_carte = trim($_POST['cod_carte'] ?? '');

    if ($actiune === 'imprumuta' && $cod_cititor && $cod_carte) {
        try {
            // Verifică dacă cartea este deja împrumutată
            $stmt = $pdo->prepare("SELECT * FROM imprumuturi WHERE cod_carte = ? AND status = 'activ'");
            $stmt->execute([$cod_carte]);

            if ($stmt->rowCount() > 0) {
                $mesaj = "⚠️ Cartea este deja împrumutată!";
                $tip_mesaj = "warning";
            } else {
                // Înregistrează împrumutul
                $stmt = $pdo->prepare("INSERT INTO imprumuturi (cod_cititor, cod_carte, status) VALUES (?, ?, 'activ')");
                $stmt->execute([$cod_cititor, $cod_carte]);

                $mesaj = "✅ Împrumut înregistrat cu succes!";
                $tip_mesaj = "success";
            }
        } catch (PDOException $e) {
            $mesaj = "❌ Eroare: " . $e->getMessage();
            $tip_mesaj = "danger";
        }
    }

if ($actiune === 'returneaza' && $cod_carte) {  // Nu mai verificăm cod_cititor obligatoriu
    try {
        // VERIFICĂM MAI ÎNTÂI CINE ARE CARTEA ÎMPRUMUTATĂ
        $stmt = $pdo->prepare("
            SELECT i.*, c.nume, c.prenume 
            FROM imprumuturi i
            JOIN cititori c ON i.cod_cititor = c.cod_bare
            WHERE i.cod_carte = ? AND i.status = 'activ'
        ");
        $stmt->execute([$cod_carte]);
        $imprumut = $stmt->fetch();

        if ($imprumut) {
            // Marchează cartea ca returnată
            $update_stmt = $pdo->prepare("
                UPDATE imprumuturi
                SET status = 'returnat', data_returnare = NOW()
                WHERE cod_carte = ? AND status = 'activ'
            ");
            $update_stmt->execute([$cod_carte]);

            $mesaj = "✅ Cartea a fost returnată cu succes!\n" .
                     "Împrumutată de: " . htmlspecialchars($imprumut['nume'] . ' ' . $imprumut['prenume']) .
                     " (" . htmlspecialchars($imprumut['cod_cititor']) . ")";
            $tip_mesaj = "success";
        } else {
            $mesaj = "⚠️ Cartea nu este împrumutată! Nu există un împrumut activ pentru codul: " . htmlspecialchars($cod_carte);
            $tip_mesaj = "warning";
        }
    } catch (PDOException $e) {
        $mesaj = "❌ Eroare: " . $e->getMessage();
        $tip_mesaj = "danger";
    }
}
}

// Obține statistici
$total_carti = $pdo->query("SELECT COUNT(*) FROM carti")->fetchColumn();
$total_cititori = $pdo->query("SELECT COUNT(*) FROM cititori")->fetchColumn();
$carti_imprumutate = $pdo->query("SELECT COUNT(*) FROM imprumuturi WHERE status = 'activ'")->fetchColumn();
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Bibliotecă - Scanare Coduri de Bare</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stat-card.clickable {
            cursor: pointer;
            text-decoration: none;
            display: block;
        }

        .stat-card.clickable:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }

        .stat-card h3 {
            font-size: 2em;
            margin-bottom: 5px;
        }

        .stat-card p {
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .click-hint {
            font-size: 0.8em;
            opacity: 0.7;
            display: block;
        }

        .scan-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .scan-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
            font-size: 1.1em;
        }

        .form-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1.1em;
            transition: border-color 0.3s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 25px;
        }

        button {
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .btn-imprumuta {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }

        .btn-returneaza {
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
            color: white;
        }

        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 1.1em;
            font-weight: 500;
        }

        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }

        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .instructions {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .instructions h3 {
            color: #667eea;
            margin-bottom: 15px;
        }

        .instructions ol {
            margin-left: 20px;
        }

        .instructions li {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .nav-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .nav-links a {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .nav-links a:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Sistem Bibliotecă</h1>
            <p style="color: #666; font-size: 1.1em;">Scanare coduri de bare pentru împrumuturi</p>

            <div class="stats">
                <a href="carti.php" class="stat-card clickable">
                    <h3><?php echo $total_carti; ?></h3>
                    <p>Total cărți</p>
                    <span class="click-hint">Click pentru detalii</span>
                </a>
                <a href="cititori.php" class="stat-card clickable">
                    <h3><?php echo $total_cititori; ?></h3>
                    <p>Cititori înregistrați</p>
                    <span class="click-hint">Click pentru detalii</span>
                </a>
                <a href="imprumuturi.php" class="stat-card clickable">
                    <h3><?php echo $carti_imprumutate; ?></h3>
                    <p>Cărți împrumutate</p>
                    <span class="click-hint">Click pentru detalii</span>
                </a>
            </div>

            <div class="nav-links">
                <a href="rapoarte.php">📊 Rapoarte</a>
                <a href="adauga_carte.php">➕ Adaugă carte</a>
                <a href="adauga_cititor.php">👤 Adaugă cititor</a>
            </div>
        </div>

        <?php if (isset($mesaj)): ?>
            <div class="alert alert-<?php echo $tip_mesaj; ?>">
                <?php echo $mesaj; ?>
            </div>
        <?php endif; ?>

        <div class="scan-section">
            <h2>🔍 Scanare Coduri</h2>

            <form method="POST" id="scanForm">
                <div class="form-group">
                    <label for="cod_cititor">1️⃣ Scanează carnetul cititorului:</label>
                    <input type="text"
                           id="cod_cititor"
                           name="cod_cititor"
                           placeholder="Scanează sau introdu codul cititorului (ex: USER001)"
                           autofocus
                           required>
                </div>

                <div class="form-group">
                    <label for="cod_carte">2️⃣ Scanează codul cărții:</label>
                    <input type="text"
                           id="cod_carte"
                           name="cod_carte"
                           placeholder="Scanează sau introdu codul cărții (ex: BOOK001)"
                           required>
                </div>

                <div class="button-group">
                    <button type="submit" name="actiune" value="imprumuta" class="btn-imprumuta">
                        📤 Împrumută carte
                    </button>
                    <button type="submit" name="actiune" value="returneaza" class="btn-returneaza">
                        📥 Returnează carte
                    </button>
                </div>
            </form>

            <div class="instructions">
                <h3>📋 Instrucțiuni de utilizare:</h3>
                <ol>
                    <li>Scanează <strong>carnetul cititorului</strong> în primul câmp</li>
                    <li>Scanează <strong>codul de bare al cărții</strong> în al doilea câmp</li>
                    <li>Apasă <strong>"Împrumută carte"</strong> când cititorul ia cartea</li>
                    <li>Apasă <strong>"Returnează carte"</strong> când cititorul aduce cartea înapoi</li>
                </ol>
            </div>
        </div>
    </div>

    <script>
        // Auto-focus pe câmpul carte după scanarea cititorului
        document.getElementById('cod_cititor').addEventListener('input', function() {
            if (this.value.length > 3) {
                setTimeout(() => {
                    document.getElementById('cod_carte').focus();
                }, 100);
            }
        });

        // Auto-submit după scanarea cărții (opțional)
        document.getElementById('cod_carte').addEventListener('input', function() {
            // Poți activa auto-submit dacă vrei
            // if (this.value.length > 3) {
            //     document.querySelector('.btn-imprumuta').click();
            // }
        });

        // Resetare formular după submit
        <?php if (isset($mesaj) && $tip_mesaj === 'success'): ?>
            setTimeout(() => {
                document.getElementById('scanForm').reset();
                document.getElementById('cod_cititor').focus();
            }, 1500);
        <?php endif; ?>
    </script>
</body>
</html>
