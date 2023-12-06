output "resource_group_name" {
  value = azurerm_resource_group.resource_group.name
}

output "cosmosdb_account_name" {
  value = azurerm_cosmosdb_account.cosmosdb_account.name
}

output "cosmosdb_sql_database" {
  value = azurerm_cosmosdb_sql_database.cosmosdb_sql_database.name
}

output "cosmosdb_sql_container" {
  value = azurerm_cosmosdb_sql_container.cosmosdb_sql_container.name
}

output "primary_web_host" {
  value = azurerm_windows_function_app.function_app.default_hostname
}