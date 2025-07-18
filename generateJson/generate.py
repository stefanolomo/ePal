import os
import json
import hashlib

TASKS_FILE = 'tasks.json'
SPECIAL_COMMAND = "xx"

def load_existing_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def input_with_quit(prompt, left_text=None, allow_paste=False):
    value = input(prompt)
    if value.strip() == '?':
        return None
    if allow_paste and left_text:
        value = value.replace(SPECIAL_COMMAND, left_text)
    return value.strip()

def hash_left_text(text):
    return hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()

def get_answer_count():
    while True:
        n_input = input("> How many correct answers will each task have? (default = 1)\n> ").strip()
        if n_input == '':
            return 1
        try:
            n = int(n_input)
            if n >= 1:
                return n
            else:
                print("⚠️ Number must be at least 1.")
        except ValueError:
            print("⚠️ Invalid number. Try again.")

def main():
    all_tasks = load_existing_tasks()
    existing_ids = {task['id'] for task in all_tasks}

    print("=== Task Entry Tool for CAE Part 4 ===")
    print("Enter '?' at any point to stop.")
    print(f"Type '{SPECIAL_COMMAND}' inside any field to insert the current LEFT part.\n")

    answer_count = get_answer_count()
    print(f"🛠️  Using {answer_count} answer(s) per task.\n")

    while True:
        print("---- New Task ----")
        original = input_with_quit("> Original sentence (? to end)\n> ")
        if original is None:
            break

        keyword = input_with_quit("> Keyword (word in capital letters)\n> ")
        left = input_with_quit("> Left part of the task\n> ")
        if left is None:
            break

        task_id = hash_left_text(left)
        if task_id in existing_ids:
            print("⚠️ This task already exists (duplicate left part). Skipping.\n")
            continue

        answers = []
        for i in range(answer_count):
            label = "> Answer\n> " if answer_count == 1 else f"> Answer {i + 1}\n> "
            answer = input_with_quit(label, left_text=left, allow_paste=True)
            if answer:
                answers.append(answer)

        if not answers:
            print("⚠️ No valid answers provided. Skipping task.")
            continue

        right = input_with_quit("> Right part of the task\n> ", left_text=left, allow_paste=True)

        task = {
            "id": task_id,
            "original": original,
            "keyword": keyword.upper(),
            "prompt": {
                "left": left,
                "right": right
            },
            "answers": answers
        }

        all_tasks.append(task)
        existing_ids.add(task_id)
        print("✅ Task added.\n")

    save_tasks(all_tasks)
    print(f"\nAll tasks saved to {TASKS_FILE}.")

if __name__ == "__main__":
    main()
