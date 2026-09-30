import json
import os


# XOR-хэш файла по 16-битным отрезкам.
# Читаем файл как бинарный поток, режем на куски по 2 байта,
# складываем их по XOR. Если в последнем куске не хватает байта, дополняем нулём
def hash_this_file(filename: str) -> int:
    hash_value = 0
    with open(filename, "rb") as f:
        # читаем файл по 2 байта(16 бит)
        while True:
            line = f.read(2)
            if not line:
                break
            if len(line) < 2:
                line = line + b"\x00"
            value = int.from_bytes(line, byteorder="big")
            hash_value = hash_value ^ value

    return hash_value


def walk_and_count_hash(init_catalogue, exclude_name="hashes.json") -> dict:
    hash_values = {}
    for dirpath, dirnames, filenames in os.walk(init_catalogue):
        for filename in filenames:
            # пропускаем файл хэшей
            if filename == exclude_name:
                continue

            filepath = os.path.join(dirpath, filename)
            hash_value = hash_this_file(filepath)
            hash_values[filepath] = hash_value

    return hash_values



def task1(init_catalogue = "task1_directory/walk_here"):
    output_path = os.path.join(init_catalogue, "hashes.json")
    if not os.path.exists(output_path):
        hash_values = walk_and_count_hash(init_catalogue)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(hash_values, f, ensure_ascii=False, indent=2)

    else:
        with open(output_path, "r", encoding="utf-8") as f:
            old_hash_values = json.load(f)
            new_hash_values = walk_and_count_hash(init_catalogue)

            changes_found = False
            for filename, hash_value in new_hash_values.items():
                if filename not in old_hash_values.keys():
                    print(f"Появился новый файл - {filename}")
                    changes_found = True
                    continue
                if old_hash_values[filename] != new_hash_values[filename]:
                    print(f"Содержимое файла {filename} было изменено")
                    changes_found = True

            for filename in old_hash_values:
                if filename not in new_hash_values:
                    print(f"Файл удалён - {filename}")
                    changes_found = True

            if not changes_found:
                print("Ничего не менялось")

task1()
