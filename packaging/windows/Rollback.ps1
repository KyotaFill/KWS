[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$VersionDirectory,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-fA-F]{64}$')][string]$ExpectedHelperSha256,
    [string]$ExpectedSigner,
    [switch]$AllowUnsigned
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$directory = (Resolve-Path -LiteralPath $VersionDirectory).Path
if (Get-Process -Name KWS -ErrorAction SilentlyContinue) { throw 'Close KWS normally before changing app version' }
$helper = Join-Path $directory 'KWSHelper.exe'
$data = if ($env:KWS_LOCAL_DATA_DIR) { $env:KWS_LOCAL_DATA_DIR } else { Join-Path $env:LOCALAPPDATA 'kws-lan' }
if ((Get-FileHash -LiteralPath $helper -Algorithm SHA256).Hash -ne $ExpectedHelperSha256) { throw 'Helper hash mismatch' }
$signature = Get-AuthenticodeSignature -LiteralPath $helper
if ($ExpectedSigner) {
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Thumbprint -ne $ExpectedSigner) { throw 'Helper signer mismatch' }
} elseif (!$AllowUnsigned -or $signature.Status -ne 'NotSigned') { throw 'Specify expected signer or explicitly permit unsigned test build' }
# Verify this release and compatibility with the existing cache; never restore a stale cache backup.
& $helper --self-test
if ($LASTEXITCODE -ne 0) { throw 'Release verification failed' }
& $helper --check-cache $data
if ($LASTEXITCODE -ne 0) { throw 'Selected version cannot open current cache. Keep newer app and all data.' }
$shell = New-Object -ComObject WScript.Shell
foreach ($folder in @([Environment]::GetFolderPath('Programs'), [Environment]::GetFolderPath('Desktop'))) {
    $link = $shell.CreateShortcut((Join-Path $folder 'KWS Desktop.lnk'))
    $link.TargetPath = Join-Path $directory 'KWS.exe'
    $link.WorkingDirectory = $directory
    $link.Save()
}
Write-Host 'Shortcut changed. No cache/device/command/receipt was restored, deleted or downgraded.'
