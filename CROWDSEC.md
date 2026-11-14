# CrowdSec — capa IPS (FASE 2, después de validar Odoo)

> NO instalar en la primera vuelta. Primero: Odoo 19 + AFIP validado + Cloudflare estable.
> CrowdSec se suma cuando ya hay tráfico real y la base funciona.

## Qué es
CrowdSec es un IPS open-source: lee logs (de Traefik/Odoo), detecta patrones de ataque
(fuerza bruta, scraping, escaneos) y **decide bloquear IPs**. Un "bouncer" aplica esas decisiones.

## Arquitectura recomendada para TU caso (Cloudflare delante)
Como Cloudflare proxea, el origen ve IPs de Cloudflare, no las reales. Por eso el bouncer
ideal **no** es el de Traefik, sino el **bouncer de Cloudflare**: CrowdSec manda las IPs
maliciosas a la **WAF de Cloudflare** y se bloquean **en el borde** (antes de llegar al VPS).

```
Logs (Traefik/Odoo) → CrowdSec (analiza) → decisiones → Cloudflare bouncer → bloqueo en el borde
```

## Pasos (resumen, a afinar al momento)
1. **Restaurar IP real** en Traefik/Coolify: para que CrowdSec vea la IP del visitante (no la de
   Cloudflare), Traefik debe confiar en los headers `CF-Connecting-IP` / `X-Forwarded-For` de
   Cloudflare. (Coolify/Traefik: configurar `forwardedHeaders.trustedIPs` con los rangos de Cloudflare.)
2. **Instalar CrowdSec** (contenedor o paquete) apuntando a los logs de acceso de Traefik:
   ```bash
   # ejemplo con Docker: crowdsecurity/crowdsec, con acquis.yaml leyendo los logs de Traefik
   ```
3. **Colecciones**: instalar `crowdsecurity/traefik` y `crowdsecurity/http-cve` /
   `crowdsecurity/base-http-scenarios` (`cscli collections install ...`).
4. **Token de Cloudflare**: crear un **API Token** con permiso de editar la WAF/Firewall de la zona.
5. **Bouncer de Cloudflare**:
   ```bash
   # cs-cloudflare-bouncer: se configura con el token y la zona; CrowdSec le pasa las decisiones.
   cscli bouncers add cloudflare-bouncer
   # cargar la API key del bouncer y el token de Cloudflare en su config, y arrancarlo.
   ```
6. **Verificar**: `cscli decisions list` muestra las IPs bloqueadas; deberían aparecer en la
   lista de IPs bloqueadas de Cloudflare.

## Alternativa más simple (sin Cloudflare bouncer)
Si en algún momento sacás Cloudflare o querés bloqueo local: **`crowdsec-firewall-bouncer`**
(bloquea con iptables/nftables en el host). Más simple, pero bloquea en el VPS, no en el borde,
y necesita igual la IP real restaurada.

## Mantenimiento
- `cscli metrics` para ver qué está detectando.
- `cscli decisions delete --ip X` para desbloquear una IP (falsos positivos).
- Mantené CrowdSec y las colecciones actualizadas.

> Todo esto es independiente de Odoo: si CrowdSec tiene un problema, Odoo sigue funcionando.
> Por eso conviene sumarlo **después** de tener la base andando.
