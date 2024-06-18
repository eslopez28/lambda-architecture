$dummyFiles = @(
    [PSCustomObject]@{Path="/usr/document/folderwithSLA1"; FullPath="/usr/document/folderwithSLA1/exampleFile1.txt"; Name="exampleFile1.txt"; CreationTime=(Get-Date).AddMinutes(-30)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA1"; FullPath="/usr/document/folderwithSLA1/exampleFile2.txt"; Name="exampleFile2.txt"; CreationTime=(Get-Date).AddMinutes(-10)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA1"; FullPath="/usr/document/folderwithSLA1/exampleFile3.txt"; Name="exampleFile3.txt"; CreationTime=(Get-Date).AddMinutes(-40)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA2"; FullPath="/usr/document/folderwithSLA2/exampleFile4.txt"; Name="exampleFile4.txt"; CreationTime=(Get-Date).AddMinutes(-5)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA2"; FullPath="/usr/document/folderwithSLA2/exampleFile5.txt"; Name="exampleFile5.txt"; CreationTime=(Get-Date).AddMinutes(-30)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA2"; FullPath="/usr/document/folderwithSLA2/exampleFile6.txt"; Name="exampleFile6.txt"; CreationTime=(Get-Date).AddMinutes(-70)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA2"; FullPath="/usr/document/folderwithSLA2/exampleFile7.txt"; Name="exampleFile7.txt"; CreationTime=(Get-Date).AddMinutes(-150)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA3"; FullPath="/usr/document/folderwithSLA3/exampleFile8.txt"; Name="exampleFile8.txt"; CreationTime=(Get-Date).AddMinutes(-100)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA3"; FullPath="/usr/document/folderwithSLA3/exampleFile9.txt"; Name="exampleFile9.txt"; CreationTime=(Get-Date).AddMinutes(-20)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA3"; FullPath="/usr/document/folderwithSLA3/exampleFile10.txt"; Name="exampleFile10.txt"; CreationTime=(Get-Date).AddMinutes(-30)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA3"; FullPath="/usr/document/folderwithSLA3/exampleFile11.txt"; Name="exampleFile11.txt"; CreationTime=(Get-Date).AddMinutes(-95)},
    [PSCustomObject]@{Path="/usr/document/folderwithSLA3"; FullPath="/usr/document/folderwithSLA3/exampleFile12.txt"; Name="exampleFile12.txt"; CreationTime=(Get-Date).AddMinutes(-80)}
)


# Configuración de los directorios y sus SLAs en minutos
$foldersSLA = @{
    "/usr/document/folderwithSLA1" = 20
    "/usr/document/folderwithSLA2" = 60
    "/usr/document/folderwithSLA3" = 90 # 24 horas
}

# Endpoint de prueba
$endpoint = "https://reqres.in/api/errorFolder"

# Obtener la hora actual
$currentDateTime = Get-Date

# Lista para almacenar errores de SLA
$slaErrors = @()
$slaFiles = @()

# Función para convertir fecha a formato ISO 8601
function ConvertDate ($date) {
    return $date.ToString("yyyy-MM-ddTHH:mm:ss")
}

# Iterar a través de cada carpeta y su SLA correspondiente
foreach ($folder in $foldersSLA.Keys) {
    $slaFiles = @()
    $slaMinutes = $foldersSLA[$folder]
    #$files = Get-ChildItem -Path $folder -File
    $files = $dummyFiles | Where-Object { $_.Path -eq $folder }
    foreach ($file in $files) {
        $fileAge = $currentDateTime - $file.CreationTime
        if ($fileAge.TotalMinutes -gt $slaMinutes) {
            $slaFiles += [PSCustomObject]@{
                filename = $file.Name
                creationDate = ConvertDate $file.CreationTime
            }
        }
    }
    if($slaFiles.Count -gt 0) {
        $slaErrors += [PSCustomObject]@{
            folder = $folder
            sla = $slaMinutes
            files = $slaFiles
        }
    }
}

# Verificar si hay errores de SLA para enviar
if ($slaErrors.Count -gt 0) {
    # Crear el objeto JSON para enviar
    $jsonBody = @{
        sla_error = $slaErrors
    } | ConvertTo-Json -Depth 5

    Write-Output $jsonBody

    # Enviar el objeto JSON al endpoint REST
    try {
        $response = Invoke-RestMethod -Uri $endpoint -Method Post -ContentType "application/json" -Body $jsonBody
        Write-Output "Response: $($response | ConvertTo-Json)"
    } catch {
        Write-Error "Failed to send data: $_"
    }
} else {
    Write-Output "No SLA violations found."
}
