import frappe, json, base64, requests

from frappe.utils.password import get_decrypted_password

kobo_settings = frappe.get_single("Kobo Settings")

TOKEN = get_decrypted_password("Kobo Settings", name = "Kobo Settings", fieldname = "token")
ASSET_UID = kobo_settings.asset_uid
URL = f'{kobo_settings.url}/api/v2/assets/{ASSET_UID}/data'

headers = {"Authorization": f"Token {TOKEN}"}


@frappe.whitelist(allow_guest=True)
def receive_kobo_submission():
    data = frappe.request.get_json()
    if not data:
        frappe.throw("No Data Received")


    headers = dict(frappe.request.headers)

    # doctype = headers.get("doctype")
    # if not doctype:
    #     frappe.throw("'doctype' header not found!")

    doctype = "Targeted Persons"
    
    # if data.get("skipconnect") == "1":
    #     return {"status": "skipped"}

    # Mapp the headers from kobo onto frappe

    doc_fields = {}
    for kobo_field, frappe_field in headers.items():

        # Ignore system headers
        if kobo_field.lower() in [
            "content-type", "user-agent", "host", "doctype", "updateby", "authorization"
        ]:
            continue



        if kobo_field in data:

            kobo_value = data[kobo_field]

            # Default Value
            kobo_value_sanitized = kobo_value

            #  Convert Kobo select options from snake_case to Capitalized
            if "_" in kobo_value:
                from onerc_relief.utils.kobo_helpers import capitalize_kobo_options
                kobo_value_sanitized = capitalize_kobo_options(kobo_value)

            doc_fields[frappe_field] = kobo_value_sanitized

    existing = None
    if "updateby" in headers:
        fieldname = headers["updateby"]
        existing = frappe.db.exists(doctype, {fieldname: doc_fields.get(fieldname)})
    
    if existing:
        doc = frappe.get_doc(doctype, existing)
        doc.update(doc_fields)
    else:
        doc = frappe.get_doc({
            "doctype": doctype,
            **doc_fields
        })


    doc.save(ignore_permissions = True)    
    frappe.db.commit()

    return {"status": "success", "name": doc.name}

