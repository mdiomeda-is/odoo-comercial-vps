# Factura Electrónica AFIP/ARCA en Odoo 19 (módulo ADHOC `l10n_ar_fiscal_ws`)

En Odoo **19** el módulo de factura electrónica de ADHOC se llama **`l10n_ar_fiscal_ws`**
(reemplaza al `l10n_ar_afipws_fe` de 18). Se instala desde el repo `ingadhoc/odoo-argentina-ce`
rama **19.0** (ya clonado en la imagen por el Dockerfile) y, a diferencia de 18, **no declara
librerías Python externas** (no hace falta pyafipws/pysimplesoap).

> ⚠️ ESTADO: este módulo para 19 está **mantenido por ADHOC pero NO lo validamos nosotros**
> de punta a punta todavía. Por eso TODO esto se hace primero en **HOMOLOGACIÓN** (entorno de
> prueba de ARCA, sin validez fiscal). Si emite un CAE de prueba OK, queda bendecido para 19;
> si algo falla, caemos a Odoo 18 (stack ya validado).

## Instalación
Ya viene en la imagen (Dockerfile clona ADHOC 19.0 en `/mnt/adhoc`, y el addons_path lo incluye).
Se instala en el paso 6 de COOLIFY-ODOO.md (`-i ...,l10n_ar_fiscal_ws`).
Si ese paso tira error de "módulo no instalable" o falta una dependencia, pegámelo y lo ajusto.

## Requisitos en ARCA (por cada CUIT) — HOMOLOGACIÓN primero
1. **Certificado digital**: Odoo genera el pedido (CSR). En homologación se sube por **WSASS**
   y se descarga el `.crt`. En producción, por "Administración de Certificados Digitales" (Clave Fiscal nivel 3).
2. **Autorizar el web service** de factura electrónica (wsfe) al certificado, en el
   **Administrador de Relaciones de Clave Fiscal**.
3. **Punto de venta** tipo **Web Services** dado de alta en ARCA. Anotá el número.

## Configuración en Odoo (por empresa)
Con **modo desarrollador** activo:
1. **Empresa** (Ajustes → Empresas): confirmá **CUIT** y **Condición frente al IVA**
   (Responsable Inscripto para Factura A). Buscá la sección **AFIP / Web Services** (la agrega el módulo):
   - **Entorno**: *Homologación* (para probar) / *Producción*.
   - **Generar CSR** → obtené el `.crt` en ARCA → **cargar certificado**.
2. **Punto de venta** electrónico con el número dado de alta en ARCA.
3. **Diario de ventas** Factura A: asociarlo al punto de venta electrónico.
4. **Clientes**: Condición frente al IVA + CUIT/DNI correctos (definen Factura A o B).

## Emisión (prueba en homologación)
Al **validar** una factura del diario electrónico, Odoo se autentica (WSAA con tu certificado),
pide el **CAE** (web service) y lo estampa. Si ARCA devuelve un **CAE de homologación**, funciona.

## Si pasa homologación → producción
Cambiá **Entorno = Producción**, cargá el certificado de producción y usá el punto de venta real.

---
Las responsabilidades frente al IVA, el plan de cuentas y los diarios se arman igual que en
**CONFIG-ARGENTINA.md** (la app en Community se llama **Facturación**, no "Contabilidad").
