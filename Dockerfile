# ============================================================================
#  Imagen Odoo 19 + módulos AFIP/ARCA de ADHOC (rama 19.0) + config base.
#  En 19 el módulo es 'l10n_ar_fiscal_ws' y su manifiesto NO declara librerías
#  Python externas (a diferencia de 18, que necesitaba pyafipws/pysimplesoap).
#  Por eso acá SOLO clonamos los módulos y copiamos el odoo.conf.
#  >> Si al instalar el módulo faltara alguna lib Python, se agrega un
#     'pip3 install --break-system-packages ...' en este mismo RUN.
# ============================================================================
ARG ODOO_VERSION=19.0
FROM odoo:${ODOO_VERSION}

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/* \
 && git clone --depth 1 -b 19.0 https://github.com/ingadhoc/odoo-argentina-ce.git /mnt/adhoc \
 && chown -R odoo:odoo /mnt/adhoc

# Config base (sin secretos de DB: esos van por variables de entorno HOST/USER/PASSWORD).
COPY config/odoo.conf /etc/odoo/odoo.conf
# Script de preconfiguración, para correrlo desde la terminal de Coolify.
COPY scripts/preconfigure.py /preconfigure.py

USER odoo
