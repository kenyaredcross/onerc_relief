import frappe

def capitalize_kobo_options(kobo_option):
    options = kobo_option.split("_")

    select_options = [option.capitalize() for option in options]

    return ' '.join(select_options)
