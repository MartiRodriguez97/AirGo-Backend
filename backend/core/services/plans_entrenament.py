from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Exercici, SensacioExercici


def create_ini_plan(usuari, pla):
    templates_ini = pla.templates.all()

    if not templates_ini.exists():
        return []

    total_entrenamientos = 6
    ejercicios_creados = []

    # 3. Creación cíclica
    for i in range(total_entrenamientos):
        template = templates_ini[i % templates_ini.count()]

        # 3. Calculamos la fecha específica para este ejercicio
        fecha_ejercicio = fecha_inicio_plan + timedelta(days=dias_relativos[i])

        # 4. Generar ejercicio
        nuevo_ejercicio = Exercici.objects.create(
            usuari=usuari,
            template = template,
            distance_meters=0.0,
            duration_seconds=0,
            avg_speed_kmh=0.0,
            route_points=[],
            dataIni = fecha_ejercicio,
            sensacio=SensacioExercici.NORMAL,
            comentari_sensacio=""
        )
        ejercicios_creados.append(nuevo_ejercicio)

    # Actualizamos los datos del plan
    pla.diesDurada = 14
    pla.numEntrenamentsSetmanals = 3
    pla.save()
    usuari.plans.add(pla)

    return ejercicios_creados

def create_plan(usuari, pla):
    templates = pla.templates.all()
    if not templates.exists():
        return []

    # Determinamos cuántos ejercicios crear según dificultad
    if usuari.dificultatPla == "REL":
        num_ejercicios = 6
    elif usuari.dificultatPla == "NOR":
        num_ejercicios = 9
    else:
        num_ejercicios = 12

    ejercicios_creados = []

    for i in range(num_ejercicios):
        template = templates[i % templates.count()]


    # 3. Creación cíclica
    for i in range(len(dias_relativos)):
        # TODO: filtrar por nombre del template cada iteracion para tener diferentes tipos de ejercicios
        template = templates[i]

        # 3. Calculamos la fecha específica para este ejercicio
        fecha_ejercicio = fecha_inicio_plan + timedelta(days=dias_relativos[i])

        # 4. Generar ejercicio
        nuevo_ejercicio = Exercici.objects.create(
            usuari=usuari,
            template = template,
            distance_meters=0.0,
            duration_seconds=0,
            avg_speed_kmh=0.0,
            route_points=[],
            dataIni = fecha_ejercicio,
            sensacio=SensacioExercici.NORMAL,
            comentari_sensacio=""
        )
        ejercicios_creados.append(nuevo_ejercicio)

    pla.diesDurada = 21
    pla.save()
    pla.numEntrenamentsSetmanals = num_ejercicios // 3
    usuari.plans.add(pla)

    return ejercicios_creados