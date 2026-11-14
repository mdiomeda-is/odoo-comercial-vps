# Configuración Argentina — Multiempresa, Facturación e IVA (Odoo 18 Community)

Estos pasos se hacen **una vez, dentro de Odoo**, después de correr los scripts.
Cubren: multiempresa (dos CUITs), plan de cuentas + IVA argentino, condiciones frente
al IVA, diario **Factura A** (fiscal) y diario **Presupuesto** (no va a ARCA).

> Recordá: en Community la emisión electrónica automática a ARCA (CAE por webservice) NO
> está incluida. Acá configurás todo y la Factura A se registra cargando el **CAE a mano**
> (obtenido del portal ARCA). La automatización es Enterprise o módulos EDI de comunidad.

---

## 1) Activar modo desarrollador
**Ajustes** → al final → **Activar el modo de desarrollador**.

> NOTA: en Odoo **Community** la app de contabilidad se llama **Facturación** (Invoicing).
> La "Contabilidad" completa es Enterprise. Donde la guía dice "Facturación", es esa app.

## 2) Localización fiscal de la Empresa 1
**Ajustes → Facturación** → sección *Impuestos / Localización Fiscal* → **País fiscal: Argentina**
(y el paquete según la responsabilidad de la empresa):
- **Responsable Inscripto (RI)** → habilita **Factura A / B / C**.
- **Monotributo** → Factura C.
- **Exento**.

Al aplicarlo se instala el **plan de cuentas** y los **impuestos de IVA** (21%, 10,5%, 27%,
Exento, No Gravado). Definí la **Condición frente al IVA** de la empresa.

## 3) Empresas adicionales (uno o más CUITs) — Multiempresa
Sin límite de empresas. Repetí este bloque **por cada CUIT** (2do, 3ro, 4to…):
1. **Ajustes → Usuarios y Empresas → Empresas → Nueva**.
2. Cargá **Nombre**, **CUIT** (campo identificación/NIF), dirección, **moneda ARS** y su
   **Condición frente al IVA**. Guardar.
3. Al haber 2+ empresas aparece el **selector de empresas** (arriba a la derecha) → multiempresa activa.
4. **Aplicá la localización fiscal (paso 2)** pero **seleccionando esa empresa** en el selector,
   para instalarle su **propio plan de cuentas AR**.
5. **Creá sus diarios (paso 5)**: cada empresa tiene sus PROPIOS diarios → una **Factura A** y
   un **Presupuesto** por empresa (los diarios NO se comparten entre empresas).
6. **Usuarios → admin → Empresas permitidas**: habilitá todas las empresas que deba operar
   cada usuario.

> Con esto podés **facturar desde varios CUITs**: cada factura toma la empresa activa, su
> plan de cuentas y su diario. El procedimiento es idéntico para 2, 3 o más empresas.

## 4) Verificar IVA
**Facturación → Configuración → Impuestos** (por empresa): deben existir IVA Ventas/Compras
**21%, 10,5%, 27%, Exento, No Gravado**. En **Ajustes → Facturación** definí los impuestos
por defecto de venta y compra.
También revisá **Facturación → Configuración → Plan de cuentas** (debe tener cuentas AR).

## 5) Diarios de venta
**Facturación → Configuración → Diarios**:

**a) Factura A (fiscal → ARCA)**
- Diario de tipo **Venta** con **"Usar documentos" = Sí**.
- Con empresa RI y cliente RI, habilita **Factura A** (y B/C según el cliente).
- Emisión: en Community cargás el **CAE** manualmente al validar (ver paso 7).

**b) Presupuesto (NO va a ARCA)**
- Crear un diario de tipo **Venta** nuevo, nombre "Presupuesto", **"Usar documentos" = No**.
- Emite comprobantes internos **sin tipo AFIP** → no se declaran. Ideal para lo no fiscal.
- (Alternativa: usar **Presupuestos de venta / cotizaciones**, que nunca van a ARCA.)

## 6) Clientes y proveedores
En cada contacto, pestaña **Facturación/Contabilidad**:
- **Condición frente al IVA** (RI, Monotributo, Consumidor Final, Exento, etc.).
- **Tipo y N° de documento** (CUIT/DNI).
Esto define automáticamente si corresponde **Factura A o B**.

## 7) Carga manual del CAE (Factura A)
Al **validar** una factura del diario Factura A, completá el **CAE** y su **vencimiento**
(campos de autorización AFIP de la factura) con los datos obtenidos del portal ARCA.

---

## Checklist de verificación
- [ ] Empresa 1 con plan de cuentas AR e IVA.
- [ ] Empresa 2 creada con su CUIT y su plan de cuentas AR.
- [ ] Selector de empresas visible; admin con acceso a ambas.
- [ ] Impuestos IVA (21 / 10,5 / 27 / Exento / No Gravado) presentes.
- [ ] Diario Factura A ("Usar documentos = Sí").
- [ ] Diario Presupuesto ("Usar documentos = No").
- [ ] Un cliente de prueba con Condición frente al IVA y CUIT.
- [ ] Factura A de prueba (con CAE manual) y un Presupuesto de prueba.
