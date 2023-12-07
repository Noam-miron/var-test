output "resource_group_name" {
  value = azurerm_resource_group.resource_group.name
}

output "cosmosdb_account_name" {
  value = azurerm_cosmosdb_account.cosmosdb_account.name
}

output "cosmosdb_sql_database" {
  value = azurerm_cosmosdb_sql_database.cosmosdb_sql_database.name
}

output "cosmosdb_sql_container_restaurants" {
  value = azurerm_cosmosdb_sql_container.restaurants.name
}

output "cosmosdb_sql_container_history" {
  value = azurerm_cosmosdb_sql_container.history.name
}

output "cosmosdb_connection_string" {
  value = azurerm_cosmosdb_account.cosmosdb_account.connection_string
  sensitive = true
}