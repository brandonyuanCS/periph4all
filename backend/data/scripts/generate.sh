#!/bin/bash

echo "========================================"
echo "Generating Mouse Embeddings"
echo "========================================"
echo

python generate_embeddings.py "$@"

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Embedding generation failed!"
    exit 1
fi

echo
echo "========================================"
echo "Success! Running tests..."
echo "========================================"
echo

python test_embeddings.py

if [ $? -ne 0 ]; then
    echo
    echo "WARNING: Tests failed!"
    exit 1
fi

echo
echo "========================================"
echo "All done! Embeddings are ready to use."
echo "========================================"

