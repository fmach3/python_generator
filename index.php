<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['prompt'])) {
    $prompt = $_POST['prompt'];

    // Execute the Python script to generate PHP code
    $pythonScriptPath = __DIR__ . '/autogen1.py'; // Path to your Python script
    $command = "python3 " . escapeshellarg($pythonScriptPath) . " " . escapeshellarg($prompt);
    exec($command, $output, $return_var);

    #if ($return_var === 0) {
    if (1) {
        // Python script executed successfully
        $generatedPhpCode = implode("\n", $output);

        // Save the generated PHP code to a timestamped file in the "generated" subfolder
        $generatedFolder = __DIR__ . '/generated'; // Path to the "generated" subfolder
        if (!is_dir($generatedFolder)) {
            mkdir($generatedFolder, 0755, true); // Create the folder if it doesn't exist
        }

        $timestamp = date('Y-m-d-His') . '.php';
        $filePath = $generatedFolder . '/' . $timestamp;
        file_put_contents($filePath, $generatedPhpCode);

        // Redirect to the newly generated PHP file in a new browser window
        $fileUrl = 'generated/' . $timestamp; // Relative URL to the generated file
        echo "<script>window.open('" . $fileUrl . "', '_blank');</script>";
    } else {
        // Handle errors
        echo '<p style="color: red;">Error generating PHP code:</p>';
        echo '<pre>' . htmlspecialchars(implode("\n", $output)) . '</pre>';
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Code Generator</title>
</head>
<body>
    <h1>PHP Code Generator</h1>
    <form method="post" action="<?= htmlspecialchars($_SERVER['PHP_SELF']) ?>">
        <label for="prompt">Enter Prompt:</label><br>
        <textarea id="prompt" name="prompt" rows="10" cols="50" required></textarea><br><br>
        <input type="submit" value="Generate PHP Code">
    </form>
</body>
</html>
