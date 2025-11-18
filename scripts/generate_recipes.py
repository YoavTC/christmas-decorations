import json
import csv
import os

def recipe_output_to_loot_table(recipe_data):
    """
    Converts Minecraft recipe output to a loot table JSON.
    """
    result = recipe_data.get("result", {})
    item_id = result.get("id", "minecraft:air")
    item_count = result.get("count", 1)
    components = result.get("components", {})

    entry = {
        "type": "minecraft:item",
        "name": item_id,
    }
    functions = []
    if components:
        functions.append({
            "function": "minecraft:set_components",
            "components": components
        })
    if item_count > 1:
        functions.append({
            "function": "minecraft:set_count",
            "count": item_count
        })
    if functions:
        entry["functions"] = functions

    loot_table = {
        "pools": [
            {
                "rolls": 1,
                "entries": [entry]
            }
        ]
    }
    return loot_table

def load_original_keys(item_id, original_recipe_dir):
    """Load the original key mappings, custom name, and christmasdeco_id from existing recipe file"""
    original_file = os.path.join(original_recipe_dir, f'{item_id}.json')
    if os.path.exists(original_file):
        with open(original_file, 'r', encoding='utf-8') as f:
            original_recipe = json.load(f)
            # Extract custom name from the middle element of the custom_name array
            custom_name_components = original_recipe['result']['components']['minecraft:custom_name']
            custom_name = custom_name_components[1]['text'] if isinstance(custom_name_components, list) else custom_name_components.get('text', '')
            return {
                'keys': original_recipe.get('key', {}),
                'custom_name': custom_name,
                'christmasdeco_id': original_recipe['result']['components']['minecraft:custom_data']['christmasdeco_id']
            }
    return None

def numeric_to_pattern(numeric_pattern, keys):
    """Convert numeric pattern back to recipe pattern with keys"""
    # Create mapping of numbers to keys
    key_list = list(keys.keys())
    num_to_key = {str(idx): key for idx, key in enumerate(key_list, 1)}
    num_to_key['0'] = ' '
    
    # Determine pattern dimensions based on length
    pattern_length = len(numeric_pattern)
    if pattern_length == 6:  # 2x3 pattern
        rows = 2
        cols = 3
    elif pattern_length == 9:  # 3x3 pattern
        rows = 3
        cols = 3
    else:
        # Try to infer dimensions
        rows = (pattern_length + 2) // 3  # Round up division
        cols = 3
    
    # Convert numeric string to pattern
    pattern = []
    for i in range(rows):
        row = ''
        for j in range(cols):
            idx = i * cols + j
            if idx < len(numeric_pattern):
                row += num_to_key.get(numeric_pattern[idx], ' ')
            else:
                row += ' '
        pattern.append(row)
    
    return pattern

def create_recipe_json(item_id, recipe_keys, recipe_pattern, texture, hitbox, placement, author, url, original_data=None):
    """Create a recipe JSON structure from CSV data"""
    # Parse recipe keys
    key_items = [k.strip() for k in recipe_keys.split(',')]
    
    # Add minecraft: prefix if not present
    key_items = [f'minecraft:{item}' if not item.startswith('minecraft:') and not item.startswith('#') else item for item in key_items]
    
    # Use original keys if available, otherwise create new mapping
    if original_data and 'keys' in original_data:
        keys = original_data['keys']
    else:
        # Create key mapping
        # Standard single character keys
        key_chars = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        keys = {}
        for i, item in enumerate(key_items):
            if i < len(key_chars):
                keys[key_chars[i]] = item
    
    # Convert numeric pattern to recipe pattern
    pattern = numeric_to_pattern(recipe_pattern, keys)
    
    # Parse hitbox into width and height
    hitbox_parts = hitbox.split(',')
    width = float(hitbox_parts[0].strip())
    height = float(hitbox_parts[1].strip())

    # Parse placement enum
    placement_mapping = {
        'FLOOR': 1,
        'WALL': 2,
        'CEILING': 4,
    }
    placement_list = [p.strip().upper() for p in placement.split(',') if p.strip()]
    placement_type = 0
    for p in placement_list:
        placement_type |= placement_mapping.get(p, 0)

    # Use original custom name if available, otherwise generate from item_id
    if original_data and 'custom_name' in original_data:
        custom_name = original_data['custom_name']
    else:
        custom_name = f"{item_id.replace('_', ' ').title()} Decoration"
    
    # Use original christmasdeco_id if available, otherwise use item_id
    if original_data and 'christmasdeco_id' in original_data:
        christmasdeco_id = original_data['christmasdeco_id']
    else:
        christmasdeco_id = item_id
    
    # Create the full recipe structure
    recipe = {
        "type": "minecraft:crafting_shaped",
        "key": keys,
        "pattern": pattern,
        "result": {
            "components": {
                "minecraft:enchantment_glint_override": False,
                "minecraft:item_model": "player_head",
                "minecraft:profile": {
                    "properties": [
                        {
                            "name": "textures",
                            "value": texture
                        }
                    ]
                },
                "minecraft:custom_data": {
                    "christmasdeco": True,
                    "christmasdeco_id": christmasdeco_id,
                    "christmasdeco_placement": placement_type,
                    "christmasdeco_width": width,
                    "christmasdeco_height": height
                },
                "minecraft:custom_name": [
                    {
                        "text": "❄ ",
                        "color": "#ec2d53",
                        "bold": True,
                        "italic": False
                    },
                    {
                        "text": custom_name,
                        "color": "white",
                        "bold": True,
                        "italic": False
                    },
                    {
                        "text": " ❄",
                        "color": "#ec2d53",
                        "bold": True,
                        "italic": False
                    }
                ],
                
                "minecraft:lore": [
                    [
                        {
                            "text": f"Model by {author}",
                            "color": "dark_gray",
                            "bold": False,
                            "italic": False
                        }
                    ],
                    [
                        {
                            "text": url,
                            "color": "dark_gray",
                            "bold": False,
                            "italic": False
                        }
                    ]
                ]
            },
            "count": 1,
            "id": "minecraft:debug_stick"
        },
        "show_notification": False
    }
    
    return recipe

def main():
    # Paths (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    csv_file = os.path.join(script_dir, 'items.csv')
    recipe_output_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'recipe')
    loot_table_output_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'loot_table')
    function_output_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'function')
    # Base spawn directory now contains placement subfolders: floor, wall, ceiling
    spawn_function_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'function', 'spawn')
    original_recipe_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'recipe')
    
    # Create output directories
    os.makedirs(recipe_output_dir, exist_ok=True)
    os.makedirs(loot_table_output_dir, exist_ok=True)
    os.makedirs(function_output_dir, exist_ok=True)
    os.makedirs(spawn_function_dir, exist_ok=True)
    # Ensure placement subdirectories exist
    placement_subdirs = {
        'FLOOR': os.path.join(spawn_function_dir, 'floor'),
        'WALL': os.path.join(spawn_function_dir, 'wall'),
        'CEILING': os.path.join(spawn_function_dir, 'ceiling'),
    }
    for p in placement_subdirs.values():
        os.makedirs(p, exist_ok=True)
    
    # List to store all recipe IDs for the mcfunction file
    recipe_ids = []
    
    # Read CSV and generate recipes
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for row in reader:
            item_id = row['id']
            recipe_keys = row['recipe keys']
            recipe_pattern = row['recipe pattern']
            texture = row['texture']
            hitbox = row['hitbox']
            placement = row['placement']
            author = row['author']
            url = row['url']

            # Derive placement list for spawn file generation (was previously undefined)
            placement_list = [p.strip().upper() for p in placement.split(',') if p.strip()]
            
            # Load original keys to preserve key letter mappings
            original_data = load_original_keys(item_id, original_recipe_dir)
            
            # Generate recipe JSON
            recipe = create_recipe_json(item_id, recipe_keys, recipe_pattern, texture, hitbox, placement, author, url, original_data)
            
            # Write recipe to file
            recipe_output_file = os.path.join(recipe_output_dir, f'{item_id}.json')
            with open(recipe_output_file, 'w', encoding='utf-8') as out_f:
                json.dump(recipe, out_f, indent=2, ensure_ascii=False)
            
            # Generate loot table from recipe
            loot_table = recipe_output_to_loot_table(recipe)
            
            # Write loot table to file (always overwrite)
            loot_table_output_file = os.path.join(loot_table_output_dir, f'{item_id}.json')
            with open(loot_table_output_file, 'w', encoding='utf-8') as out_f:
                json.dump(loot_table, out_f, indent=2, ensure_ascii=False)
            
            # Generate spawn function files per placement (empty if new)
            for placement_flag in placement_list:
                subdir_key = placement_flag.upper()
                if subdir_key in placement_subdirs:
                    spawn_function_file = os.path.join(placement_subdirs[subdir_key], f'{item_id}.mcfunction')
                    if not os.path.exists(spawn_function_file):
                        with open(spawn_function_file, 'w', encoding='utf-8') as out_f:
                            out_f.write('')  # Create empty file for manual editing later
                        print(f'Generated: spawn/{subdir_key.lower()}/{item_id}.mcfunction (empty)')
            
            # Add to recipe IDs list
            recipe_ids.append(item_id)
            
            print(f'Generated: {item_id}.json (recipe, loot table, and advancement)')
    
    # Generate grant_all_recipes.mcfunction file (always overwrite)
    mcfunction_file = os.path.join(function_output_dir, 'give_all_recipes.mcfunction')
    with open(mcfunction_file, 'w', encoding='utf-8') as f:
        for recipe_id in recipe_ids:
            f.write(f'recipe give @a christmasdeco:{recipe_id}\n')
    
    print(f'Generated: give_all_recipes.mcfunction')
    print(f'\nRecipes generated in: {recipe_output_dir}')
    print(f'Loot tables generated in: {loot_table_output_dir}')
    print(f'Spawn functions generated in: {spawn_function_dir}')
    print(f'Function generated in: {function_output_dir}')

if __name__ == '__main__':
    main()
