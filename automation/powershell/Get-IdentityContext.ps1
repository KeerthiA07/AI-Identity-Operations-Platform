param(
    [Parameter(Mandatory=$true)]
    [string]$UserPrincipalName
)

# Read-only Microsoft Graph PowerShell workflow.
# Install once if required:
# Install-Module Microsoft.Graph -Scope CurrentUser

Connect-MgGraph -Scopes "User.Read.All","GroupMember.Read.All","AppRoleAssignment.Read.All","RoleManagement.Read.Directory"

$user = Get-MgUser -UserId $UserPrincipalName -Property Id,DisplayName,UserPrincipalName,Department,JobTitle,AccountEnabled

$groups = Get-MgUserMemberOf -UserId $user.Id -All |
    Where-Object { $_.AdditionalProperties.'@odata.type' -eq '#microsoft.graph.group' } |
    ForEach-Object { $_.AdditionalProperties.displayName }

$appAssignments = Get-MgUserAppRoleAssignment -UserId $user.Id -All |
    ForEach-Object { $_.AdditionalProperties.resourceDisplayName }

[PSCustomObject]@{
    Id                = $user.Id
    DisplayName       = $user.DisplayName
    UserPrincipalName = $user.UserPrincipalName
    Department        = $user.Department
    JobTitle          = $user.JobTitle
    AccountEnabled    = $user.AccountEnabled
    Groups            = @($groups)
    Applications      = @($appAssignments)
} | ConvertTo-Json -Depth 5
