import json
import random
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


# --- Modelos de Datos (Pydantic) ---
class PromptModel(BaseModel):
    left: str
    right: str


class ExerciseModel(BaseModel):
    id: str
    original: str
    keyword: str
    prompt: PromptModel
    answers: List[str]
    tags: List[str]


# --- Configuración de la Aplicación ---
app = FastAPI(
    title="API de Ejercicios de Transformación",
    description="Una API para servir ejercicios de reescritura de frases.",
    version="1.1.0",
)

try:
    with open("./data.json", "r", encoding="utf-8") as f:
        exercise_data: List[ExerciseModel] = json.load(f)
except FileNotFoundError:
    exercise_data = []


def find_exercise_by_id(exercise_id: str) -> Optional[ExerciseModel]:
    for exercise in exercise_data:
        if exercise["id"] == exercise_id:
            return ExerciseModel(**exercise)
    return None


# --- Definición de Endpoints ---


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Ejercicios"}


@app.get("/exercise", response_model=ExerciseModel, tags=["Ejercicios"])
def get_exercise_by_id(id: str = Query(..., description="El ID único del ejercicio")):
    exercise = find_exercise_by_id(id)
    if not exercise:
        raise HTTPException(
            status_code=404, detail="Ejercicio no encontrado con ese ID"
        )
    return exercise


@app.get("/exercise/by-number", response_model=ExerciseModel, tags=["Ejercicios"])
def get_exercise_by_number(
    n: int = Query(..., gt=0, description="El número del ejercicio (empezando en 1)"),
):
    index = n - 1
    if 0 <= index < len(exercise_data):
        return exercise_data[index]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Número de ejercicio fuera de rango. Hay {len(exercise_data)} ejercicios en total.",
        )


@app.get("/exercise/random", response_model=ExerciseModel, tags=["Ejercicios"])
def get_random_exercise():
    if not exercise_data:
        raise HTTPException(status_code=404, detail="No hay ejercicios disponibles")
    return random.choice(exercise_data)


# ==============================================================================
# === BLOQUE MODIFICADO ===
# ==============================================================================
# URL actualizada a plural: /exercises/
# response_model actualizado a List[ExerciseModel]
# El nombre de la función ahora es más claro: get_exercises_by_tag
@app.get("/exercises/by-tag", response_model=List[ExerciseModel], tags=["Ejercicios"])
def get_exercises_by_tag(
    tag: str = Query(..., description="La etiqueta para filtrar los ejercicios"),
):
    """
    Obtiene una lista de todos los ejercicios que contienen la etiqueta especificada.
    Si no se encuentra ninguno, devuelve una lista vacía.
    """
    # Filtra los ejercicios que contienen el tag
    filtered_exercises = [ex for ex in exercise_data if tag in ex.get("tags", [])]

    # Devuelve la lista completa (estará vacía si no hay coincidencias)
    return filtered_exercises


# ==============================================================================
# === FIN DEL BLOQUE MODIFICADO ===
# ==============================================================================


@app.get("/exercise/printable/{exercise_id}", tags=["Formato"])
def get_printable_task(exercise_id: str):
    exercise = find_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404, detail="Ejercicio no encontrado con ese ID"
        )

    printable_text = (
        f"Original: {exercise.original}\n\n"
        f"Keyword: {exercise.keyword}\n\n"
        f"{exercise.prompt.left} ... {exercise.prompt.right}"
    )

    return {"exercise_id": exercise_id, "printable_format": printable_text}
