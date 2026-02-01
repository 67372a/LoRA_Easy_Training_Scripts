#!/usr/bin/env bash
set -euo pipefail

# Activate venv
source "../venv/bin/activate"


run_label() {
    local label="$1"
    shift
    local cmd="$*"

    echo "[START] $label: $cmd"
    # line-buffered output, prefix each line
    stdbuf -oL bash -lc "$cmd" 2>&1 \
        | awk -v L="[$label]" '{print L " " $0}'
}

cleanup() {
    echo
    echo "Stopping children..."
    jobs -p | xargs -r kill 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM


# 1) Process watcher (restart main.py on exit)
run_label PROC '
while true; do
    (cd .. && python main.py)
    echo "App closed. Restarting in 1s - press Ctrl+C to stop."
    sleep 1
done
' &

# 2) UI file watcher + compiler (ui_files directory)
run_label COMPILER '
inotifywait -m -e close_write,moved_to,create --format "%f" ../ui_files |
while read -r file; do
    if [[ "$file" =~ \.ui$ ]]; then
        base="${file%.ui}"
        echo "Detected $file - compiling -> $base.py"
        pyside6-uic "../ui_files/$file" -o "../ui_files/$base.py"
    fi
done
' &

# 3) Qt Designer
run_label DESIGN 'pyside6-designer' &

# Keep script alive and responsive to signals
wait
