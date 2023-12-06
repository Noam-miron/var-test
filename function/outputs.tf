output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage_account.name
}

output "service_plan_name" {
  value = azurerm_service_plan.service_plan.name
}

output "function_app_name" {
  value = azurerm_windows_function_app.function_app.name
}

output "primary_web_host" {
  value = azurerm_windows_function_app.function_app.default_hostname
}