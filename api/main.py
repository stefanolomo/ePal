import json
import random
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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


app = FastAPI(
    title="API de Ejercicios de Transformación",
    version="1.1.0",
)

# En producción cambia "*" por tu dominio
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Ejercicios"}


@app.get("/exercises", response_model=List[ExerciseModel])
def get_all_exercises():
    return exercise_data


@app.get("/exercise", response_model=ExerciseModel)
def get_exercise_by_id(id: str = Query(...)):
    exercise = find_exercise_by_id(id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return exercise


@app.get("/exercise/by-number", response_model=ExerciseModel)
def get_exercise_by_number(n: int = Query(..., gt=0)):
    index = n - 1
    if 0 <= index < len(exercise_data):
        return exercise_data[index]
    raise HTTPException(status_code=404, detail="Número de ejercicio fuera de rango")


@app.get("/exercise/random", response_model=ExerciseModel)
def get_random_exercise():
    if not exercise_data:
        raise HTTPException(status_code=404, detail="No hay ejercicios disponibles")
    return random.choice(exercise_data)


@app.get("/exercises/by-tag", response_model=List[ExerciseModel])
def get_exercises_by_tag(tag: str = Query(...)):
    return [ex for ex in exercise_data if tag in ex.get("tags", [])]


@app.get("/exercise/printable/{exercise_id}")
def get_printable_task(exercise_id: str):
    exercise = find_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    printable_text = (
        f"Original: {exercise.original}\n\n"
        f"Keyword: {exercise.keyword}\n\n"
        f"{exercise.prompt.left} ... {exercise.prompt.right}"
    )

    return {"exercise_id": exercise_id, "printable_format": printable_text}
