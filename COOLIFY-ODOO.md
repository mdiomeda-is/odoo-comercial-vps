# Desplegar Odoo 19 en Coolify (paso a paso)

Pre: VPS preparado con `scripts/01-setup-vps.sh` (Coolify instalado), y un **repo Git**
con esta carpeta (Coolify construye la imagen desde el Dockerfile). DNS del dominio
apuntando a la IP del VPS.

## 1) Subir este proyecto a un repo Git
Coolify construye a partir de un repositorio (GitHub/GitLab):
```bash
cd odoo-comercial-vps
git init && git add . && git commit -m "Odoo 19 comercial VPS"
# crear el repo (privado) y pushear
gh repo create intellia/odoo-comercial-vps --private --source=. --push
```

## 2) Crear el recurso en Coolify
1. Panel de Coolify → **New → Project** (ej. "Odoo Comercial").
2. Dentro del proyecto → **New Resource → Docker Compose** → **desde Git**.
3. Conectá el repo y elegí la rama. Coolify detecta el `docker-compose.yml` y el `Dockerfile`.

## 3) Variables de entorno (en el recurso)
Cargá estas (pestaña **Environment Variables**). Generá las claves con `openssl rand -base64 24`:
```
POSTGRES_USER=odoo
POSTGRES_PASSWORD=<clave fuerte>
ODOO_DB_NAME=comercial
ODOO_ADMIN_LOGIN=admin@tudominio.com
ODOO_ADMIN_PASSWORD=<clave fuerte>
ODOO_INIT_MODULES=base,contacts,crm,sale_management,account,l10n_ar,purchase,stock,project,l10n_ar_fiscal_ws
COMPANY_NAME=Tu Empresa S.A.
COMPANY_VAT=30-12345678-9
COMPANY_STREET=Calle 123
COMPANY_CITY=Buenos Aires
COMPANY_ZIP=1000
COMPANY_STATE=Buenos Aires
COMPANY_COUNTRY_CODE=AR
COMPANY_PHONE=+54 11 4000-0000
COMPANY_EMAIL=info@tuempresa.com
COMPANY_WEBSITE=https://tuempresa.com
COMPANY_CURRENCY=ARS
COMPANY_LANG=es_AR
COMPANY_TZ=America/Argentina/Buenos_Aires
```

## 4) Dominio + SSL
En el servicio **odoo**, campo **Domains**: poné `https://odoo.tudominio.com` y puerto **8069**.
Coolify emite el certificado (Let's Encrypt) automáticamente.

> Si vas a usar Cloudflare adelante, primero dejá el DNS en **"DNS only" (nube gris)** para que
> salga el certificado; después pasalo a **Proxied** con SSL **Full (strict)**. Ver CLOUDFLARE.md.

## 5) Deploy
Clic en **Deploy**. Coolify construye la imagen (clona los módulos ADHOC 19.0) y levanta
**db + odoo**. Odoo arranca pero la base `comercial` todavía no existe (paso 6).

## 6) Crear la base e instalar módulos (terminal de Coolify)
Abrí la **Terminal** del contenedor `odoo` en Coolify y corré:
```bash
/entrypoint.sh odoo -d "$ODOO_DB_NAME" -i "$ODOO_INIT_MODULES" \
  --without-demo=all --stop-after-init --no-http
```
Mirá que termine con **`Modules loaded.`** sin `CRITICAL`.
**→ Acá se valida si AFIP 19 (`l10n_ar_fiscal_ws`) instala bien.** Si falta alguna lib Python,
el error lo dice; se agrega el `pip install` al Dockerfile y re-deploy.

Luego, en Coolify, **Restart** del servicio odoo (para que sirva la base nueva).

## 7) Preconfigurar empresa + idioma
En la terminal del contenedor `odoo`:
```bash
python3 /preconfigure.py
```
Carga empresa, admin e **instala es_AR de forma robusta**. Entrás a `https://odoo.tudominio.com`
con `ODOO_ADMIN_LOGIN` / `ODOO_ADMIN_PASSWORD`.

## 8) Config fiscal AFIP/ARCA
Seguí **CONFIG-AFIP.md** (certificado, punto de venta, entorno homologación) y
**CONFIG-ARGENTINA.md** (responsabilidad frente al IVA, diarios).

## 9) n8n (a futuro)
En Coolify → New Resource → **Service → n8n** (template de un clic) → asignás subdominio y listo.
Comparte el mismo Traefik/SSL de Coolify; no toca a Odoo.

---

### Notas
- `workers = 0` (threaded) → el websocket va por el 8069, por eso Coolify rutea **un solo puerto**.
- Backups: Coolify tiene backups programados de bases Postgres (activalos en el recurso db),
  o usá `pg_dump` por terminal. Guardá también el volumen `odoo-data` (filestore).
- Cambiá el `admin_passwd` de `config/odoo.conf` antes de producción (o sobre-escribilo con un
  file-mount en Coolify).
