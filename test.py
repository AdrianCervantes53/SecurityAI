"""
def ajustar_diccionario(positions, events):
    keys_to_remove = []
    for key, value in positions.items():
        if value["tipo"] == "":
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        if key != str(len(positions) - 1):  # Evitar IndexError en el último elemento
            for i in range(int(key), len(positions) - 1):
                positions[str(i)]["tipo"] = positions[str(i + 1)]["tipo"]
                positions[str(i)]["id"] = positions[str(i + 1)]["id"]
                events[str(i)] = events[str(i + 1)]
            positions[str(len(positions) - 1)]["tipo"] = ""
            positions[str(len(positions) - 1)]["id"] = ""
            events[str(len(events) - 1)] = ""
    return positions, events

# Ejemplo de uso:

events = {
            "0": "e0",
            "1": "e1",
            "2": "e2",
            "3": "e3"
        }

positions["1"]["tipo"] = ""

positions_modificado, eventishos = ajustar_diccionario(positions, events)
print(positions_modificado) 
print(eventishos)

positions["1"]["tipo"] = ""
positions_modificado, eventishos = ajustar_diccionario(positions, events)
print(positions_modificado)
print(eventishos)

a = set()
a.add("0")

for i in a:
    print(i)
a.clear()
print(a)
a.clear()
print(a)
"""


events = {
    "0": None,
    "1": None,
    "2": None,
    "3": None,
    "4": None
}

for i in events.values():
    print(i)