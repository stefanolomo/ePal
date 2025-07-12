import json
import hashlib
import os

TASKS_FILE = 'tasks.json'

def load_existing_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def input_with_quit(prompt):
    value = input(prompt)
    if value.strip() == '?':
        return None
    return value.strip()

def hash_left_text(text):
    return hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()

def main():
    all_tasks = load_existing_tasks()
    existing_ids = {task['id'] for task in all_tasks}

    print("=== Task Entry Tool for CAE Part 4 ===")
    print("Enter '?' at any point to stop.\n")

    while True:
        print("---- New Task ----")
        left = input_with_quit("> Left part of the task (? to end)\n> ")
        if left is None:
            break

        task_id = hash_left_text(left)

        if task_id in existing_ids:
            print("⚠️ This task already exists (duplicate left part). Skipping.\n")
            continue

        right = input("> Right part of the task\n> ").strip()
        keyword = input("> Keyword (word in capital letters)\n> ").strip()
        original = input("> Original sentence\n> ").strip()

        try:
            n = int(input("> How many correct answers are there?\n> "))
        except ValueError:
            print("Invalid number. Skipping task.")
            continue

        answers = []
        for i in range(n):
            answer = input(f"> Answer {i + 1}\n> ").strip()
            if answer:
                answers.append(answer)

        if not answers:
            print("⚠️ No valid answers provided. Skipping task.")
            continue

        tags_input = input("> Tags (comma separated)\n> ").strip()
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

        task = {
            "id": task_id,
            "original": original,
            "keyword": keyword.upper(),
            "prompt": {
                "left": left,
                "right": right
            },
            "answers": answers,
            "tags": tags
        }

        all_tasks.append(task)
        existing_ids.add(task_id)
        print("✅ Task added.\n")

    save_tasks(all_tasks)
    print(f"\nAll tasks saved to {TASKS_FILE}.")

if __name__ == "__main__":
    main()