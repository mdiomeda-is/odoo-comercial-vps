#!/usr/bin/env bash
# ============================================================================
#  01 · Prepara un VPS NUEVO (Ubuntu 22.04/24.04) e instala Coolify.
#  Ejecutar como root:  sudo bash scripts/01-setup-vps.sh
#  (Coolify instala Docker por su cuenta; acá además dejamos firewall + swap.)
# ============================================================================
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
echo ">> Actualizando paquetes base..."
apt-get update -y
apt-get install -y ca-certificates curl ufw

# ---------- Firewall ----------
echo ">> Firewall: SSH, HTTP, HTTPS y panel de Coolify (8000)..."
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp      # panel de Coolify (cerralo después de poner dominio+SSL al panel)
ufw --force enable

# ---------- Swap (útil en VPS con poca RAM) ----------
if ! swapon --show | grep -q '/swapfile'; then
  echo ">> Creando swap de 2G..."
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# ---------- Coolify ----------
echo ">> Instalando Coolify (instala Docker si falta)..."
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

echo ""
echo "============================================================"
echo "  Coolify instalado."
echo "  Entrá al panel:  http://<IP-del-VPS>:8000"
echo "  Creá el usuario admin y activá 2FA."
echo "  Después seguí:  COOLIFY-ODOO.md"
echo "============================================================"
