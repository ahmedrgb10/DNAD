function GetUrl {
    param (
        [string]$orgUrl,
        [hashtable]$header,
        [string]$areaID
    )
    
    $orgResourceAreasUrl = [string]::Format("{0}/_apis/resourceAreas/{1}?api-preview=5.0-preview.1", $orgUrl , $areaID)

    $results = Invoke-RestMethod -Uri $orgResourceAreasUrl -Headers $header

    if ("null" -eq $results){
        $areaUrl = $orgUrl
    }
    else {
        $areaUrl = $results
    }

    return $areaUrl
}


$orgUrl = "https://tfsapp.egyptianbanks.net/tfs/DefaultCollection"
$personalToken ="q324tbxlrrrrk7braf6qgqa4v6rw72viyjmkhlmvxxu3hctry53q"

Write-Host "Initialize authentication context" -ForegroundColor Yellow
$token = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($personalToken)"))
$header = @{authorization = "Basic $token"}

Write-Host "List my work items" -ForegroundColor DarkBlue
$workAreaId = "1d4f49f9-02b9-4e26-b826-2cdb6195f2a9"
$tfsBaseUrl = GetUrl -orgUrl $orgUrl -header $header -areaId $workAreaId

Write-Host "$($tfsBaseUrl)" -ForegroundColor Cyan

$workItemId = 229626#231618
$wisUrl = "$($tfsBaseUrl)/CPES/_apis/wit/workitems/$($workItemId)?"+"$"+"expand=all" 

Write-Host "$($wisUrl)" -ForegroundColor DarkMagenta


$workItem = Invoke-RestMethod -Uri $wisUrl -Method Get -Headers $header -ContentType "application/json"

#Write-Host "$($workItem.fields)" -ForegroundColor Black -BackgroundColor Gray

$workItem.fields | Out-File D:\Backyard\Automation\outputs\"$($workItemId)".txt
$workItem.relations | Set-Content D:\Backyard\Automation\outputs\"$($workItemId)-relations".txt


#Get changesets
$changesets = $workItem.relations #| Where-Object {$_.rel -eq 'ArtifactLink' -and $_.attributes.name -eq "Fixed in Changeset"}
Write-Host "$($changesets)" -ForegroundColor Gray

for each