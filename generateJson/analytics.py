import json
import sys
from collections import Counter
import statistics

def analizar_tasks(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    total_tasks = len(tasks)
    keywords = [task.get("keyword", "").strip().upper() for task in tasks]
    tags = [tag for task in tasks for tag in task.get("tags", [])]
    respuestas_cant = [len(task.get("answers", [])) for task in tasks]
    longitudes_origen = [len(task.get("original", "").split()) for task in tasks]

    keyword_counts = Counter(keywords)
    tag_counts = Counter(tags)

    print(f"Total de tareas: {total_tasks}")
    print(f"Keywords distintos ({len(keyword_counts)}):")
    for k, c in keyword_counts.most_common():
        print(f"  {k}: {c}")

    print(f"\nTags distintos ({len(tag_counts)}):")
    for t, c in tag_counts.most_common():
        print(f"  {t}: {c}")

    print(f"\nPromedio de respuestas por tarea: {statistics.mean(respuestas_cant):.2f}")
    print(f"Longitud original (palabras):")
    print(f"  Mínima: {min(longitudes_origen)}")
    print(f"  Máxima: {max(longitudes_origen)}")
    print(f"  Promedio: {statistics.mean(longitudes_origen):.2f}")
    print(f"  Mediana: {statistics.median(longitudes_origen)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 analytics.py ruta_a_tasks.json")
        sys.exit(1)

    ruta_json = sys.argv[1]
    analizar_tasks(ruta_json)
