import json
import hashlib

TASKS_FILE = 'tasks.json'

def hash_original_text(text):
    return hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()

def main():
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    updated_count = 0
    for task in tasks:
        original = task.get('original', '')
        if original:
            new_id = hash_original_text(original)
            if task.get('id') != new_id:
                task['id'] = new_id
                updated_count += 1

    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated_count} tasks with new id based on original sentence.")

if __name__ == "__main__":
    main()
