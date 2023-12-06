terraform {
  backend "azurerm" {
    resource_group_name  = "tf-state-rg"
    storage_account_name = "tfstatevarproj"
    container_name       = "tfstate"
    key                  = "db.tfstate"
  }
}
data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "resource_group" {
  name     = "${random_pet.prefix.id}-rg"
  location = var.resource_group_location
}

resource "azurerm_cosmosdb_account" "cosmosdb_account" {
  name                      = random_pet.prefix.id
  location                  = var.cosmosdb_account_location
  resource_group_name       = azurerm_resource_group.resource_group.name
  offer_type                = "Standard"
  kind                      = "GlobalDocumentDB"
  enable_automatic_failover = false
  enable_free_tier          = true
  geo_location {
    location          = var.resource_group_location
    failover_priority = 0
  }
  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }
  depends_on = [
    azurerm_resource_group.example
  ]
}

resource "azurerm_cosmosdb_sql_database" "cosmosdb_sql_database" {
  name                = "${random_pet.prefix.id}-cosmosdb-sqldb"
  resource_group_name = azurerm_resource_group.resource_group.name
  account_name        = azurerm_cosmosdb_account.cosmosdb_account.name
  throughput          = var.throughput
}

resource "azurerm_cosmosdb_sql_container" "cosmosdb_sql_container" {
  name                  = "${random_pet.prefix.id}-sql-container"
  resource_group_name   = azurerm_resource_group.resource_group.name
  account_name          = azurerm_cosmosdb_account.cosmosdb_account.name
  database_name         = azurerm_cosmosdb_sql_database.cosmosdb_sql_database.name
  partition_key_path    = "/definition/id"
  partition_key_version = 1
  throughput            = var.throughput

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    included_path {
      path = "/included/?"
    }

    excluded_path {
      path = "/excluded/?"
    }
  }

  unique_key {
    paths = ["/definition/idlong", "/definition/idshort"]
  }
}

resource "random_pet" "prefix" {
  prefix = var.prefix
  length = 1
}