import os


def exclude_list():
    with open('exclude.txt', 'r') as exclude_file:
        exclude = list(map(
            str.rstrip,
            exclude_file.readlines()
        ))
    return exclude


def generate_item_files(namespace='raft_items'):
    exclude = exclude_list()

    for path, dirs, files in os.walk(f'{namespace}/textures/item'):
        for file in files:

            if file in exclude:  # Exclude texture files listed inside exclude.txt
                continue
            new_filepath = (str(path)[len(namespace) + 14:] + f'\\{file[:-4]}').replace('\\', '/')
            print(new_filepath)
            with (open(f'{namespace}/models/item{new_filepath}.json', 'w') as model,
                  open(f'{namespace}/items{new_filepath}.json', 'w') as item):

                model.write(
f'''{{
  "parent": "item/generated",
  "textures": {{
    "layer0": "{namespace}:item''' + new_filepath + '"\n  }\n}')
                item.write(
f'''{{"model":{{
    "type": "minecraft:model",
    "model": "{namespace}:item''' + new_filepath + '"\n}}')


def generate_lang_files(namespace='raft_items', entrytype='item.mineraft.', path=None, entryname_prefix=''):
    exclude = exclude_list()

    with open(f'{namespace}/lang/temp.json', 'a+') as lang_file:
        filenames = os.listdir(f'{namespace}/textures/item' if path is None else path)
        lang_file.seek(0)
        lines = set(map(
            lambda s: s[:-2] if s[-2] == ',' else s[:-1],
            lang_file.readlines()[1:-1]
        ))
        lang_file.seek(0)
        lang_file.truncate()

        for file in filenames:
            if file[-4:] != '.png' or file in exclude:
                continue
            print(file)

            entryname = file[:-4]
            lines.add(
                f'  "{entrytype}{entryname}": "{entryname_prefix}{entryname.replace("_", " ").title()}"')

        lang_file.write('{\n')
        lang_file.write(',\n'.join(sorted(lines)))
        lang_file.write('\n}\n')


generate_item_files()
generate_lang_files()
for path, dirs, files in os.walk('raft_items/textures/item/structure'):
    generate_lang_files(
        entrytype=f'structure.mineraft.{path[35:]}_'.replace("\\", "_"), path=path, entryname_prefix=f'{path[35:]} '.replace("_", " ").title())
