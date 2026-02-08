# Test script for uploading ZIP file to Marathon agent
# Usage: .\test_upload.ps1

$zipFile = "test_backend.zip"
$url = "http://127.0.0.1:8000/upload/"

# Check if ZIP file exists
if (-Not (Test-Path $zipFile)) {
    Write-Host "Creating test ZIP file..." -ForegroundColor Yellow
    Compress-Archive -Path "test_app.py", "test_requirements.txt" -DestinationPath $zipFile -Force
}

Write-Host "Uploading $zipFile to Marathon agent..." -ForegroundColor Cyan

try {
    # Upload file using multipart/form-data
    $response = Invoke-RestMethod -Uri $url -Method Post -Form @{
        file = Get-Item -Path $zipFile
    }
    
    Write-Host "`n✅ Upload Successful!" -ForegroundColor Green
    Write-Host "`nProject ID: $($response.project_id)" -ForegroundColor Yellow
    Write-Host "`n--- Detection Results ---" -ForegroundColor Magenta
    Write-Host "Language: $($response.detection.language) (Confidence: $($response.detection.confidence))"
    Write-Host "Framework: $($response.detection.framework)"
    Write-Host "Dependencies: $($response.detection.dependencies)"
    
    Write-Host "`n--- Parsing Results ---" -ForegroundColor Magenta
    Write-Host "Files Parsed: $($response.parsing.files_parsed)"
    Write-Host "Functions: $($response.parsing.total_functions)"
    Write-Host "Classes: $($response.parsing.total_classes)"
    Write-Host "Lines of Code: $($response.parsing.total_lines)"
    
    Write-Host "`n--- Embeddings ---" -ForegroundColor Magenta
    Write-Host "Code Chunks: $($response.embeddings.chunks_created)"
    Write-Host "Index Created: $($response.embeddings.index_created)"
    
    Write-Host "`n--- Full Response ---" -ForegroundColor Blue
    $response | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host "`n❌ Upload Failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
