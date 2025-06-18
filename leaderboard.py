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
                    data.append({
                        "username": row["username"],
                        "score": int(row["score"]),
                        "time": row["time"]
                    })
                except ValueError:
                    print(f"Skipping invalid entry for user: {row['username']}")
            return merge_sort(data)
    except FileNotFoundError:
        print("Leaderboard file not found. Creating a new one.")
        return []

def save_leaderboard(data):
    sorted_data = merge_sort(data)
    with open(LEADERBOARD_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "score", "time"])
        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)

def add_score(username, score, time):
    data = load_leaderboard()
    found = False
    for entry in data:
        if entry["username"] == username:
            
            if score > entry["score"] or (score == entry["score"] and time < entry["time"]):
                entry["score"] = score
                entry["time"] = time
            found = True
            break
    if not found:
        data.append({"username": username, "score": score, "time": time})
    save_leaderboard(data)

def display_leaderboard():
    data = load_leaderboard()
    if not data:
        print("Belum ada data di leaderboard.")
        return

    headers = ["No.", "Username", "Score", "Time (s)"]
    table_data = []
    for i, entry in enumerate(data, start=1):
        table_data.append([i, entry['username'], entry['score'], entry['time']])
    
    print("-"*52)
    print(f"|{' ' * 50}|")
    print(f"|{'LEADERBOARD':^50}|")
    print(f"|{' ' * 50}|")
    print("-"*52)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    def parse_time(t):
        try:
            parts = t.split()
            menit = int(parts[0])
            detik = int(parts[2])
            return menit * 60 + detik
        except (ValueError, IndexError):
            return 99999
    sorted_list = []
    while left and right:
        if left[0]['score'] > right[0]['score']:
            sorted_list.append(left.pop(0))
        elif left[0]['score'] < right[0]['score']:
            sorted_list.append(right.pop(0))
        else:
            # ini buat ngitung kalo scorenya seri baru diliat waktu yang lebih kecil siapa
            if parse_time(left[0]["time"]) < parse_time(right[0]["time"]):
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
    sorted_list.extend(left or right)
    return sorted_list

def cari_binary(data, target):
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        username = data[mid]["username"]
        if username == target:
            return data[mid]
        elif username < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


def cari_username(target):
    data = load_leaderboard()
    
    data_sorted = sorted(data, key=lambda x: x["username"])
    result = cari_binary(data_sorted, target)
    if result:
        print("\n=== Hasil Pencarian Username ===")
        print(f"Username : {result['username']}")
        print(f"Score    : {result['score']}")
        print(f"Time     : {result['time']}")
    else:
        print(f"\nUsername '{target}' tidak ditemukan dalam leaderboard.")
