@echo off
echo ========================================
echo Generating Mouse Embeddings
echo ========================================
echo.

python generate_embeddings.py %*

if errorlevel 1 (
    echo.
    echo ERROR: Embedding generation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Success! Running tests...
echo ========================================
echo.

python test_embeddings.py

if errorlevel 1 (
    echo.
    echo WARNING: Tests failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo All done! Embeddings are ready to use.
echo ========================================
pause

