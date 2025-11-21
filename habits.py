# ---------- hybits.py ------------
# file for cotroling habits

import json
from datetime import date, timedelta
import csv
import argparse

# ---------- save -----------
def save_data(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------- load -----------
def load_data(filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"habits": {}} # Return empty structure if file not found
    except json.JSONDecodeError:
        print("❌ Chyba při načítání dat! Soubor je poškozen.")
        return {"habits": {}}

# ---------- Add a new habit -----------
def add_habit(name, filename="data.json"):
    if not name.strip():
        print("❌ Název návyku nesmí být prázdný!")
        return
    
    data = load_data(filename)

    if name in data["habits"]:
        print(f"❌ Návyk '{name}' už existuje!")
        return
    
    data["habits"][name] = []
    save_data(data, filename)
    print(f"✅ Návyk '{name}' přidán.")

# ---------- Check in a habit -----------
def check_in(name, check_date=None, filename="data.json"):
    data = load_data(filename)
    
    if name not in data["habits"]:
        print(f"❌ Návyk '{name}' neexistuje!")
        return
    
    if check_date is None:
        check_date = date.today().isoformat()
    elif isinstance(check_date, date):
        check_date = check_date.isoformat()
    elif not isinstance(check_date, str):
        print("❌ Neplatný formát data!")
        return
    
    if check_date in data["habits"][name]:
        print(f"❌ Návyk '{name}' už byl zaznamenán pro datum {check_date}.")
        return
    
    data["habits"][name].append(check_date)
    save_data(data, filename)
    print(f"✅ Zapsáno: {name} dne {check_date}.")




# ---------- List of habits -----------
def list_habits(filename="data.json"):
    data = load_data(filename)
    
    if not data["habits"]:
        print("📭 Zatím nemáš žádné návyky.")
        return
    
    print("📋 Seznam návyků:")
    for habit in sorted(data["habits"]):
        print("-", habit)

# ---------- Stats of habits -----------
def last_7_days(dates):
    if not dates:
        return 0
    today = date.today()
    week_ago = today - timedelta(days=6)
    return sum(1 for d in dates if week_ago <= d <= today)


def last_30_days(dates):
    if not dates:
        return 0
    today = date.today()
    month_ago = today - timedelta(days=29)
    return sum(1 for d in dates if month_ago <= d <= today)    


def stats(name, filename="data.json"):
    data = load_data(filename)
    
    if name not in data["habits"]:
        print(f"❌ Návyk '{name}' neexistuje!")
        return
    
    dates = []
    for d in data["habits"][name]:
        try:
            dates.append(date.fromisoformat(d))
        except ValueError:
            print(f"❌ Neplatné datum '{d}' v návyku '{name}'!")
            return
        
    # remove duplicates and sort
    unique_dates = sorted(set(dates))

    seven_day_count = last_7_days(unique_dates)
    thirty_day_count = last_30_days(unique_dates)

    date_count = 0
    #ignot future dates
    for d in unique_dates:
        if d <= date.today():
            date_count += 1
        else:
            break

    streak = habit_streak(name, filename)

    # dict for stats
    stats_dict = {
        "name": name,
        "count": date_count,
        "7_days": seven_day_count,
        "30_days": thirty_day_count,
        "dates": [d.isoformat() for d in unique_dates],
        "streak": streak
    }

    return stats_dict

# ----------- Stats for all habits -----------
def all_stats(filename="data.json"):
    data = load_data(filename)
    all_stats_list = []
    
    for habit in sorted(data["habits"]):
        s = stats(habit, filename)
        if s:
            all_stats_list.append(s)
        
    if not all_stats_list:
        print("📭 Zatím nemáš žádné návyky.")
        return None
    
    return all_stats_list
    

# ----------- Streak line -----------
def habit_streak(name, filename="data.json"):
    data = load_data(filename)

    if name not in data["habits"]:
        print(f"❌ Návyk '{name}' neexistuje!")
        return
    
    dates = []
    for d in data["habits"][name]:
        try:
            dates.append(date.fromisoformat(d))
        except ValueError:
            print(f"❌ Neplatné datum '{d}' v návyku '{name}'!")
            return
        
    # remove duplicates and sort
    unique_dates = sorted(set(dates))
    if not unique_dates:
        return 0 # no streak if no dates
    
    streak = 0
    today = date.today()
    day_check = today
    for d in reversed(unique_dates):
        if d == day_check:
            streak += 1
            day_check -= timedelta(days=1)
        elif d < day_check:
            break # streak broken
    return streak

# ----------- Export to CSV -----------
def export_csv(filename="data.json", csv_filename="habits_export.csv"):
    data = load_data(filename)
    
    if not data["habits"]:
        print("📭 Zatím nemáš žádné návyky k exportu.")
        return
    
    with open(csv_filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(["habit", "date"])

        # Iterate over habits and their dates
        # for habit, dates in data["habits"].items():
        #     for d in dates:
        #         writer.writerow([habit, d])

        # sorted output
        for habit in sorted(data["habits"]):
            dates = sorted(data["habits"][habit])
            for d in dates:
                writer.writerow([habit, d])
                
    print(f"✅ Data exportována do '{csv_filename}'.")

# ---------- Command line interface -----------
def main():
    parser = argparse.ArgumentParser(
        description="📊 Habit Tracker – sleduj svoje návyky z příkazové řádky."
    )

    subparser = parser.add_subparsers(dest="command", required=True)

    # Add
    parser_add = subparser.add_parser("add", help="Přidat nový návyk.")
    parser_add.add_argument("name", help="Název návyku.")

    # List
    parser_list = subparser.add_parser("list", help="Vypsat všechny návyky.")

    # Check-in
    parser_checkin = subparser.add_parser("checkin", help="Zapsat návyk pro dnešní den nebo zadané datum.")
    parser_checkin.add_argument("name", help="Název návyku.")
    parser_checkin.add_argument("--date", help="Datum ve formátu RRRR-MM-DD (volitelné).")

    # Stats
    parser_stats = subparser.add_parser("stats", help="Zobrazit statistiky návyku.")
    parser_stats.add_argument("name", help="Název návyku.")

    # Stats for all habits
    parser_all_stats = subparser.add_parser("stats-all", help="Zobrazit statistiky pro všechny návyky.")
    # parser_all_stats.add_argument() # No arguments needed

    # Export
    parser_export = subparser.add_parser("export", help="Exportovat data do CSV souboru.")
    parser_export.add_argument("--output", default="habits_export.csv", help="Název výstupního CSV souboru (volitelné).")

    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        add_habit(args.name)
    elif args.command == "list":
        list_habits()
    elif args.command == "checkin":
        if args.date:
            try:
                check_date = date.fromisoformat(args.date)
            except ValueError:
                print("❌ Neplatný formát data! Použij RRRR-MM-DD.")
                return
            check_in(args.name, check_date)
        else:
            check_in(args.name)
    elif args.command == "stats":
        s = stats(args.name)
        if s:
            print(f"📊 Statistiky pro návyk '{s['name']}':")
            print(f"- Celkem zapsáno: {s['count']}")
            print(f"- Posledních 7 dní: {s['7_days']}")
            print(f"- Posledních 30 dní: {s['30_days']}")
            print(f"- Aktuální série: {s['streak']}")
            print(f"- Zapsaná data: {', '.join(s['dates']) if s['dates'] else 'Žádná data'}")
    elif args.command == "stats-all":
        all_s = all_stats()
        if all_s:
            print("📊 Statistiky pro všechny návyky:")
            for s in all_s:
                print(f"- {s['name']}: Celkem zapsáno {s['count']}, Posledních 7 dní {s['7_days']}, Posledních 30 dní {s['30_days']}, Aktuální série {s['streak']}")
        else:
            print("📭 Zatím nemáš žádné návyky.")
    elif args.command == "export":
        export_csv(csv_filename=args.output)

if __name__ == "__main__":
    main()
