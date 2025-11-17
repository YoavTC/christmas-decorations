"""
Standalone script to validate and fix spawn function files.
Ensures all summon commands follow the correct format:
- No leading slashes
- Coordinates are ~ ~ ~
- Tags:[christmasdeco_parent] is present
- count:1 (not Count:1)
"""
import os
import re


def validate_spawn_functions(spawn_function_dir):
    """
    Validate and fix all spawn function files in the given directory.
    
    Args:
        spawn_function_dir: Path to directory containing .mcfunction files
        
    Returns:
        dict: Summary of validation results
    """
    print(f'\nValidating spawn function files in: {spawn_function_dir}')
    
    results = {
        'total_files': 0,
        'empty_files': 0,
        'modified_files': 0,
        'valid_files': 0,
        'issues_fixed': []
    }
    
    if not os.path.exists(spawn_function_dir):
        print(f'Error: Directory does not exist: {spawn_function_dir}')
        return results
    
    for filename in os.listdir(spawn_function_dir):
        if not filename.endswith('.mcfunction'):
            continue
            
        results['total_files'] += 1
        filepath = os.path.join(spawn_function_dir, filename)
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip empty files
        if not content.strip():
            results['empty_files'] += 1
            print(f'  ⚠ {filename}: Empty file')
            continue
        
        # Process each line
        lines = content.split('\n')
        modified = False
        file_issues = []
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Remove leading slash if present
            if stripped_line.startswith('/summon'):
                stripped_line = stripped_line[1:]
                modified = True
                issue = f'Removed leading slash'
                file_issues.append(issue)
            
            if stripped_line.startswith('summon '):
                # Ensure coordinates are ~ ~ ~
                coord_match = re.search(r'(summon\s+\S+\s+)([^\s]+\s+[^\s]+\s+[^\s]+)(\s+.*)', stripped_line)
                if coord_match:
                    prefix = coord_match.group(1)
                    coords = coord_match.group(2)
                    suffix = coord_match.group(3)
                    
                    if coords != '~ ~ ~':
                        stripped_line = prefix + '~ ~ ~' + suffix
                        modified = True
                        issue = f'Changed coordinates to ~ ~ ~'
                        file_issues.append(issue)
                
                # Check if Tags:[christmasdeco_parent] is present
                if 'Tags:[christmasdeco_parent]' not in stripped_line:
                    match = re.search(r'(summon\s+\S+\s+~\s+~\s+~\s+)(\{.*)', stripped_line)
                    if match:
                        prefix = match.group(1)
                        nbt_data = match.group(2)
                        
                        if nbt_data.startswith('{') and len(nbt_data) > 1:
                            stripped_line = prefix + '{Tags:[christmasdeco_parent],' + nbt_data[1:]
                            modified = True
                            issue = f'Added Tags:[christmasdeco_parent]'
                            file_issues.append(issue)
                
                # Replace Count:1 with count:1
                if 'Count:1' in stripped_line:
                    stripped_line = stripped_line.replace('Count:1', 'count:1')
                    modified = True
                    issue = f'Fixed Count:1 to count:1'
                    file_issues.append(issue)
            
            lines[i] = stripped_line
        
        # Write back if modified
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            results['modified_files'] += 1
            results['issues_fixed'].append({
                'file': filename,
                'issues': file_issues
            })
            print(f'  ✓ {filename}: Fixed {len(file_issues)} issue(s)')
            for issue in file_issues:
                print(f'    - {issue}')
        else:
            results['valid_files'] += 1
            print(f'  ✓ {filename}: Already valid')
    
    return results


def print_summary(results):
    """Print a summary of validation results"""
    print('\n' + '=' * 60)
    print('VALIDATION SUMMARY')
    print('=' * 60)
    print(f'Total files processed: {results["total_files"]}')
    print(f'Empty files skipped:   {results["empty_files"]}')
    print(f'Files modified:        {results["modified_files"]}')
    print(f'Files already valid:   {results["valid_files"]}')
    print('=' * 60)


def main():
    """Main entry point when script is run directly"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    spawn_function_dir = os.path.join(project_root, 'src', 'data', 'christmasdeco', 'function', 'spawn')
    
    results = validate_spawn_functions(spawn_function_dir)
    print_summary(results)


if __name__ == '__main__':
    main()
