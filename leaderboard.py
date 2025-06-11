# leaderboard.py
import csv
import os
from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(BASE_DIR, 'db', 'leaderboard.csv')

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                try:
                    data.append({"username": row["username"], "score": int(row["score"])})
                except ValueError:
                    print(f"Skipping invalid score entry for user: {row['username']}")
            return sorted(data, key=lambda x: x["score"], reverse=True)
    except FileNotFoundError:
        print("Leaderboard file not found. Creating a new one.")
        return []
    except csv.Error as e:
        print(f"Error reading leaderboard file: {e}")
        return []

def save_leaderboard(data):
    sorted_data = sorted(data, key=lambda x: x["score"], reverse=True)
    with open(LEADERBOARD_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "score"])
        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)

def add_score(username, score):
    data = load_leaderboard()
    found = False
    for entry in data:
        if entry['username'] == username:
            entry['score'] = max(entry['score'], score)
            found = True
            break
    if not found:
        data.append({"username": username, "score": score})
    save_leaderboard(data)

def display_leaderboard():
    data = load_leaderboard()
    if not data:
        print("Belum ada data di leaderboard.")
        return

    headers = ["No.", "Username", "Score"]
    table_data = []
    for i, entry in enumerate(data, start=1):
        table_data.append([i, entry['username'], entry['score']])

    print("\n=== Leaderboard ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))