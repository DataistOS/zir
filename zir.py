#!/usr/bin/env bash

# Define the diacritics pattern and excluded directories
PATTERN='[\u0650\u064D]'
EXCLUDES="{_build,build,logs,venv,.venv,.git}"

# Use the provided argument as the target path, or default to current directory (.)
TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
  echo -e "\033[1;31m❌ Error: Directory '$TARGET_DIR' does not exist.\033[0m"
  exit 1
fi

echo -e "\033[1;34m🔍 Scanning '$TARGET_DIR' for unwanted Persian diacritics...\033[0m"
echo "--------------------------------------------------"

# Find files and format the output cleanly with counts
found=0
while IFS= read -r file; do
  if [ -n "$file" ]; then
    count=$(grep -cE "$(printf "$PATTERN")" "$file")
    printf "\033[31m[Found]\033[0m %-40s \033[32m(%s matches)\033[0m\n" "$file" "$count"
    found=1
  fi
done < <(grep -rIE "$(printf "$PATTERN")" "$TARGET_DIR" --exclude-dir=$EXCLUDES --files-with-matches)

echo "--------------------------------------------------"
if [ $found -eq 0 ]; then
  echo -e "\033[1;32m✨ Clean! No unwanted diacritics found.\033[0m"
else
  echo -e "\033[1;33m⚠️ Scan completed. Please review the files above.\033[0m"
fi

