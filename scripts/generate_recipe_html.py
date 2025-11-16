import csv
import os
import re

def generate_recipe_html_from_csv(csv_path):
    """
    Generate HTML recipe list from items.csv
    
    Args:
        csv_path: Path to the items.csv file
    
    Returns:
        String containing the generated HTML figures
    """
    html_figures = []
    
    # Read the CSV file
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        rows = sorted(reader, key=lambda x: x['id'])
        
        for row in rows:
            item_id = row['id']
            author = row['author']
            url = row['url']
            
            # Convert item_id to display name (e.g., "bamboo_flower_cart" -> "Bamboo Flower Cart")
            display_name = item_id.replace('_', ' ').title()
            
            # Generate the image filename
            image_filename = f"{item_id}.png"
            
            # Create the figure HTML
            figure_html = f'''                <figure>
                    <img src="recipe images/{image_filename}">
                    <figcaption>
                        <h3>{display_name}</h3>
                        <a href="https://{url}" target="_blank">{author}</a>
                    </figcaption>
                </figure>'''
            
            html_figures.append(figure_html)
    
    # Join all figures with newlines
    return '\n'.join(html_figures)


def update_index_html(csv_path, html_path):
    """
    Update the index.html file with generated recipe HTML
    
    Args:
        csv_path: Path to the items.csv file
        html_path: Path to the index.html file
    """
    # Generate the recipe HTML
    recipe_html = generate_recipe_html_from_csv(csv_path)
    
    # Read the current index.html
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Pattern to match the recipe-list div and its contents
    pattern = r'(<div class="recipe-list">)\s*.*?\s*(</div>)'
    
    # Replace the content between <div class="recipe-list"> and </div>
    replacement = f'\\1\n{recipe_html}\n            \\2'
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write the updated HTML back to the file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"✓ Successfully updated {html_path}")
    print(f"✓ Generated {len(recipe_html.count('<figure>'))} recipe items")


if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "items.csv")
    html_path = os.path.join(script_dir, "..", "docs", "index.html")
    
    # Update the index.html file
    update_index_html(csv_path, html_path)
