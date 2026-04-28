provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "devsecops" {
  name     = "rg-${var.project_name}-devsecops-${var.environment}"
  location = var.location
}

# --- Secure Delivery Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "devsecops_k8s" {
  name                = "aks-devsecops-iq-${var.environment}"
  location            = azurerm_resource_group.devsecops.location
  resource_group_name = azurerm_resource_group.devsecops.name
  dns_prefix          = "devsecops-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Governance State Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "governance" {
  name                   = "psql-devsecops-governance-${var.environment}"
  resource_group_name    = azurerm_resource_group.devsecops.name
  location               = azurerm_resource_group.devsecops.location
  version                = "13"
  administrator_login    = "devsecopsadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Multi-Cloud Shared Services (AWS S3 Evidence Sink) ---

resource "aws_s3_bucket" "evidence_sink" {
  bucket = "db-devsecops-evidence-sink-${var.environment}"
}

# --- Global Secrets Management (Azure Key Vault) ---

resource "azurerm_key_vault" "vault" {
  name                        = "kv-devsecops-${var.environment}"
  location                    = azurerm_resource_group.devsecops.location
  resource_group_name         = azurerm_resource_group.devsecops.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}
