import json

try:
    # Leemos el archivo JSON y tratamos de analizar sus datos
    with open('result.json', encoding='utf-8', errors='ignore') as f:
        try:
            data = json.load(f)
        except ValueError:
            print("Hubo un problema al analizar el archivo JSON.")
            data = {"contacts":{"list":[]}}
except Exception as ex:
    print(f"Ocurrió un error grave ({type(ex)}): {str(ex)}")
    data = {"contacts":{"list":[]}}

# Continuamos procesándolos como antes
if data and data.get('contacts') and data['contacts'].get('list'):
    for entry in data['contacts']['list']:
        first_name = entry.get('first_name')
        last_name = entry.get('last_name')
        phone_number = entry.get('phone_number')
        date = entry.get('date')
        date_unix_time = entry.get('date_unixtime')
        
        if first_name is None or last_name is None or phone_number is None:
            continue

        country_code = ''
        while len(phone_number) >= 3 and phone_number[0] == '0':
            phone_number = phone_number[1:]
        country_code += ''.join(['+' + phone_number[:3]])
        phone_number = phone_number[3:].lstrip('0')
        phone_number = country_code + ' ' + phone_number if phone_number else ''

        # Genera las líneas vCard
        # Genera las líneas vCard (versión 2.1)
        vcard_lines = []
        vcard_lines.append(f'BEGIN:VCARD\n')
        vcard_lines.append(f'VERSION:2.1\n')
        vcard_lines.append(f'N:{last_name};{first_name};;\n')
        vcard_lines.append(f'FN:{first_name} {last_name}\n')
        vcard_lines.append(f'TEL;TYPE=CELL,VOICE:{phone_number}\n')
        vcard_lines.append(f'END:VCARD\n')

        # Escribimos las líneas vCard en un archivo
        with open('output.vcf', 'a', encoding='utf-8') as f:
            f.writelines(vcard_lines)
else:
    print("El archivo JSON parece estar vacío o mal formateado.")