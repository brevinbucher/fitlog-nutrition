#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

# ----------------- DB CONFIG ----------------- #

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASS = "SwiftBrev21!"   # <-- change this
DB_NAME = "fitlog"


# ----------------- CONNECTION HELPERS ----------------- #

def connect_no_db():
    """Connect to MySQL server without specifying a database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
    )


def connect_with_db():
    """Connect directly to the fitlog database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
    )


# ----------------- SETUP FUNCTIONS ----------------- #

def ensure_database():
    """Create the fitlog database if it does not exist."""
    conn = connect_no_db()
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    conn.commit()
    cur.close()
    conn.close()


def ensure_tables(conn):
    """Create all tables if they do not exist."""
    cur = conn.cursor()

    # data_sources
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_sources (
            data_source_id INT AUTO_INCREMENT PRIMARY KEY,
            source_name    VARCHAR(255) NOT NULL,
            source_url     VARCHAR(500)
        );
    """)

    # categories
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id   INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL
        );
    """)

    # foods
    cur.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            food_id         INT AUTO_INCREMENT PRIMARY KEY,
            food_name       VARCHAR(255) NOT NULL,
            brand_or_source VARCHAR(255),
            category_id     INT,
            data_source_id  INT,
            FOREIGN KEY (category_id)    REFERENCES categories(category_id),
            FOREIGN KEY (data_source_id) REFERENCES data_sources(data_source_id)
        );
    """)

    # nutrients
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nutrients (
            nutrient_id   INT AUTO_INCREMENT PRIMARY KEY,
            nutrient_name VARCHAR(255) NOT NULL,
            unit_name     VARCHAR(50)  NOT NULL
        );
    """)

    # food_nutrients
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_nutrients (
            food_id         INT,
            nutrient_id     INT,
            amount_per_100g DECIMAL(10,2),
            PRIMARY KEY (food_id, nutrient_id),
            FOREIGN KEY (food_id)     REFERENCES foods(food_id),
            FOREIGN KEY (nutrient_id) REFERENCES nutrients(nutrient_id)
        );
    """)

    # fastfood_restaurants
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fastfood_restaurants (
            restaurant_id   INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_name VARCHAR(255) NOT NULL
        );
    """)

    # fastfood_items
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fastfood_items (
            fastfood_item_id  INT AUTO_INCREMENT PRIMARY KEY,
            food_id           INT,
            restaurant_id     INT,
            original_item_name VARCHAR(255),
            FOREIGN KEY (food_id)       REFERENCES foods(food_id),
            FOREIGN KEY (restaurant_id) REFERENCES fastfood_restaurants(restaurant_id)
        );
    """)

    # users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       INT AUTO_INCREMENT PRIMARY KEY,
            email         VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at    DATE NOT NULL
        );
    """)

    # user_meal_logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_meal_logs (
            meal_log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id     INT NOT NULL,
            meal_date   DATE NOT NULL,
            meal_type   VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # user_meal_items
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_meal_items (
            meal_item_id   INT AUTO_INCREMENT PRIMARY KEY,
            meal_log_id    INT NOT NULL,
            food_id        INT NOT NULL,
            serving_amount DECIMAL(10,2),
            serving_unit   VARCHAR(50),
            FOREIGN KEY (meal_log_id) REFERENCES user_meal_logs(meal_log_id),
            FOREIGN KEY (food_id)     REFERENCES foods(food_id)
        );
    """)

    # user_profiles
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id      INT PRIMARY KEY,
            display_name VARCHAR(255),
            age          INT,
            height_cm    DECIMAL(5,2),
            gender       VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # user_goals
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_goals (
            goal_id      INT AUTO_INCREMENT PRIMARY KEY,
            user_id      INT NOT NULL,
            goal_type    VARCHAR(50) NOT NULL,
            target_value DECIMAL(10,2) NOT NULL,
            start_date   DATE NOT NULL,
            end_date     DATE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # user_weight_logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_weight_logs (
            weight_log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id       INT NOT NULL,
            weigh_date    DATE NOT NULL,
            weight_kg     DECIMAL(5,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # exercises
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            exercise_id   INT AUTO_INCREMENT PRIMARY KEY,
            exercise_name VARCHAR(255) NOT NULL,
            category      VARCHAR(100)
        );
    """)

    # workouts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            workout_id       INT AUTO_INCREMENT PRIMARY KEY,
            user_id          INT NOT NULL,
            workout_date     DATETIME NOT NULL,
            duration_minutes INT,
            notes            VARCHAR(500),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # workout_exercises
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workout_exercises (
            workout_exercise_id INT AUTO_INCREMENT PRIMARY KEY,
            workout_id          INT NOT NULL,
            exercise_id         INT NOT NULL,
            sets                INT,
            reps                INT,
            weight_kg           DECIMAL(5,2),
            FOREIGN KEY (workout_id) REFERENCES workouts(workout_id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
        );
    """)

    # user_daily_summaries
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_daily_summaries (
            summary_date    DATE NOT NULL,
            user_id         INT  NOT NULL,
            calories_eaten  DECIMAL(10,2),
            calories_burned DECIMAL(10,2),
            protein_grams   DECIMAL(10,2),
            PRIMARY KEY (summary_date, user_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # achievements
    cur.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INT AUTO_INCREMENT PRIMARY KEY,
            title          VARCHAR(255) NOT NULL,
            description    VARCHAR(500)
        );
    """)

    # user_achievements
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_achievements (
            user_id        INT NOT NULL,
            achievement_id INT NOT NULL,
            earned_at      DATETIME NOT NULL,
            PRIMARY KEY (user_id, achievement_id),
            FOREIGN KEY (user_id)        REFERENCES users(user_id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id)
        );
    """)

    # audit_log
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            audit_id    INT AUTO_INCREMENT PRIMARY KEY,
            user_id     INT,
            action      VARCHAR(255) NOT NULL,
            details     TEXT,
            action_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    conn.commit()
    cur.close()


def table_empty(conn, table_name: str) -> bool:
    """Return True if the given table has zero rows."""
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cur.fetchone()[0]
    cur.close()
    return count == 0


def insert_sample_data(conn):
    """Insert a few sample rows so the demo query has something to show."""
    cur = conn.cursor()

    # data_sources
    if table_empty(conn, "data_sources"):
        cur.execute("""
            INSERT INTO data_sources (source_name, source_url) VALUES
              ('Kaggle Food Nutrition Dataset',
               'https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset'),
              ('Fast Food Nutrition Dataset',
               'https://www.kaggle.com/datasets/ulrikthygepedersen/fastfood-nutrition');
        """)

    # categories
    if table_empty(conn, "categories"):
        cur.execute("""
            INSERT INTO categories (category_name) VALUES
              ('Fruit'),
              ('Fast Food');
        """)

    # nutrients
    if table_empty(conn, "nutrients"):
        cur.execute("""
            INSERT INTO nutrients (nutrient_name, unit_name) VALUES
              ('Calories', 'kcal'),
              ('Protein',  'g');
        """)

    # foods
    if table_empty(conn, "foods"):
        cur.execute("""
            INSERT INTO foods (food_name, brand_or_source, category_id, data_source_id) VALUES
              ('Apple, raw', 'USDA', 1, 1),
              ('Big Mac',    'McDonald''s', 2, 2);
        """)

    # food_nutrients
    if table_empty(conn, "food_nutrients"):
        cur.execute("""
            INSERT INTO food_nutrients (food_id, nutrient_id, amount_per_100g) VALUES
              (1, 1, 52.00),    -- Apple calories
              (1, 2, 0.26),     -- Apple protein
              (2, 1, 257.00),   -- Big Mac calories (example)
              (2, 2, 12.00);    -- Big Mac protein (example)
        """)

    # fastfood_restaurants
    if table_empty(conn, "fastfood_restaurants"):
        cur.execute("""
            INSERT INTO fastfood_restaurants (restaurant_name) VALUES
              ('McDonald''s');
        """)

    # fastfood_items
    if table_empty(conn, "fastfood_items"):
        cur.execute("""
            INSERT INTO fastfood_items (food_id, restaurant_id, original_item_name) VALUES
              (2, 1, 'Big Mac');
        """)

    # users
    if table_empty(conn, "users"):
        cur.execute("""
            INSERT INTO users (email, password_hash, created_at) VALUES
              ('test@example.com', 'fakehash', CURDATE());
        """)

    # user_meal_logs
    if table_empty(conn, "user_meal_logs"):
        cur.execute("""
            INSERT INTO user_meal_logs (user_id, meal_date, meal_type) VALUES
              (1, CURDATE(), 'lunch');
        """)

    # user_meal_items
    if table_empty(conn, "user_meal_items"):
        cur.execute("""
            INSERT INTO user_meal_items (meal_log_id, food_id, serving_amount, serving_unit) VALUES
              (1, 2, 1.00, 'sandwich'),
              (1, 1, 150.00, 'g');
        """)

    conn.commit()
    cur.close()


def show_sample_data(conn):
    """Run a sample query that joins several tables and prints output."""
    cur = conn.cursor()
    cur.execute("""
        SELECT f.food_name,
               n.nutrient_name,
               fn.amount_per_100g,
               n.unit_name
        FROM foods f
        JOIN food_nutrients fn ON f.food_id = fn.food_id
        JOIN nutrients n       ON fn.nutrient_id = n.nutrient_id
        ORDER BY f.food_name, n.nutrient_name
        LIMIT 10;
    """)

    rows = cur.fetchall()
    print("Sample foods with nutrients (per 100g):")
    for food_name, nutrient_name, amt, unit in rows:
        print(f"- {food_name}: {amt} {unit} of {nutrient_name}")

    cur.close()


# ----------------- MAIN ----------------- #

def main():
    print("Starting FitLog Nutrition demo...")

    try:
        # Make sure DB exists
        ensure_database()

        # Connect to DB
        conn = connect_with_db()
        print("Connected to database!")

        # Make sure tables + sample data exist
        ensure_tables(conn)
        insert_sample_data(conn)

        # Run a demo query
        show_sample_data(conn)

        conn.close()
        print("Connection closed.")

    except Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    main()
