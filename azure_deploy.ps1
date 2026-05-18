Write-Host "Checking Azure login status..."
az account show --output none
if ($LASTEXITCODE -ne 0) {
    Write-Host "You need to log in to Azure."
    az login
}
Write-Host "Deploying to Azure App Service..."
az webapp up --name nexshop-ecommerce-app-$((Get-Random -Maximum 9999)) --resource-group nexshop-rg --runtime "PYTHON|3.9" --sku F1 --location eastus
Write-Host "Deployment completed!"

