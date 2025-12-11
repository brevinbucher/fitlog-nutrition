# FitLog  
A Nutrition, Fitness, and Health Tracking Application  
Developer: Brevin Bucher  
Course: CS 3620 – Database Systems  

## Overview  
FitLog is a nutrition and fitness logging application that integrates real-world nutrition data, fast-food nutrition data, and global health datasets to deliver an interactive and analytics-driven experience.

Users can:
- Create an account  
- Log meals from real datasets  
- Track calories and protein intake  
- Log weight entries  
- View weight history and trends  
- View daily nutrition summaries  
- Explore top high-calorie foods  
- Analyze global obesity statistics from a public dataset  

## Core Features  

### User Accounts
- Sign up and login  
- Secure password storage  
- Access control for all actions  

### Nutrition Logging
- Search and select foods from real datasets  
- Enter serving amounts  
- Automatic calorie + protein calculation  

### Weight Tracking
- Log weight for today or any date  
- View historical weight with gain/loss trends  

### Daily Nutrition Summary
- Total calories consumed  
- Total protein consumed  
- Aggregated from meal logs  

### Analytical Views
1. Daily nutrition summary  
2. Top 5 highest-calorie foods  
3. Global obesity statistics (public dataset)  
4. Weight history and trend analysis  

## Public Datasets Used  
FitLog uses three public datasets:

1) Kaggle Food Nutrition Dataset  
https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset  

2) Kaggle Fast Food Nutrition Dataset  
https://www.kaggle.com/datasets/ulrikthygepedersen/fastfood-nutrition  

3) World Bank Global Health & Nutrition Dataset  
https://data.worldbank.org  

These datasets populate:  
foods, nutrients, categories, fastfood_restaurants, fastfood_items, countries, country_nutrition_stats, and data_sources.

## Database Design  
FitLog uses 30 normalized tables including:

### Core Tables
- users  
- user_profiles  
- user_meal_logs  
- user_meal_items  
- user_weight_logs  

### Nutrition Dataset Tables
- foods  
- nutrients  
- food_nutrients  
- categories  

### Fast Food Dataset Tables
- fastfood_restaurants  
- fastfood_items  

### Global Health Dataset Tables
- countries  
- country_nutrition_stats  

### Analytics / Supporting Tables
- user_daily_summaries  
- achievements  
- user_achievements  
- audit_log  

All tables use primary keys, foreign keys, NOT NULL constraints, and 3NF design.

## ER Diagram
<img width="1818" height="654" alt="image" src="https://github.com/user-attachments/assets/a47dab27-b479-4120-83e0-c271820cc12b" />

## How to Run the Application  

### 1. Install dependencies
pip install mysql-connector-python

### 2. Configure database in app.py
DB_HOST = "127.0.0.1"  
DB_USER = "root"  
DB_PASS = "your_mysql_password"  
DB_NAME = "fitlog"  

### 3. Run the application
python app.py

The app will:
- Create the database (if needed)  
- Create all tables  
- Insert sample data  
- Launch an interactive menu  

## Sample Main Menu
1) Log a meal  
2) Log weight  
3) View daily nutrition summary  
4) View sample foods + nutrients  
5) View top 5 high-calorie foods  
6) View global obesity statistics  
7) View weight history  
0) Quit  

## Demo Video  
[https://youtu.be/bVsqzI2bNes ](https://youtu.be/bVsqzI2bNes) 

## Author  
Brevin Bucher  
Ohio University  
Computer Science — CS 3620
