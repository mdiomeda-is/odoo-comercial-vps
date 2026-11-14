# Cloudflare Free delante de Odoo (edge gratis)

Esquema: **Cloudflare Free → VPS → Coolify/Traefik → Odoo (8069) + PostgreSQL**.
Con el plan Free tenés DNS, SSL, protección DDoS y proxy sin pagar nada.

## Orden recomendado (para que salga el SSL)
1. Primero dejá el registro del dominio en **DNS only (nube gris)** y desplegá en Coolify →
   así Let's Encrypt emite el certificado del origen sin interferencia.
2. Cuando ya entra por HTTPS, pasá el registro a **Proxied (nube naranja)**.
3. En Cloudflare, **SSL/TLS → Full (strict)**.

## Lo que funciona bien en Free
- DNS, SSL, DDoS y proxy.
- **WebSockets**: Odoo usa `/websocket` para chat/notificaciones; Cloudflare Free lo soporta.

## Límites de Free a tener en cuenta
- **Uploads hasta 100 MB**: restaurar backups grandes o importar archivos pesados por la web
  se corta. Esos restores hacelos **por consola / directo al servidor**.
- **Timeout de 100 s**: reportes o importaciones muy largas → error **524** en pantalla
  (el proceso sigue en Odoo por detrás). Para procesos largos usá **crons / jobs en segundo plano**.

## Configuración recomendada en Cloudflare
1. **SSL/TLS = Full (strict)**.
2. **WAF → regla personalizada para bloquear `/web/database`** (el gestor de bases): es la
   más importante. Además en `config/odoo.conf` ya está `list_db = False` y un `admin_passwd`.
   - Regla: *Field* URI Path **contains** `/web/database` → *Action* **Block**.
3. **Rocket Loader = OFF** y cualquier "optimización de JavaScript" (rompen la UI de Odoo).
   - Speed → Optimization → Content Optimization → desactivar Rocket Loader.
4. **No cachear `/web`**: dejá el cache por defecto (solo estáticos). Si activaste algo agresivo,
   creá una regla **Bypass cache** para `/web/*`.
5. **Email**: Cloudflare NO proxea SMTP. Los registros **MX** y el host de mail van en
   **DNS only (nube gris)**. Configurá **SPF** y **DKIM** si Odoo manda correos.

## En Odoo / Coolify (ya contemplado)
- `proxy_mode = True` en `config/odoo.conf` (toma bien la IP real y HTTPS de los headers).
- Coolify/Traefik maneja el certificado del origen (para el Full strict de Cloudflare).

Con esto tenés un Odoo productivo detrás de Cloudflare sin pagar nada de CF.

## CrowdSec (opcional, fase 2)
Para la capa IPS open-source detrás de Cloudflare: se puede sumar **CrowdSec** al Traefik de
Coolify (bouncer + colecciones). Es avanzado y conviene hacerlo una vez que Odoo esté estable;
mientras tanto, Cloudflare Free ya te da DDoS/WAF en el borde. Lo dejamos como paso posterior.
