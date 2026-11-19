#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
#  Preconfiguración de la empresa (vía XML-RPC): empresa, admin e idioma es_AR.
#  Instala el idioma de forma ROBUSTA con base.language.install (no solo load_lang),
#  para evitar el error "Invalid language code: es_AR" en la tienda/reportes.
#  Se ejecuta DENTRO del contenedor odoo (ver COOLIFY-ODOO.md).
# ============================================================================
import os
import xmlrpc.client

URL = "http://localhost:8069"
DB = os.environ["ODOO_DB_NAME"]
NEW_LOGIN = os.environ["ODOO_ADMIN_LOGIN"]
NEW_PASSWORD = os.environ["ODOO_ADMIN_PASSWORD"]

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

uid = None
for login, pwd in [(NEW_LOGIN, NEW_PASSWORD), ("admin", "admin")]:
    try:
        cand = common.authenticate(DB, login, pwd, {})
        if cand:
            uid, AUTH_PWD = cand, pwd
            print(f">> Autenticado como '{login}' (uid={uid})")
            break
    except Exception as e:  # noqa
        print(f"   (intento '{login}' falló: {e})")
if not uid:
    raise SystemExit("!! No se pudo autenticar.")


def call(model, method, *args, **kw):
    return models.execute_kw(DB, uid, AUTH_PWD, model, method, list(args), kw)


def get(k, default=""):
    return os.environ.get(k, default)


def find_id(model, domain, ctx=None):
    kw = {"limit": 1}
    if ctx:
        kw["context"] = ctx
    res = call(model, "search", domain, **kw)
    return res[0] if res else False


# --- Instalación ROBUSTA del idioma ---
lang_code = get("COMPANY_LANG", "es_AR")
print(f">> Instalando idioma {lang_code}...")
# res.lang incluye idiomas inactivos; hay que buscar con active_test=False
lang_id = find_id("res.lang", [["code", "=", lang_code]], ctx={"active_test": False})
if lang_id:
    try:
        wiz = call("base.language.install", "create",
                   {"lang_ids": [(6, 0, [lang_id])], "overwrite": False})
        call("base.language.install", "lang_install", [wiz])
        print("   idioma instalado (base.language.install).")
    except Exception as e:  # noqa
        print(f"   (fallo base.language.install, pruebo load_lang: {e})")
        try:
            call("res.lang", "load_lang", lang_code)
        except Exception as e2:  # noqa
            print(f"   (load_lang también falló: {e2})")
    # asegurar activo
    try:
        act = find_id("res.lang", [["code", "=", lang_code]], ctx={"active_test": False})
        call("res.lang", "write", [act], {"active": True})
    except Exception:
        pass
else:
    print(f"   (no encontré res.lang para {lang_code})")

# --- País / provincia / moneda ---
country_id = find_id("res.country", [["code", "=", get("COMPANY_COUNTRY_CODE", "AR")]])
state_id = False
if country_id and get("COMPANY_STATE"):
    state_id = find_id("res.country.state",
                       [["country_id", "=", country_id], ["name", "ilike", get("COMPANY_STATE")]])
currency_id = find_id("res.currency", [["name", "=", get("COMPANY_CURRENCY", "ARS")]])
if currency_id:
    call("res.currency", "write", [currency_id], {"active": True})

# --- Empresa (id=1) ---
cvals = {
    "name": get("COMPANY_NAME"), "vat": get("COMPANY_VAT"),
    "street": get("COMPANY_STREET"), "city": get("COMPANY_CITY"),
    "zip": get("COMPANY_ZIP"), "phone": get("COMPANY_PHONE"),
    "email": get("COMPANY_EMAIL"), "website": get("COMPANY_WEBSITE"),
}
if country_id:
    cvals["country_id"] = country_id
if state_id:
    cvals["state_id"] = state_id
if currency_id:
    cvals["currency_id"] = currency_id
cvals = {k: v for k, v in cvals.items() if v}
call("res.company", "write", [1], cvals)
print(f">> Empresa actualizada: {cvals.get('name', '(sin nombre)')}")

# --- Admin ---
call("res.users", "write", [uid], {
    "name": get("COMPANY_NAME") + " Admin",
    "login": NEW_LOGIN, "email": NEW_LOGIN, "password": NEW_PASSWORD,
    "lang": lang_code, "tz": get("COMPANY_TZ", "America/Argentina/Buenos_Aires"),
})
print(f">> Admin configurado -> login: {NEW_LOGIN}")


# --- URL base (para que los links internos salgan en https) ---
def set_param(key, val):
    pid = find_id("ir.config_parameter", [["key", "=", key]])
    if pid:
        call("ir.config_parameter", "write", [pid], {"value": val})
    else:
        call("ir.config_parameter", "create", {"key": key, "value": val})


base_url = get("ODOO_BASE_URL")
if base_url:
    set_param("web.base.url", base_url)
    set_param("web.base.url.freeze", "True")  # evita que Odoo la pise al loguear
    print(f">> web.base.url = {base_url} (freeze=True)")

print("")
print("========================================================")
print("  Preconfiguración completada.")
print(f"  Login: {NEW_LOGIN}   (contraseña: la del .env)")
print("  Config fiscal AFIP/ARCA: ver CONFIG-AFIP.md")
print("========================================================")
