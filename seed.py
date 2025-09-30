import csv
import ast
from app import app, db, Recipe, Ingredient, recipe_ingredients

def get_or_create_ingredient(session, name):
    """
    Helper function to get an ingredient by name or create it if it doesn't exist.
    We pass the session explicitly to manage it better.
    """
    ingredient = session.query(Ingredient).filter_by(name=name).first()
    if not ingredient:
        ingredient = Ingredient(name=name)
        session.add(ingredient)
    return ingredient

def seed_database():
    with app.app_context():
        # *** FIX IS HERE: Create all tables based on the models ***
        print("Creating database tables...")
        db.create_all()
        
        print("Clearing old data...")
        # Note: Clearing substitution_map is good practice, though it might be empty
        db.session.execute(db.text('DELETE FROM substitution_map'))
        db.session.execute(recipe_ingredients.delete())
        db.session.query(Recipe).delete()
        db.session.query(Ingredient).delete()
        db.session.commit()

        print("Seeding database from CSV...")
        
        try:
            csv_file_path = 'RecipeNLG_dataset.csv'
            f = open(csv_file_path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: Make sure '{csv_file_path}' is in your project folder.")
            return
            
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            if i >= 5000:
                print("Reached the limit of 5000 recipes for seeding.")
                break
                
            new_recipe = Recipe(
                title=row.get('title', 'No Title'),
                instructions=row.get('directions', '')
            )
            # Add the new recipe to the session early
            db.session.add(new_recipe)
            
            try:
                ingredients_list = ast.literal_eval(row.get('ingredients', '[]'))
            except (ValueError, SyntaxError):
                ingredients_list = []

            # Use set() to get only unique ingredient names
            for ingredient_name in set(ingredients_list):
                clean_name = ingredient_name.strip().lower()
                if clean_name:
                    # Pass the session to the helper function
                    ingredient_obj = get_or_create_ingredient(db.session, clean_name)
                    if ingredient_obj: # Ensure ingredient object exists
                        new_recipe.ingredients.append(ingredient_obj)
            
            if i > 0 and i % 100 == 0:
                print(f"Committing batch of 100 recipes (Total: {i})...")
                db.session.commit()
        
        f.close()
        print("Committing final batch...")
        db.session.commit()
        print("Database seeding complete!")

if __name__ == '__main__':
    seed_database()