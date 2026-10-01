$ErrorActionPreference = 'Stop'
$dest = Join-Path $PSScriptRoot 'raw.json'
if (Test-Path -LiteralPath $dest) { throw 'Retained capture exists; refuse overwrite' }
$started = [DateTimeOffset]::UtcNow.ToString('o')
function Hash-Text([string]$value) {
    $bytes = [Text.Encoding]::UTF8.GetBytes($value)
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}
function Steam-State {
    $active = Get-ItemProperty -LiteralPath 'HKCU:\Software\Valve\Steam\ActiveProcess'
    $client = Get-ItemProperty -LiteralPath 'HKCU:\Software\Valve\Steam'
    $steam = Get-Process -Id $active.pid
    if ($steam.ProcessName -ne 'steam') { throw 'ActiveProcess PID is not Steam' }
    $expected = [IO.Path]::GetFullPath((Join-Path $client.SteamPath 'steam.exe'))
    if ([IO.Path]::GetFullPath($steam.Path) -ine $expected) { throw 'Steam process/path mismatch' }
    if ([uint32]$active.ActiveUser -eq 0 -or -not $client.AutoLoginUser) { throw 'No nonempty Steam profile identity control' }
    [ordered]@{
        pid = [int]$active.pid
        started_utc = $steam.StartTime.ToUniversalTime().ToString('o')
        active_user_low32 = [uint32]$active.ActiveUser
        auto_login_name_casefold_sha256 = Hash-Text $client.AutoLoginUser.ToLowerInvariant()
        path = $expected
        executable_sha256 = (Get-FileHash -LiteralPath $expected -Algorithm SHA256).Hash.ToLowerInvariant()
        file_version = $steam.FileVersion
    }
}
function File-Observation([string]$path) {
    $f = Get-Item -LiteralPath $path
    if ($f.PSIsContainer -or ($f.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Expected regular file' }
    $bytes = [IO.File]::ReadAllBytes($f.FullName)
    $ascii = [Text.Encoding]::ASCII.GetString($bytes)
    [ordered]@{
        path = $f.FullName
        bytes = $bytes.Length
        sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
        created_utc = $f.CreationTimeUtc.ToString('o')
        modified_utc = $f.LastWriteTimeUtc.ToString('o')
        attributes = $f.Attributes.ToString()
        keyboard1_header = $ascii.Contains('[Keyboard1]')
        circle_assignment = [regex]::IsMatch($ascii,'(?m)^Circle=')
    }
}
function Select-Profile([string]$vdf, [uint32]$activeLow32, [string]$accountHash) {
    $matches = [regex]::Matches($vdf,'(?ms)^\s*"(?<id>[0-9]{17})"\s*\r?\n\s*\{(?<body>.*?)^\s*\}')
    if ($matches.Count -eq 0) { throw 'No account records: no verdict' }
    $records = @(foreach ($match in $matches) {
        $names = [regex]::Matches($match.Groups['body'].Value,'(?m)^\s*"AccountName"\s*"(?<v>[^"\r\n]+)"\s*$')
        if ($names.Count -ne 1) { throw 'Missing/ambiguous AccountName: no verdict' }
        [ordered]@{
            steam_id64 = $match.Groups['id'].Value
            account_name_casefold_sha256 = Hash-Text $names[0].Groups['v'].Value.ToLowerInvariant()
        }
    })
    $selected = @($records | Where-Object {
        [uint32]([uint64]::Parse($_.steam_id64) -band [uint64]4294967295) -eq $activeLow32 -and
        $_.account_name_casefold_sha256 -ceq $accountHash
    })
    if ($selected.Count -ne 1) { throw 'Active profile selection not unique: no verdict' }
    [ordered]@{record_count=$matches.Count;selected=$selected[0]}
}
$before = Steam-State
$steamDir = Split-Path -Parent $before.path
$vdfPath = Join-Path $steamDir 'config/loginusers.vdf'
$vdfBytes = [IO.File]::ReadAllBytes($vdfPath)
$vdf = [Text.Encoding]::UTF8.GetString($vdfBytes)
# Bounded extraction of Steam's flat per-account records, not a generic VDF parser.
# Full-line delimiters avoid treating a brace inside an ordinary quoted name as a record end.
$profileData = Select-Profile $vdf $before.active_user_low32 $before.auto_login_name_casefold_sha256
$profile = $profileData.selected
$low = [uint32]([uint64]::Parse($profile.steam_id64) -band [uint64]4294967295)
if ($low -ne $before.active_user_low32 -or $profile.account_name_casefold_sha256 -cne $before.auto_login_name_casefold_sha256) { throw 'Independent Steam profile controls disagree' }
$root = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'My Games/FINAL FANTASY XII THE ZODIAC AGE'
$accountDir = Join-Path $root $profile.steam_id64
$paths = @((Join-Path $root 'keymap.ini'), (Join-Path $accountDir 'keymap.ini'))
$filesBefore = @($paths | ForEach-Object { File-Observation $_ })
$rootDirectories = @(Get-ChildItem -LiteralPath $root -Directory | ForEach-Object { [ordered]@{name=$_.Name;attributes=$_.Attributes.ToString()} })
$filesAfter = @($paths | ForEach-Object { File-Observation $_ })
$after = Steam-State
$vdfAfter = (Get-FileHash -LiteralPath $vdfPath -Algorithm SHA256).Hash.ToLowerInvariant()
$vdfHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($vdfBytes)).ToLowerInvariant()
if (($before | ConvertTo-Json -Compress) -cne ($after | ConvertTo-Json -Compress)) { throw 'Steam identity changed during observation' }
if (($filesBefore | ConvertTo-Json -Compress) -cne ($filesAfter | ConvertTo-Json -Compress)) { throw 'Keymap files changed during observation' }
if ($vdfHash -cne $vdfAfter) { throw 'Profile file changed during observation' }
if (@(Get-Process -Name FFXII_TZA -ErrorAction SilentlyContinue).Count -ne 0) { throw 'Unexpected running game; observation scope no longer matches' }
$receipt = [ordered]@{
    status = 'HOST_ARTIFACT_OBSERVED_NO_FF12_PROCESS'
    method = 'A: retained/filesystem artifacts with current host profile metadata; not live FF12'
    started_utc = $started
    ended_utc = [DateTimeOffset]::UtcNow.ToString('o')
    powershell_version = $PSVersionTable.PSVersion.ToString()
    capture_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    steam_before = $before
    steam_after = $after
    profile_file = [ordered]@{path=$vdfPath;sha256=$vdfHash;after_sha256=$vdfAfter;record_count=$profileData.record_count;selected=$profile}
    documents_root = $root
    directory_entries = $rootDirectories
    files_before = $filesBefore
    files_after = $filesAfter
    ff12_process_count = 0
    changes = @()
    limitations = @('No FF12 process/API call, path creation or formatter observed.','Steam host metadata is bracketed, not an atomic API account snapshot.','File timestamps do not identify their creator; files predate this observation.','Other profile/account records and unrelated files were not copied.','No inference of safe returned-stack-pointer lifetime or cause of an empty directory component.')
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $dest -Encoding utf8NoBOM
Write-Output ('OBSERVED: two existing keymaps; stable Steam profile controls; game absent. Account directory matches selected profile: ' + ((Split-Path -Leaf $accountDir) -ceq $profile.steam_id64))
