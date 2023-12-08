terraform {
  backend "azurerm" {
    resource_group_name  = "tf-state-rg"
    storage_account_name = "tfstatevarproj"
    container_name       = "tfstate"
    key                  = "function.tfstate"
    use_oidc             = true
  }
}
data "azurerm_client_config" "current" {}

# Generate random resource group name
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = random_pet.rg_name.id
}

# Generate random value for the storage account name
resource "random_string" "storage_account_name" {
  length  = 8
  lower   = true
  numeric = false
  special = false
  upper   = false
}

resource "azurerm_storage_account" "storage_account" {
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  name = random_string.storage_account_name.result

  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
  name                = "varonis-app-service-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "varonis-linux-function-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id

  app_settings = {
  #  # "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  #   #TODO: zip deploy function
  }

  site_config {
    # always_on = true
    # cors {
    #   allowed_origins = ["*"]
    # }
  }
}