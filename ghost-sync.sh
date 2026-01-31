#!/bin/bash
echo " Shadow-Sync: Pushing Wraith-Core to the cloud..."
git add .
echo "Enter mission update:"
read commit_msg
git commit -m "Wraith-Core: $commit_msg"
git push origin main
echo " Sync Complete."
