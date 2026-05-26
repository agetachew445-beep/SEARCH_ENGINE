#!/bin/bash
# Run all tests for IR Search Engine

echo "=== Running IR Search Engine Tests ==="
echo ""

# Activate virtual environment if it exists
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

echo "Running Django tests..."
python manage.py test

echo ""
echo "=== Test Summary ==="
echo "Check output above for results"
echo ""
