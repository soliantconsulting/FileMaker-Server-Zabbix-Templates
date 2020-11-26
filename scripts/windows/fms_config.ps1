#######################################################################
#    fms_config.ps1
#
#    Powershell script used for calling the FMS Admin API.
#    For Windows
#    
#
#    Wim Decorte <wdecorte@soliantconsulting.com>
#    version 1.0.0 - 20190517_1239 
#
#    Released under the GNU General Public License WITHOUT ANY WARRANTY.
#
#######################################################################


# special config to skip ssl validation since we will be using 'localhost'
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# parse the command line arguments
$u = $args[0]
$p = $args[1]
$fms_version = $args[2]
# $fms_version = 18 # $args[2]

if($fms_version -eq "17")
{
    $URI = "https://localhost/fmi/admin/api/v1/user/login"

    $account = @{
        username = $u
        password = $p ;
      }

    $body = $account | ConvertTo-Json

    $response = Invoke-RestMethod -Uri $URI -Method POST -body $body -ContentType "application/json"
    $token = $response.token
}
else
{
    # this applies to 18 and up
    # username:password pair
    $credPair = $u + ":" + $p
    # Write-Host $credPair
    # $credPair = "$($username):$($password)"
    # base64 encode it
    $encodedCredentials = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($credPair))
    # Write-Host $encodedCredentials
    # and add it to the header
    $headers = @{ Authorization = "Basic $encodedCredentials" }

    $URI = "https://localhost/fmi/admin/api/v2/user/auth"
    $response = Invoke-RestMethod -Uri $URI -Method POST -Headers $headers
    $token = $response.response.token
}


$headers2 = @{ Authorization = "Bearer $token"  }
$URI2 = "https://localhost:16000/fmi/admin/internal/v1/server/config"
$config = Invoke-RestMethod -Uri $URI2 -Method GET -Headers $headers2 

# log out to free up an admin console session
if($fms_version -eq "17")
{
    $URI3 = "https://localhost/fmi/admin/api/v1/user/logout"
    $logout = Invoke-RestMethod -Uri $URI3 -Method POST -Headers $headers2 -ContentType "application/json"
}
else
{
    # 18 and up
    $URI3 = "https://localhost/fmi/admin/api/v2/user/auth/" + $token
    $logout = Invoke-RestMethod -Uri $URI3 -Method DELETE -Headers $headers2
}

# write the output as pure json to be parsed by zabbix dependent items
Write-Output $config | ConvertTo-Json
