#!/bin/bash

# Log into Azure
az login

# Show current subscription (use 'az account set' to change subscription)
az account show

# Variables
subscriptionId=$(az account show --query id -o tsv)
appName="GitHub-var-test-Actions-OIDC"
RBACRole="Contributor"

githubOrgName="Noam-miron"
githubRepoName="var-test"
githubBranch="main"

# Create AAD App and Principal
appId=$(az ad app create --display-name $appName --query appId -o tsv)
az ad sp create --id $appId

# Create federated GitHub credentials (Entity type 'Branch')
githubBranchConfig='{
    "name": "GH-['"$githubOrgName-$githubRepoName"']-Branch-['"$githubBranch"']",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'"$githubOrgName/$githubRepoName"':ref:refs/heads/'"$githubBranch"'",
    "description": "Federated credential linked to GitHub ['"$githubBranch"'] branch @: ['"$githubOrgName/$githubRepoName"']",
    "audiences": ["api://AzureADTokenExchange"]
}'
echo $githubBranchConfig | az ad app federated-credential create --id $appId --parameters "@-"

# Create federated GitHub credentials (Entity type 'Pull Request')
githubPRConfig='{
    "name": "GH-['"$githubOrgName-$githubRepoName"']-PR",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'"$githubOrgName/$githubRepoName"':pull_request",
    "description": "Federated credential linked to GitHub Pull Requests @: ['"$githubOrgName/$githubRepoName"']",
    "audiences": ["api://AzureADTokenExchange"]
}'
echo $githubPRConfig | az ad app federated-credential create --id $appId --parameters "@-"

# Assign RBAC permissions to Service Principal (Change as necessary)
echo "$appId" | while read -r line
do
    # Permission 1 (Example)
    az role assignment create \
        --role $RBACRole \
        --scope /subscriptions/efc72010-7c33-47d9-962b-6fd3849197df \
        --assignee $line \
        --subscription $subscriptionId

    # Permission 2 (Example)
    # az role assignment create \
    #    --role "Reader and Data Access" \
    #    --assignee "$line" \
    #    --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Storage/storageAccounts/$storageName"
done
