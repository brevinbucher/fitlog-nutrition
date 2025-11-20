import mysql.connector

def main():
    print("Starting FitLog Checkpoint 1 demo...")

    # ---- Connect to MySQL ----
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SwiftBrev21!",
            database="fitlog"
        )
        print("Connected to database!")

        cursor = conn.cursor()

        # ---- Simple Test Query ----
        cursor.execute("SELECT 'FitLog is running!' AS message;")
        result = cursor.fetchone()
        print(result[0])

        conn.close()
        print("Connection closed.")

    except mysql.connector.Error as e:
        print("Error connecting to database:", e)

if __name__ == "__main__":
    main()
