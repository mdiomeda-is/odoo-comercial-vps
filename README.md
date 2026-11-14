# Odoo 19 Comercial en VPS nuevo — Coolify + Cloudflare (Intellia Solution)

Instalación **desde cero** en un VPS limpio, pensada para crecer (Odoo + n8n + más).

**Arquitectura:** Cloudflare Free (edge) → VPS → **Coolify** (Traefik + SSL) → **Odoo 19** +
PostgreSQL 16. Facturación electrónica AFIP/ARCA con los módulos ADHOC de 19 (`l10n_ar_fiscal_ws`).

> ⚠️ **Odoo 19 está en modo validación.** El objetivo es probar que AFIP 19 funciona
> (homologación). Si pasa, queda en 19; si no, el mismo esquema sirve para 18 (cambiás la
> versión en el Dockerfile y el módulo a `l10n_ar_afipws_fe`).

## Pasos

1. **Preparar el VPS + instalar Coolify** (como root):
   ```bash
   sudo bash scripts/01-setup-vps.sh
   ```
   Entrá a `http://<IP>:8000`, creá el admin de Coolify y activá 2FA.

2. **Desplegar Odoo** siguiendo **[COOLIFY-ODOO.md](COOLIFY-ODOO.md)**
   (subir a Git → recurso Compose en Coolify → variables → dominio/SSL → deploy →
   crear base + módulos por terminal → preconfigurar).

3. **Cloudflare** adelante: **[CLOUDFLARE.md](CLOUDFLARE.md)**
   (SSL Full strict, bloquear `/web/database`, Rocket Loader off, no cachear `/web`, SPF/DKIM).

4. **Config fiscal**: **[CONFIG-AFIP.md](CONFIG-AFIP.md)** (certificado + punto de venta,
   probar en homologación) y **[CONFIG-ARGENTINA.md](CONFIG-ARGENTINA.md)** (IVA, diarios, multiempresa).

5. **n8n** a futuro: desde el panel de Coolify (template de un clic), mismo Traefik/SSL.

## Archivos
| Archivo | Qué es |
|---|---|
| `scripts/01-setup-vps.sh` | Firewall + swap + instala Coolify |
| `Dockerfile` | Odoo 19 + clona módulos ADHOC 19.0 + config + preconfigure |
| `docker-compose.yml` | db (Postgres 16) + odoo, para Coolify |
| `config/odoo.conf` | Config base (proxy_mode, list_db=False, workers=0, addons AFIP) |
| `scripts/preconfigure.py` | Empresa + admin + idioma es_AR robusto (XML-RPC) |
| `COOLIFY-ODOO.md` | Deploy paso a paso en Coolify |
| `CLOUDFLARE.md` | Edge con Cloudflare Free |
| `CONFIG-AFIP.md` / `CONFIG-ARGENTINA.md` | Facturación electrónica y fiscal AR |

## Diferencias vs. el otro server (EasyPanel)
- Acá el proxy/SSL lo da **Coolify** (no EasyPanel), sin límite de apps.
- Odoo **19** (no 18) con el módulo AFIP nuevo (`l10n_ar_fiscal_ws`), **sin** la imagen custom
  de librerías Python que hizo falta en 18.
- `workers=0` para rutear un solo puerto (8069) por simplicidad en Coolify.
