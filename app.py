import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# --- 1. Basic App and Database Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- 2. Database Models (All Together) ---
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

substitution_map = db.Table('substitution_map',
    db.Column('original_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('substitute_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, lazy='subquery',
        backref=db.backref('recipes', lazy=True))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    substitutes = db.relationship('Ingredient', secondary=substitution_map,
                                  primaryjoin=(id == substitution_map.c.original_id),
                                  secondaryjoin=(id == substitution_map.c.substitute_id),
                                  backref='substitute_for')


# --- 3. Upgraded Algorithm & API Routes ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

def find_best_matches(available_ingredients):
    """
    Finds recipe matches, now with support for ingredient substitutions.
    """
    available_set = set(name.lower() for name in available_ingredients)
    all_recipes = Recipe.query.all()
    
    scored_recipes = []
    for recipe in all_recipes:
        recipe_ingredients_set = {ing for ing in recipe.ingredients}
        total_ingredients_count = len(recipe_ingredients_set)
        
        if total_ingredients_count == 0:
            continue

        direct_matches = {ing for ing in recipe_ingredients_set if ing.name in available_set}
        missing_ingredients = recipe_ingredients_set - direct_matches
        
        substituted_matches = set()
        for missing_ing in missing_ingredients:
            for sub in missing_ing.substitutes:
                if sub.name in available_set:
                    substituted_matches.add(missing_ing)
                    break # Found a substitute, no need to check for others

        # Weighted score: 1.0 for direct match, 0.9 for substituted match
        score = (len(direct_matches) * 1.0 + len(substituted_matches) * 0.9) / total_ingredients_count
        
        if score > 0:
            # Convert ingredient objects back to names for the JSON response
            final_missing = [ing.name for ing in (missing_ingredients - substituted_matches)]
            
            scored_recipes.append({
                "recipe_id": recipe.id,
                "title": recipe.title,
                "score": round(score * 100, 2),
                "instructions": recipe.instructions,
                "needed_ingredients": [ing.name for ing in recipe_ingredients_set],
                "available_ingredients": [ing.name for ing in direct_matches],
                "substituted_ingredients": [ing.name for ing in substituted_matches],
                "missing_ingredients": final_missing
            })
            
    return sorted(scored_recipes, key=lambda x: x['score'], reverse=True)

@app.route('/api/search', methods=['POST'])
def search_recipes():
    """Receives ingredients and returns best recipe matches."""
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({"error": "Missing 'ingredients' in request body"}), 400
        
    available_ingredients = data['ingredients']
    if not isinstance(available_ingredients, list):
        return jsonify({"error": "'ingredients' must be a list of strings"}), 400
        
    matched_recipes = find_best_matches(available_ingredients)
    
    return jsonify(matched_recipes)


# --- 4. Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)