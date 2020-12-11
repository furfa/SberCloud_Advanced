
def abiturient_key(name, surname, patronymic):
    return f"{name}{surname}{patronymic}"


def find_repeats(faculties):
    abiturients = {}

    for faculty in faculties:
        for abiturient in faculties[faculty]:
            key = abiturient_key(abiturient[0], abiturient[1], abiturient[2])
            if key not in abiturients:
                abiturients[key] = 1
            else:
                abiturients[key] += 1

    repeats = {}
    for faculty in faculties:
        repeats_here = 0
        for abiturient in faculties[faculty]:
            key = abiturient_key(abiturient[0], abiturient[1], abiturient[2])
            repeats_here += min(1, abiturients[key]-1)
        repeats[faculty] = repeats_here
    return repeats