#!/bin/bash

# ALPHA GUARD IT // ENGINEERING LOG PROTOCOL
JOURNAL="ENGINEERING_LOG.md"

# Setup the log file if it's missing
if [ ! -f "$JOURNAL" ]; then
    echo "# ALPHA GUARD IT // ENGINEERING LOG" > "$JOURNAL"
    echo "Proprietor: AlphaGuard IT" >> "$JOURNAL"
    echo "--------------------------------" >> "$JOURNAL"
fi

# Append the Session Header
echo -e "\n## SESSION: $(date '+%Y-%m-%d %H:%M')" >> "$JOURNAL"
echo "Fuel: Black Coffee & Nicotine" >> "$JOURNAL"
echo "--------------------------------" >> "$JOURNAL"

# Open nano and jump to the bottom for the entry
nano +999999 "$JOURNAL"

echo "[SYSTEM] Entry stored. Run ./ghost-sync.sh to secure to cloud."
