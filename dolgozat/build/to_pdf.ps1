# A docx -> PDF átalakítás a telepített Worddel (a tartalomjegyzéket előbb frissíti).
# Használat: powershell -ExecutionPolicy Bypass -File dolgozat/build/to_pdf.ps1 <be.docx> <ki.pdf>
param([string]$InPath, [string]$OutPath)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open((Resolve-Path $InPath).Path, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    $doc.SaveAs2([System.IO.Path]::GetFullPath($OutPath), 17)
    $doc.Close($false)
} finally {
    $word.Quit()
}
Write-Output "pdf written: $OutPath"
