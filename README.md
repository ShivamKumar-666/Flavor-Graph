# 🍲 FlavorGraph: Intelligent Recipe Navigator

FlavorGraph is a full-stack web application designed to solve the common kitchen problem: "What can I make with what I have?" This project provides smart recipe suggestions based on a user's available ingredients, featuring a clean, modern frontend and a powerful Python backend that not only finds direct matches but also recommends recipes by identifying potential ingredient substitutions.



---

## ## Key Features

* **Greedy Matching Algorithm:** Quickly finds and ranks recipes with the highest percentage of available ingredients.
* **Ingredient Substitution Engine:** Intelligently suggests recipes by identifying valid substitutes for missing ingredients (e.g., using margarine instead of butter).
* **Interactive Frontend:** A modern, responsive user interface built with HTML, CSS, and JavaScript.
* **REST API Backend:** A robust backend built with **Python** and **Flask** to handle data processing and algorithmic logic.
* **Database Management:** Uses **SQLite** and **SQLAlchemy** to manage a large dataset of recipes and ingredient relationships.

---

## ## Tech Stack

* **Backend:** Python, Flask, SQLAlchemy
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Data Source:** RecipeNLG Dataset

---

## ## How It Works

The application models recipes and ingredients as a graph. When a user inputs their pantry items, a greedy algorithm calculates a "match score" for each recipe in the database. To enhance the results, the algorithm also considers valid substitutions for missing ingredients, applying a slightly lower weight for substituted matches to prioritize direct results. The final ranked list is then sent to the frontend for display.

---

## ## Getting Started

### ### Prerequisites

* Python 3.x
* pip

### ### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/flavor-graph.git](https://github.com/your-username/flavor-graph.git)
    cd flavor-graph
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install the required packages:**
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```
4.  **Set up the database:**
    * Run the main seeder to populate recipes:
        ```bash
        python seed.py
        ```
    * Run the substitution seeder to create ingredient relationships:
        ```bash
        python seed_substitutions.py
        ```
5.  **Run the application:**
    ```bash
    python app.py
    ```
    Open your browser and navigate to `http://127.0.0.1:5000`.
