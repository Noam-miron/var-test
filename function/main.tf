terraform {
  backend "azurerm" {
    resource_group_name  = "tf-state-rg"
    storage_account_name = "tfstatevarproj"
    container_name       = "tfstate"
    key                  = "function.tfstate"
    use_oidc             = true
  }
}

resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = random_pet.rg_name.id
}

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
  name                = "${var.project}-app-service-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_application_insights" "application_insight" {
  name                = "${azurerm_linux_function_app.function_app.name}-appinsight"
  resource_group_name = azurerm_resource_group.resource_group.name
  location            = azurerm_resource_group.rg.location
  application_type    = "other"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "${var.project}-linux-function-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id

  https_only                  = true
  functions_extension_version = "~4"
  app_settings = {
    "ENABLE_ORYX_BUILD"              = "true"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "AzureWebJobsFeatureFlags"       = "EnableWorkerIndexing"
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.application_insight.instrumentation_key
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  zip_deploy_file = data.archive_file.function.output_path
}

#   app_settings = {
#    "WEBSITE_RUN_FROM_PACKAGE" = "1"
#     # "FUNCTIONS_WORKER_RUNTIME" = "python"
#   #   #TODO: zip deploy function
#   }

#   site_config {
#     ### always_on = true
#     # cors {
#     #   allowed_origins = ["*"]
#     # }
#   }
# }