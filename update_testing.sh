#!/bin/bash

# AI content (ChatGPT, 02/19/2024), verified and adapted by Nicolas Huber.

# Note: This script is a workaround and is used to address an issue where FileNotFoundError occurs

# Issue: FileNotFoundError occurs when running pytest without specifying the test files in the command.
# The reason for this issue is unknown, but it might be related to the pytest version or the pytest configuration.
# This problem might be addressed and solved in the future, but for now, this workaround is necessary.

# Avoid issue: run pytest for a specific test file to avoid FileNotFoundError
# Running pytest without specifying the test files in the command might lead to FileNotFoundError.

# This script is used to update the testing.sh script to include all test files in the tests directory.

CURRENT_DIR=$(pwd)
TEST_DIR="$CURRENT_DIR/tests"
OUTPUT_SCRIPT="$CURRENT_DIR/testing.sh"
rm -f "$OUTPUT_SCRIPT"

echo "#!/bin/bash" >> "$OUTPUT_SCRIPT"
echo "" >> "$OUTPUT_SCRIPT"
echo "# Automatically generated shell script to run all test files with pytest. Check update_testing.sh for further reference" >> "$OUTPUT_SCRIPT"
echo "" >> "$OUTPUT_SCRIPT"

for FILE_PATH in "$TEST_DIR"/*; do
    if [ -f "$FILE_PATH" ]; then
        FILENAME=$(basename "$FILE_PATH")
        if [[ "$FILENAME" == test_*.py ]]; then
            echo "pytest -v \"tests/$(basename "$FILE_PATH")\"" >> "$OUTPUT_SCRIPT"
        fi
    fi
done

chmod +x "$OUTPUT_SCRIPT"
echo "Updated testing.sh script generated."