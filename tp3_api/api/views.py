from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection
from datetime import datetime, timedelta
import os

DATA_LAKE_PATH = "../data_lake/all_transactions"

def top_products(request):
    try:
        x = int(request.GET.get("x", 5))
    except:
        x = 5

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT product_id, COUNT(*) as total
            FROM all_transactions
            GROUP BY product_id
            ORDER BY total DESC
            LIMIT %s
        """, [x])
        rows = cursor.fetchall()

    data = [{"product_id": r[0], "total": r[1]} for r in rows]
    return JsonResponse(data, safe=False)


def total_by_user_type(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, transaction_type, SUM(amount) as total_spent
            FROM all_transactions
            GROUP BY user_id, transaction_type
        """)
        rows = cursor.fetchall()

    data = [
        {
            "user_id": row[0],
            "transaction_type": row[1],
            "total_spent": float(row[2])
        }
        for row in rows
    ]
    return JsonResponse(data, safe=False)

def money_last_5_minutes(request):
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT SUM(amount) FROM all_transactions
            WHERE STR_TO_DATE(timestamp, '%%Y-%%m-%%dT%%H:%%i:%%s.%%f') >= %s
        """, [five_minutes_ago])
        row = cursor.fetchone()

    return JsonResponse({"total_last_5_minutes": float(row[0]) if row[0] else 0.0})


def list_datalake_files(request):
    files_info = []
    for root, dirs, files in os.walk(DATA_LAKE_PATH):
        for file in files:
            files_info.append(os.path.join(root, file))
    return JsonResponse({"files": files_info})

def get_file_version(request):
    date = request.GET.get("date")
    if not date:
        return JsonResponse({"error": "Missing ?date=YYYY-MM-DD"}, status=400)

    path = os.path.join(DATA_LAKE_PATH, date, "batch.json")
    if not os.path.exists(path):
        return JsonResponse({"error": f"No data found for date {date}"}, status=404)

    with open(path, "r") as f:
        lines = f.readlines()
    
    return JsonResponse({"lines": lines})


def access_log(request):
    logs = [
        {"user": "alice", "action": "read", "file": "2025-05-17", "timestamp": datetime.now().isoformat()},
        {"user": "bob", "action": "write", "file": "2025-05-14", "timestamp": datetime.now().isoformat()}
    ]
    return JsonResponse({"access_log": logs})

def fulltext_search(request, text):
    matches = []
    print(f"Searching for '{text}' in {DATA_LAKE_PATH}")
    for root, dirs, files in os.walk(DATA_LAKE_PATH):
        print(f"Scanning directory: {root}, files: {files}")
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if text.lower() in line.lower():
                            print(f"Found match in {file_path} line {i + 1}")
                            matches.append({
                                "file": file_path,
                                "line_number": i + 1,
                                "line": line.strip()
                            })
            except Exception as e:
                print(f"Erreur lecture fichier {file_path} : {e}")
    
    return JsonResponse({"matches": matches})
