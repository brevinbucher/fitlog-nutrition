import mysql.connector
from mysql.connector import Error
from datetime import date

#DB CONFIG

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASS = "SwiftBrev21!"   # <-- change if needed
DB_NAME = "fitlog"


#CONNECTION HELPERS

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


#SETUP FUNCTIONS

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

    # countries
    cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            country_id   INT AUTO_INCREMENT PRIMARY KEY,
            country_name VARCHAR(255) NOT NULL,
            iso_code     CHAR(3)
        );
    """)

    # country_nutrition_stats
    cur.execute("""
        CREATE TABLE IF NOT EXISTS country_nutrition_stats (
            stat_id        INT AUTO_INCREMENT PRIMARY KEY,
            country_id     INT NOT NULL,
            year           INT NOT NULL,
            obesity_rate   DECIMAL(5,2),
            diabetes_rate  DECIMAL(5,2),
            data_source_id INT,
            FOREIGN KEY (country_id)     REFERENCES countries(country_id),
            FOREIGN KEY (data_source_id) REFERENCES data_sources(data_source_id)
        );
    """)

    # roles
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id   INT AUTO_INCREMENT PRIMARY KEY,
            role_name VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    # permissions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS permissions (
            permission_id   INT AUTO_INCREMENT PRIMARY KEY,
            permission_name VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    # role_permissions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id       INT NOT NULL,
            permission_id INT NOT NULL,
            PRIMARY KEY (role_id, permission_id),
            FOREIGN KEY (role_id)       REFERENCES roles(role_id),
            FOREIGN KEY (permission_id) REFERENCES permissions(permission_id)
        );
    """)

    # user_roles
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INT NOT NULL,
            role_id INT NOT NULL,
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        );
    """)

    # food_tags
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_tags (
            tag_id   INT AUTO_INCREMENT PRIMARY KEY,
            tag_name VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    # food_tag_map
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_tag_map (
            food_id INT NOT NULL,
            tag_id  INT NOT NULL,
            PRIMARY KEY (food_id, tag_id),
            FOREIGN KEY (food_id) REFERENCES foods(food_id),
            FOREIGN KEY (tag_id)  REFERENCES food_tags(tag_id)
        );
    """)

    # user_favorite_foods
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_favorite_foods (
            user_id INT NOT NULL,
            food_id INT NOT NULL,
            PRIMARY KEY (user_id, food_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (food_id) REFERENCES foods(food_id)
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
    """
    Sample data seeding (currently NOT called from main).
    You already inserted your own sample data via SQL, so this
    function is kept only for reference.
    """
    cur = conn.cursor()

    if table_empty(conn, "roles"):
        cur.execute("""
            INSERT INTO roles (role_name) VALUES
              ('user'),
              ('admin');
        """)

    if table_empty(conn, "permissions"):
        cur.execute("""
            INSERT INTO permissions (permission_name) VALUES
              ('log_meal'),
              ('view_analytics'),
              ('manage_users');
        """)

    if table_empty(conn, "role_permissions"):
        cur.execute("""
            INSERT INTO role_permissions (role_id, permission_id)
            SELECT r.role_id, p.permission_id
            FROM roles r, permissions p
            WHERE r.role_name = 'user'
              AND p.permission_name IN ('log_meal', 'view_analytics');
        """)
        cur.execute("""
            INSERT INTO role_permissions (role_id, permission_id)
            SELECT r.role_id, p.permission_id
            FROM roles r, permissions p
            WHERE r.role_name = 'admin';
        """)

    if table_empty(conn, "food_tags"):
        cur.execute("""
            INSERT INTO food_tags (tag_name) VALUES
              ('high_protein'),
              ('high_calorie'),
              ('healthy');
        """)

    conn.commit()
    cur.close()


#AUDIT & ANALYTICS HELPERS
def log_action(conn, user_id, action, details):
    """Insert an audit log entry."""
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO audit_log (user_id, action, details)
        VALUES (%s, %s, %s);
    """, (user_id, action, details))
    conn.commit()
    cur.close()

def show_weight_history(conn, user_id):
    """Analytical View: Show user's weight history ordered by date."""
    cur = conn.cursor()
    cur.execute("""
        SELECT weigh_date, weight_kg
        FROM user_weight_logs
        WHERE user_id = %s
        ORDER BY weigh_date DESC
        LIMIT 30;
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("\nNo weight entries logged yet.\n")
        return

    print("\n--- Weight History (latest first) ---")
    prev = None
    for d, w in rows:
        line = f"{d}: {w:.1f} kg"
        if prev is not None:
            diff = w - prev
            if diff > 0:
                line += f"  (+{diff:.1f})"
            elif diff < 0:
                line += f"  ({diff:.1f})"
        print(line)
        prev = w
    print()


def show_sample_data(conn):
    """Analytical view #1: foods with nutrients (per 100g)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT f.food_name,
               n.nutrient_name,
               fn.amount_per_100g,
               n.unit_name
        FROM foods f
        JOIN food_nutrients fn ON f.food_id = fn.food_id
        JOIN nutrients n       ON fn.nutrient_id = n.nutrient_id
        ORDER BY f.food_id, n.nutrient_name
        LIMIT 20;
    """)

    rows = cur.fetchall()
    print("\nSample foods with nutrients (per 100g):")
    for food_name, nutrient_name, amt, unit in rows:
        print(f"- {food_name}: {amt:.2f} {unit} of {nutrient_name}")

    cur.close()


def show_user_daily_summary(conn, user_id):
    """
    Analytical view #2: total calories and protein for a given user on a given date.
    Assumes:
      - serving_amount is in grams when serving_unit = 'g'
      - food_nutrients.amount_per_100g is per 100g of food
    """
    cur = conn.cursor()

    date_str = input(
        "\nEnter date for summary (YYYY-MM-DD) or press Enter for today: "
    ).strip()
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    query = """
        SELECT
            uml.meal_date,
            SUM(
                CASE
                    WHEN n.nutrient_name = 'Calories'
                    THEN fn.amount_per_100g * (umi.serving_amount / 100.0)
                    ELSE 0
                END
            ) AS total_calories,
            SUM(
                CASE
                    WHEN n.nutrient_name = 'Protein'
                    THEN fn.amount_per_100g * (umi.serving_amount / 100.0)
                    ELSE 0
                END
            ) AS total_protein
        FROM user_meal_logs uml
        JOIN user_meal_items umi ON uml.meal_log_id = umi.meal_log_id
        JOIN foods f             ON umi.food_id = f.food_id
        JOIN food_nutrients fn   ON f.food_id = fn.food_id
        JOIN nutrients n         ON fn.nutrient_id = n.nutrient_id
        WHERE uml.user_id = %s
          AND uml.meal_date = %s
        GROUP BY uml.meal_date;
    """

    cur.execute(query, (user_id, date_str))
    row = cur.fetchone()
    cur.close()

    if row:
        day, total_cal, total_protein = row
        print(f"\nDaily summary for user {user_id} on {day}:")
        print(f"  Calories: {float(total_cal):.1f} kcal")
        print(f"  Protein:  {float(total_protein):.1f} g\n")
    else:
        print(f"\nNo logged meals for user {user_id} on {date_str}.\n")


def show_top_calorie_foods(conn):
    """Analytical view #3: Top 5 highest-calorie foods per 100g."""
    cur = conn.cursor()
    cur.execute("""
        SELECT f.food_name, fn.amount_per_100g AS kcal_100g
        FROM foods f
        JOIN food_nutrients fn ON f.food_id = fn.food_id
        JOIN nutrients n       ON fn.nutrient_id = n.nutrient_id
        WHERE n.nutrient_name = 'Calories'
        ORDER BY fn.amount_per_100g DESC
        LIMIT 5;
    """)
    rows = cur.fetchall()
    print("\nTop 5 highest-calorie foods (per 100g):")
    for name, kcal in rows:
        print(f"- {name}: {float(kcal):.1f} kcal / 100g")
    print()
    cur.close()


def show_global_obesity_stats(conn):
    """Analytical view #4: list countries by obesity rate using the country dataset."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.country_name, s.obesity_rate
        FROM country_nutrition_stats s
        JOIN countries c ON s.country_id = c.country_id
        ORDER BY s.obesity_rate DESC;
    """)
    rows = cur.fetchall()
    cur.close()

    if not rows:
        print("\nNo country nutrition stats found.\n")
        return

    print("\nGlobal obesity statistics (highest to lowest):")
    for name, rate in rows:
        print(f"- {name}: {float(rate):.1f}%")
    print()


#AUTH & INTERACTIVE WRITE ACTIONS

def login_or_signup(conn):
    """Basic access control: login or create an account."""
    cur = conn.cursor()

    print("\n--- Login / Signup ---")
    email = input("Email: ").strip()

    cur.execute("SELECT user_id, password_hash FROM users WHERE email = %s;", (email,))
    row = cur.fetchone()

    if row:
        user_id, stored_pw = row
        pw = input("Password: ").strip()
        if pw != stored_pw:
            print("Invalid password.")
            cur.close()
            return None
        print(f"Welcome back, {email} (user_id={user_id})")
        log_action(conn, user_id, "login", "User logged in")
        cur.close()
        return user_id
    else:
        print("No account found. Creating a new one.")
        pw = input("Choose a password: ").strip()
        cur.execute("""
            INSERT INTO users (email, password_hash, created_at)
            VALUES (%s, %s, CURDATE());
        """, (email, pw))
        user_id = cur.lastrowid
        conn.commit()
        log_action(conn, user_id, "signup", "New account created")
        print(f"Account created, user_id={user_id}")
        cur.close()
        return user_id


def log_meal(conn, user_id):
    """Write action: create a meal and add items."""
    print("\n--- Log a Meal ---")
    date_str = input("Meal date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")
    meal_type = input("Meal type (breakfast/lunch/dinner/snack): ").strip().lower()
    if meal_type not in ("breakfast", "lunch", "dinner", "snack"):
        meal_type = "lunch"

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_meal_logs (user_id, meal_date, meal_type)
        VALUES (%s, %s, %s);
    """, (user_id, date_str, meal_type))
    meal_log_id = cur.lastrowid
    conn.commit()
    cur.close()

    while True:
        print("\nAvailable foods:")
        cur = conn.cursor()
        cur.execute("SELECT food_id, food_name FROM foods ORDER BY food_id LIMIT 50;")
        rows = cur.fetchall()
        for fid, name in rows:
            print(f"  {fid}: {name}")
        cur.close()

        choice = input("Enter food_id to add (or 'done'): ").strip()
        if choice.lower() == "done":
            break
        try:
            food_id = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        amount_str = input("Amount in grams (e.g. 100): ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Please enter a valid number.")
            continue

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_meal_items (meal_log_id, food_id, serving_amount, serving_unit)
            VALUES (%s, %s, %s, 'g');
        """, (meal_log_id, food_id, amount))
        conn.commit()
        cur.close()
        print("Added item.")

    log_action(conn, user_id, "log_meal", f"Logged meal {meal_log_id} on {date_str}")
    print("Meal logged!\n")


def log_weight(conn, user_id):
    """Write action: log a new weight entry."""
    print("\n--- Log Weight ---")
    date_str = input("Weigh date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    weight_str = input("Weight in kg (e.g. 75.5): ").strip()
    try:
        weight_kg = float(weight_str)
    except ValueError:
        print("Invalid number, cancelling.")
        return

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_weight_logs (user_id, weigh_date, weight_kg)
        VALUES (%s, %s, %s);
    """, (user_id, date_str, weight_kg))
    conn.commit()
    cur.close()

    log_action(conn, user_id, "log_weight", f"Logged weight {weight_kg} kg on {date_str}")
    print("Weight logged!\n")


#MAIN MENU

def main():
    print("Starting FitLog Nutrition app...")

    try:
        # Make sure DB exists
        ensure_database()

        # Connect to DB
        conn = connect_with_db()
        print("Connected to database!")

        # Make sure all tables exist
        ensure_tables(conn)

        # Login / signup
        user_id = login_or_signup(conn)
        if not user_id:
            print("Exiting (auth failed).")
            conn.close()
            return

        # Main interactive loop
        while True:
            print("1) Log a meal")
            print("2) Log weight")
            print("3) View daily nutrition summary")
            print("4) View sample foods + nutrients")
            print("5) View top 5 high-calorie foods")
            print("6) View global obesity statistics")
            print("7) View weight history")
            print("0) Quit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                log_meal(conn, user_id)
            elif choice == "2":
                log_weight(conn, user_id)
            elif choice == "3":
                show_user_daily_summary(conn, user_id)
            elif choice == "4":
                show_sample_data(conn)
            elif choice == "5":
                show_top_calorie_foods(conn)
            elif choice == "6":
                show_global_obesity_stats(conn)
            elif choice == "7":
                show_weight_history(conn, user_id)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

        conn.close()
        print("Connection closed. Goodbye!")

    except Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    main()
