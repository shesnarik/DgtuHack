import json

with open('handlers/keyboards/admin/admin_trigger_settings.txt', 'r', encoding='utf-8') as file:
    trigger_config = file.read()
    json_content = f"{{{trigger_config}}}"
    my_list_str = json.loads(json_content)
