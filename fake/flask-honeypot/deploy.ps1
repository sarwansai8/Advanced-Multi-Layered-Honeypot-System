# PowerShell script to deploy Flask honeypot with ngrok
Write-Host "=== Honeypot Deployment Script ===" -ForegroundColor Green

# Download ngrok if it doesn't exist
if (-not (Test-Path "ngrok.exe")) {
    Write-Host "Downloading ngrok..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok.zip"
    
    # Extract ngrok
    Write-Host "Extracting ngrok..." -ForegroundColor Yellow
    Expand-Archive -Path "ngrok.zip" -DestinationPath "." -Force
    
    Write-Host "ngrok downloaded successfully!" -ForegroundColor Green
} else {
    Write-Host "ngrok already exists" -ForegroundColor Green
}

# Configure ngrok with auth token
Write-Host "Configuring ngrok authentication..." -ForegroundColor Yellow
$authToken = "2slA6lKLAgsiY96bp6WKTNStagN_7g4C1mRciLP6hWtBE87bt"
Start-Process -FilePath ".\ngrok.exe" -ArgumentList "config", "add-authtoken", $authToken -NoNewWindow -Wait

# Start ngrok tunnel
Write-Host "Starting ngrok tunnel to expose port 5000..." -ForegroundColor Yellow
Write-Host "Your honeypot will be accessible from the internet!" -ForegroundColor Green
Write-Host "Check the ngrok interface for your public URL." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the tunnel when finished." -ForegroundColor Yellow

# Start ngrok in the foreground
Start-Process -FilePath ".\ngrok.exe" -ArgumentList "http", "5000" -NoNewWindow
