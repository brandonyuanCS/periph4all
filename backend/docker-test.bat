@echo off
REM Script to test Docker build locally (simulating Hugging Face Spaces)

echo Building Docker image...
docker build -t periph4all-api:test .

echo.
echo Starting container...
echo API will be available at http://localhost:7860
echo Press Ctrl+C to stop
echo.

REM Run container with port mapping
docker run -p 7860:7860 ^
  -e PORT=7860 ^
  -e GROQ_API_KEY=%GROQ_API_KEY% ^
  -e ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000 ^
  periph4all-api:test

