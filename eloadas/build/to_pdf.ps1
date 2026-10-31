# A pptx -> PDF átalakítás a telepített PowerPointtal (vizuális ellenőrzéshez).
param([string]$InPath, [string]$OutPath)
$app = New-Object -ComObject PowerPoint.Application
try {
    $deck = $app.Presentations.Open((Resolve-Path $InPath).Path, $true, $false, $false)
    $deck.SaveAs([System.IO.Path]::GetFullPath($OutPath), 32)
    $deck.Close()
} finally { $app.Quit() }
Write-Output "pdf written: $OutPath"
