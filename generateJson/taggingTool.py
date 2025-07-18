import json

TASKS_FILE = 'tasks.json'

def load_tasks():
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def format_answers(left, right, answers):
    return [f"{left} {ans} {right}".strip() for ans in answers]

def normalize_tag(tag):
    tag = tag.strip().lower()
    return tag.capitalize()

def main():
    tasks = load_tasks()
    modified = False

    for idx, task in enumerate(tasks):
        print("=" * 40)
        print(f"Task #: {idx + 1}")
        print(f"Original: {task.get('original', '')}\n")

        left = task.get('prompt', {}).get('left', '')
        right = task.get('prompt', {}).get('right', '')
        answers = task.get('answers', [])

        for i, formatted in enumerate(format_answers(left, right, answers)):
            print(f"Answer: {formatted}")

        # Normalize any existing tags on load
        tags = [normalize_tag(t) for t in task.get('tags', [])]
        task['tags'] = tags

        if tags:
            print(f"\nTags: {', '.join(tags)}")
        else:
            print("\nNo tags in this question")

        print("Write the tags to add or delete (x, x, x | ? to move to next question):")
        user_input = input("--> ").strip()

        while user_input != '?':
            input_tags = [normalize_tag(t) for t in user_input.split(',') if t.strip()]
            if not input_tags:
                print("No tags entered. Enter at least one tag or '?' to skip.")
            else:
                if 'tags' not in task:
                    task['tags'] = []
                # Normalize again, to be absolutely sure
                task['tags'] = [normalize_tag(t) for t in task['tags']]
                for tag in input_tags:
                    if tag in task['tags']:
                        task['tags'].remove(tag)
                        print(f"Removed tag: {tag}")
                    else:
                        task['tags'].append(tag)
                        print(f"Added tag: {tag}")
                modified = True
                print(f"Current tags: {', '.join(task['tags']) if task['tags'] else 'No tags'}")
            print("Write the tags to add or delete (comma separated, enter ? to move to next question):")
            user_input = input("> ").strip()

    if modified:
        save_tasks(tasks)
        print("\nTasks updated and saved.")
    else:
        print("\nNo changes made.")

if __name__ == "__main__":
    main()
