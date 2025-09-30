from app import app, db, Ingredient

# A list of common ingredient substitutions
# Format: ('original ingredient', ['substitute 1', 'substitute 2', ...])
SUBSTITUTION_DATA = [
    ('butter', ['margarine', 'olive oil']),
    ('buttermilk', ['milk', 'yogurt']), # Note: milk + lemon is more complex, we'll keep it simple
    ('lemon juice', ['vinegar', 'lime juice']),
    ('sour cream', ['yogurt']),
    ('baking powder', ['baking soda']),
    ('flour', ['whole wheat flour']),
    ('onion', ['shallot', 'leek']),
]

def seed_subs():
    with app.app_context():
        print("Seeding ingredient substitutions...")
        
        for original_name, substitute_names in SUBSTITUTION_DATA:
            # Find the Ingredient object for the original ingredient
            original_ingredient = db.session.query(Ingredient).filter_by(name=original_name).first()

            if not original_ingredient:
                print(f"  - Skipping '{original_name}', not found in database.")
                continue

            # Find the Ingredient objects for all its substitutes
            for sub_name in substitute_names:
                substitute_ingredient = db.session.query(Ingredient).filter_by(name=sub_name).first()
                
                if substitute_ingredient:
                    # Add the relationship if it doesn't already exist
                    if substitute_ingredient not in original_ingredient.substitutes:
                        original_ingredient.substitutes.append(substitute_ingredient)
                        print(f"  - Mapped '{sub_name}' as a substitute for '{original_name}'.")
                else:
                    print(f"  - Skipping substitute '{sub_name}', not found in database.")
        
        db.session.commit()
        print("Substitution seeding complete!")

if __name__ == '__main__':
    seed_subs()
    