from scripts.extract import extract_from_json
from scripts.analyze import count_connections, drop_connections, make_graph
from scripts.freqs import gen_freqs

print("Введите название файла с данными(без расширения)")
filename = input()
print("Извлекаем данные...")
data = extract_from_json(f"./data/{filename}.json", limit=1000)
print("Переименовываем сущности...")
gen_freqs(filename)

from scripts.entity_naming import fix_names #нужно в таком порядке

data = fix_names(data)
print("Считаем соединения...")
connections = count_connections(data)
print("Строим граф...")
connections = drop_connections(connections, connection_limit=7)
graph = make_graph(connections)
graph.show(f"./visualizations/{filename}.html")
print(f"Граф сгенерирован в файле \"./visualizations/{filename}.html\"")