CREATE DATABASE fitlog;

USE fitlog;

CREATE TABLE test_message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    msg TEXT
);

INSERT INTO test_message (msg)
VALUES ('Hello from MySQL!');







CREATE DATABASE IF NOT EXISTS fitlog;
USE fitlog;

-- 1. data_sources
CREATE TABLE data_sources (
    data_source_id INT AUTO_INCREMENT PRIMARY KEY,
    source_name    VARCHAR(255) NOT NULL,
    source_url     VARCHAR(500)
);

-- 2. categories
CREATE TABLE categories (
    category_id   INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

-- 3. foods
CREATE TABLE foods (
    food_id         INT AUTO_INCREMENT PRIMARY KEY,
    food_name       VARCHAR(255) NOT NULL,
    brand_or_source VARCHAR(255),
    category_id     INT,
    data_source_id  INT,
    FOREIGN KEY (category_id)    REFERENCES categories(category_id),
    FOREIGN KEY (data_source_id) REFERENCES data_sources(data_source_id)
);

-- 4. nutrients
CREATE TABLE nutrients (
    nutrient_id   INT AUTO_INCREMENT PRIMARY KEY,
    nutrient_name VARCHAR(255) NOT NULL,
    unit_name     VARCHAR(50)  NOT NULL
);

-- 5. food_nutrients (bridge)
CREATE TABLE food_nutrients (
    food_id        INT,
    nutrient_id    INT,
    amount_per_100g DECIMAL(10,2),
    PRIMARY KEY (food_id, nutrient_id),
    FOREIGN KEY (food_id)     REFERENCES foods(food_id),
    FOREIGN KEY (nutrient_id) REFERENCES nutrients(nutrient_id)
);

-- 6. fastfood_restaurants
CREATE TABLE fastfood_restaurants (
    restaurant_id   INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_name VARCHAR(255) NOT NULL
);

-- 7. fastfood_items
CREATE TABLE fastfood_items (
    fastfood_item_id INT AUTO_INCREMENT PRIMARY KEY,
    food_id          INT,
    restaurant_id    INT,
    original_item_name VARCHAR(255),
    FOREIGN KEY (food_id)       REFERENCES foods(food_id),
    FOREIGN KEY (restaurant_id) REFERENCES fastfood_restaurants(restaurant_id)
);

-- 8. users
CREATE TABLE users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(255) NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    created_at     DATE NOT NULL
);

-- 9. user_meal_logs
CREATE TABLE user_meal_logs (
    meal_log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    meal_date   DATE NOT NULL,
    meal_type   VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 10. user_meal_items
CREATE TABLE user_meal_items (
    meal_item_id   INT AUTO_INCREMENT PRIMARY KEY,
    meal_log_id    INT NOT NULL,
    food_id        INT NOT NULL,
    serving_amount DECIMAL(10,2),
    serving_unit   VARCHAR(50),
    FOREIGN KEY (meal_log_id) REFERENCES user_meal_logs(meal_log_id),
    FOREIGN KEY (food_id)     REFERENCES foods(food_id)
);













USE fitlog;

INSERT INTO data_sources (source_name, source_url) VALUES
  ('Kaggle Food Nutrition Dataset', 'https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset'),
  ('Fast Food Nutrition Dataset', 'https://www.kaggle.com/datasets/ulrikthygepedersen/fastfood-nutrition');

INSERT INTO categories (category_name) VALUES
  ('Fruit'), ('Fast Food');

INSERT INTO nutrients (nutrient_name, unit_name) VALUES
  ('Calories', 'kcal'),
  ('Protein', 'g');

INSERT INTO foods (food_name, brand_or_source, category_id, data_source_id) VALUES
  ('Apple, raw', 'USDA', 1, 1),
  ('Big Mac', 'McDonald''s', 2, 2);

INSERT INTO food_nutrients (food_id, nutrient_id, amount_per_100g) VALUES
  (1, 1, 52.00),   -- Apple calories
  (1, 2, 0.26),    -- Apple protein
  (2, 1, 257.00),  -- Big Mac calories (example number)
  (2, 2, 12.00);   -- Big Mac protein (example number)

















