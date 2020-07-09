import json
import sys
with open(sys.argv[1]) as json_file:
    cli_note_data = json.load(json_file)

    new_data = []
    for data in cli_note_data['data']:
        data['cli_note'] = [data['cli_note']]
        data['description'] = [data['description']]
        new_data.append(data)
    
    with open(sys.argv[1] + '_new', 'w') as outfile:
        json.dump(cli_note_data, outfile, indent=4)