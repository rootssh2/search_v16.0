import os

def split_file(filename, start_num, part_size):
    with open(filename, 'rb') as f:
        part_num = start_num
        while True:
            chunk = f.read(part_size)
            if not chunk:
                break
            part_filename = f"{part_num}.txt"
            with open(part_filename, 'wb') as part_file:
                part_file.write(chunk)
            part_num += 1

file_to_split = input("Digite o nome do arquivo .txt para dividir: ")
start_num = int(input("Digite o número inicial para o arquivo dividido: "))
part_size_mb = int(input("Digite o tamanho de cada divisão em MB: "))
part_size = part_size_mb * 1024 * 1024

if os.path.isfile(file_to_split):
    split_file(file_to_split, start_num, part_size)
    print("Divisão concluída com sucesso!")
else:
    print("Arquivo não encontrado.")