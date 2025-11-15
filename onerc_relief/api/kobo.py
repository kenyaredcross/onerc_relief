import requests
import frappe

from frappe.utils.password import get_decrypted_password

kobo_settings = frappe.get_single("Kobo Settings")

TOKEN = get_decrypted_password("Kobo Settings", name = "Kobo Settings", fieldname = "token")
ASSET_UID = kobo_settings.asset_uid
URL = f'{kobo_settings.url}/api/v2/assets/{ASSET_UID}/data'
headers = {"Authorization": f"Token {TOKEN}"}

def fetch_kobo_data():
    pass