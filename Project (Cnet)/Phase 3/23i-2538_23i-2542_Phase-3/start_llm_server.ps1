# Starts the local llama.cpp server on the CPU (Phase 2 Step 5 settings).
# Uses ~2.5-3 GB RAM. Close Discord/extra browser tabs first if free RAM < 4 GB.
# Stop it with Ctrl+C in this window.
$root = $PSScriptRoot
& "$root\external\llamacpp\bin\llama-server.exe" `
    -m "$root\external\models\Llama-3.2-3B-Instruct-Q4_K_M.gguf" `
    --host 127.0.0.1 --port 8080 `
    -c 2048 -n 128 -t 6 --parallel 1 --no-webui
