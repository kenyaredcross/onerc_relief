
# def capitalize_kobo_options(kobo_option):
#     options = kobo_option.split("_")

#     select_options = [option.capitalize() for option in options]

#     return ' '.join(select_options)


def cleanup_kobo_select_options(kobo_field: str) -> str:
    
    '''
        Receives Kobo Single Choice (snake_case) and Multichoice (snake_case seperated by spaces)
        and converts them to Proper Nouns seperated by space and commas for multi-select 

    '''
    select_options = kobo_field.split(" ") 

    cleaned_options = []

    for select_option in select_options:
        options = select_option.split("_")
        cleaned_options.append(" ".join(option.capitalize() for option in options))

    return ", ".join(cleaned_options)
