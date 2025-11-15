<?php
// editare_imprumut.php - Editare împrumut
require_once 'config.php';

$mesaj = '';
$tip_mesaj = '';

// Verifică dacă avem ID
if (!isset($_GET['id']) || empty($_GET['id'])) {
    die('ID împrumut lipsă');
}

$id = (int)$_GET['id'];

// Obține datele împrumutului
$stmt = $pdo->prepare("
    SELECT
        i.*,
        c.titlu as carte_titlu,
        c.autor as carte_autor,
        cit.nume as cititor_nume,
        cit.prenume as cititor_prenume
    FROM imprumuturi i
    JOIN carti c ON i.cod_carte = c.cod_bare
    JOIN cititori cit ON i.cod_cititor = cit.cod_bare
    WHERE i.id = ?
");
$stmt->execute([$id]);
$imprumut = $stmt->fetch();

if (!$imprumut) {
    die('Împrumutul nu a fost găsit');
}

// Obține lista tuturor cărților disponibile
$carti_stmt = $pdo->query("SELECT cod_bare, titlu, autor FROM carti ORDER BY titlu");
$carti = $carti_stmt->fetchAll();

// Obține lista tuturor cititorilor
$cititori_stmt = $pdo->query("SELECT cod_bare, nume, prenume FROM cititori ORDER BY nume, prenume");
$cititori = $cititori_stmt->fetchAll();

// Procesare formular
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cod_cititor = trim($_POST['cod_cititor']);
    $cod_carte = trim($_POST['cod_carte']);
    $data_imprumut = trim($_POST['data_imprumut']);
    $data_returnare = trim($_POST['data_returnare']);
    $status = trim($_POST['status']);

    try {
        // Logică automată: Dacă status = "returnat" și nu ai dată, pune data curentă
        if ($status === 'returnat' && empty($data_returnare)) {
            $data_returnare = date('Y-m-d H:i:s');
        }
        
        // Logică automată: Dacă ai dată returnare, statusul devine automat "returnat"
        if (!empty($data_returnare)) {
            $status = 'returnat';
        }

        $stmt = $pdo->prepare("
            UPDATE imprumuturi
            SET cod_cititor = ?, cod_carte = ?, data_imprumut = ?, data_returnare = ?, status = ?
            WHERE id = ?
        ");

        // Convertește datele goale în NULL
        $data_returnare_null = empty($data_returnare) ? null : $data_returnare;

        $stmt->execute([$cod_cititor, $cod_carte, $data_imprumut, $data_returnare_null, $status, $id]);

        $mesaj = "✅ Împrumutul a fost actualizat cu succes!";
        $tip_mesaj = "success";

        // Reîncarcă datele
        $stmt = $pdo->prepare("
            SELECT
                i.*,
                c.titlu as carte_titlu,
                c.autor as carte_autor,
                cit.nume as cititor_nume,
                cit.prenume as cititor_prenume
            FROM imprumuturi i
            JOIN carti c ON i.cod_carte = c.cod_bare
            JOIN cititori cit ON i.cod_cititor = cit.cod_bare
            WHERE i.id = ?
        ");
        $stmt->execute([$id]);
        $imprumut = $stmt->fetch();

    } catch (PDOException $e) {
        $mesaj = "❌ Eroare: " . $e->getMessage();
        $tip_mesaj = "danger";
    }
}
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editare Împrumut - Sistem Bibliotecă</title>
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
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        h1 {
            color: #667eea;
            margin-bottom: 30px;
            font-size: 2.2em;
            text-align: center;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
            font-size: 1em;
        }

        select, input[type="datetime-local"], input[type="date"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }

        .required {
            color: #dc3545;
            font-weight: bold;
        }

        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .back-link, .home-link {
            display: inline-block;
            margin-top: 20px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 5px;
            transition: all 0.3s;
        }

        .home-link {
            background: #28a745;
            margin-right: 10px;
        }

        .home-link:hover {
            background: #218838;
        }

        .back-link {
            background: #667eea;
            color: white;
        }

        .back-link:hover {
            background: #764ba2;
        }

        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .info-box h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .preview-card {
            background: #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border-left: 4px solid #28a745;
        }

        .preview-card h4 {
            margin-bottom: 8px;
            color: #28a745;
            font-size: 1em;
        }

        .preview-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 0.9em;
        }

        .preview-item {
            display: flex;
            justify-content: space-between;
        }

        .preview-label {
            font-weight: 600;
            color: #666;
        }

        .preview-value {
            color: #333;
        }

        .status-select {
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #ddd;
            background: white;
        }

        .status-activ {
            background: #d4edda;
            color: #155724;
        }

        .status-returnat {
            background: #d1ecf1;
            color: #0c5460;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 Editare Împrumut</h1>

        <div class="info-box">
            <h3>💡 Informații utile</h3>
            <ul style="margin-left: 20px;">
                <li>Selectează cititorul și cartea din listele disponibile</li>
                <li>Data împrumutului este obligatorie</li>
                <li>Data returnării poate fi goală pentru împrumuturi active</li>
                <li>Statusul se actualizează automat când adaugi dată returnare</li>
            </ul>
        </div>

        <?php if (isset($mesaj)): ?>
            <div class="alert alert-<?php echo $tip_mesaj; ?>">
                <?php echo $mesaj; ?>
            </div>
        <?php endif; ?>

        <form method="POST" id="imprumutForm">
            <div class="form-group">
                <label>Cititor <span class="required">*</span></label>
                <select name="cod_cititor" required>
                    <option value="">Selectează cititor</option>
                    <?php foreach ($cititori as $cititor): ?>
                        <option value="<?php echo htmlspecialchars($cititor['cod_bare']); ?>"
                                <?php echo $imprumut['cod_cititor'] == $cititor['cod_bare'] ? 'selected' : ''; ?>>
                            <?php echo htmlspecialchars($cititor['nume'] . ' ' . $cititor['prenume'] . ' (' . $cititor['cod_bare'] . ')'); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-group">
                <label>Carte <span class="required">*</span></label>
                <select name="cod_carte" required>
                    <option value="">Selectează carte</option>
                    <?php foreach ($carti as $carte): ?>
                        <option value="<?php echo htmlspecialchars($carte['cod_bare']); ?>"
                                <?php echo $imprumut['cod_carte'] == $carte['cod_bare'] ? 'selected' : ''; ?>>
                            <?php echo htmlspecialchars($carte['titlu'] . ' - ' . ($carte['autor'] ?: 'Autor necunoscut') . ' (' . $carte['cod_bare'] . ')'); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-group">
                <label>Data împrumut <span class="required">*</span></label>
                <input type="datetime-local"
                       name="data_imprumut"
                       value="<?php echo date('Y-m-d\TH:i', strtotime($imprumut['data_imprumut'])); ?>"
                       required>
            </div>

            <div class="form-group">
                <label>Data returnare (opțional)</label>
                <input type="datetime-local"
                       name="data_returnare"
                       value="<?php echo $imprumut['data_returnare'] ? date('Y-m-d\TH:i', strtotime($imprumut['data_returnare'])) : ''; ?>">
            </div>

            <div class="form-group">
                <label>Status <span class="required">*</span></label>
                <select name="status" required>
                    <option value="activ" <?php echo $imprumut['status'] == 'activ' ? 'selected' : ''; ?>>Activ (împrumutată)</option>
                    <option value="returnat" <?php echo $imprumut['status'] == 'returnat' ? 'selected' : ''; ?>>Returnată</option>
                </select>
            </div>

            <button type="submit">💾 Salvează modificările</button>
        </form>

        <!-- Previzualizare împrumut -->
        <div class="preview-card">
            <h4>📖 Previzualizare împrumut</h4>
            <div class="preview-grid">
                <div class="preview-item">
                    <span class="preview-label">Cititor:</span>
                    <span class="preview-value" id="previewCititor">
                        <?php echo htmlspecialchars($imprumut['cititor_nume'] . ' ' . $imprumut['cititor_prenume']); ?>
                    </span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Carte:</span>
                    <span class="preview-value" id="previewCarte">
                        <?php echo htmlspecialchars($imprumut['carte_titlu']); ?>
                    </span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Data împrumut:</span>
                    <span class="preview-value" id="previewDataImprumut">
                        <?php echo date('d.m.Y H:i', strtotime($imprumut['data_imprumut'])); ?>
                    </span>
                </div>
                <div class="preview-item">
                    <span class="preview-label">Status:</span>
                    <span class="preview-value" id="previewStatus">
                        <?php echo $imprumut['status'] == 'activ' ? 'Activ' : 'Returnat'; ?>
                    </span>
                </div>
            </div>
        </div>

        <a href="index.php" class="home-link">🏠 Acasă</a>
        <a href="imprumuturi.php" class="back-link">← Înapoi la lista împrumuturi</a>
    </div>

    <script>
		// Actualizare previzualizare în timp real
		function updatePreview() {
			const cititorSelect = document.querySelector('select[name="cod_cititor"]');
			const carteSelect = document.querySelector('select[name="cod_carte"]');
			const dataInput = document.querySelector('input[name="data_imprumut"]');
			const statusSelect = document.querySelector('select[name="status"]');

			// Actualizează cititor
			const cititorOption = cititorSelect.options[cititorSelect.selectedIndex];
			document.getElementById('previewCititor').textContent =
				cititorOption ? cititorOption.text.split(' (')[0] : '-';

			// Actualizează carte
			const carteOption = carteSelect.options[carteSelect.selectedIndex];
			document.getElementById('previewCarte').textContent =
				carteOption ? carteOption.text.split(' (')[0] : '-';

			// Actualizează dată
			if (dataInput.value) {
				const date = new Date(dataInput.value);
				document.getElementById('previewDataImprumut').textContent =
					date.toLocaleDateString('ro-RO') + ' ' + date.toLocaleTimeString('ro-RO', {hour: '2-digit', minute: '2-digit'});
			}

			// Actualizează status
			document.getElementById('previewStatus').textContent =
				statusSelect.value === 'activ' ? 'Activ' : 'Returnat';
		}

		// Adaugă event listeners pentru actualizare în timp real
		document.querySelector('select[name="cod_cititor"]').addEventListener('change', updatePreview);
		document.querySelector('select[name="cod_carte"]').addEventListener('change', updatePreview);
		document.querySelector('input[name="data_imprumut"]').addEventListener('input', updatePreview);
		document.querySelector('select[name="status"]').addEventListener('change', updatePreview);

		// LOGICA NOUĂ: Când schimbi statusul manual
		document.querySelector('select[name="status"]').addEventListener('change', function() {
			const dataReturnareInput = document.querySelector('input[name="data_returnare"]');
			
			// Dacă selectezi "returnat" și nu ai dată, completează automat cu data curentă
			if (this.value === 'returnat' && !dataReturnareInput.value) {
				const now = new Date();
				const year = now.getFullYear();
				const month = String(now.getMonth() + 1).padStart(2, '0');
				const day = String(now.getDate()).padStart(2, '0');
				const hours = String(now.getHours()).padStart(2, '0');
				const minutes = String(now.getMinutes()).padStart(2, '0');
				
				dataReturnareInput.value = `${year}-${month}-${day}T${hours}:${minutes}`;
				
				alert('ℹ️ Data returnării a fost completată automat cu data curentă.\nPoți să o modifici dacă vrei.');
			}
			
			// Dacă selectezi "activ", șterge data returnării
			if (this.value === 'activ') {
				dataReturnareInput.value = '';
			}
			
			updatePreview();
		});

		// Când modifici data returnării manual
		document.querySelector('input[name="data_returnare"]').addEventListener('input', function() {
			const statusSelect = document.querySelector('select[name="status"]');
			
			// Doar sugerează, nu forța!
			if (this.value && statusSelect.value === 'activ') {
				if (confirm('💡 Ai completat data returnării.\n\nVrei să schimbi automat statusul în "Returnat"?')) {
					statusSelect.value = 'returnat';
				}
			}
			
			updatePreview();
		});

		// Resetare formular după succes
		<?php if (isset($mesaj) && $tip_mesaj === 'success'): ?>
			setTimeout(() => {
				updatePreview();
			}, 500);
		<?php endif; ?>
    </script>
</body>
</html>
