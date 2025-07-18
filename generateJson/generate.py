import os
import json
import hashlib
import time
from datetime import datetime

TASKS_FILE = 'tasks.json'
DETAILS_LOG = 'details.log'

def load_existing_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def input_with_quit(prompt, record_time=False, timings=None):
    value = ''
    if not record_time:
        value = input(prompt)
    else:
        print(prompt, end="", flush=True)
        start = time.time()
        value = input()
        end = time.time()
        if timings is not None:
            timings.append(end - start)

    if value.strip() == '?':
        return None
    return value.strip()

def hash_original_text(text):
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

def append_to_details_log(entries, avg_time):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(DETAILS_LOG, 'a', encoding='utf-8') as f:
        f.write(f"Created {entries} entries at {now}. Average time per entry: {avg_time:.2f} (seconds)\n")

def main():
    all_tasks = load_existing_tasks()

    print("=== Task Entry Tool for CAE Part 4 ===")
    print("Enter '?' at any point to stop.\n")

    answer_count = get_answer_count()
    print(f"🛠️  Using {answer_count} answer(s) per task.\n")

    timings = []
    entry_count = 0

    while True:
        print("---- New Task ----")
        original = input_with_quit("> Original sentence (? to end)\n> ", record_time=True, timings=timings)
        if original is None:
            break

        keyword = input_with_quit("> Keyword (word in capital letters)\n> ", record_time=True, timings=timings)
        left = input_with_quit("> Left part of the task\n> ", record_time=True, timings=timings)
        if left is None:
            break

        task_id = hash_original_text(original)

        answers = []
        for i in range(answer_count):
            label = "> Answer\n> " if answer_count == 1 else f"> Answer {i + 1}\n> "
            answer = input_with_quit(label, record_time=True, timings=timings)
            if answer:
                answers.append(answer)

        if not answers:
            print("⚠️ No valid answers provided. Skipping task.")
            continue

        right = input_with_quit("> Right part of the task\n> ", record_time=True, timings=timings)

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
        entry_count += 1
        print("✅ Task added.\n")

    save_tasks(all_tasks)
    if entry_count > 0 and len(timings) > 0:
        avg_time = sum(timings[-(entry_count* (3 + answer_count)):]) / (entry_count * (3 + answer_count))
        print(f"\nAverage time per entry: {avg_time:.2f} seconds")
        append_to_details_log(entry_count, avg_time)
    print(f"\nAll tasks saved to {TASKS_FILE}.")

if __name__ == "__main__":
    main()
