import os
import argparse
from typing import List, Optional
from colorama import init, Fore, Back, Style
from pathlib import Path
import logging
import re

init(autoreset=True)

def print_menu(options, title="Menu"):
    print(f"\n{title}")
    for key, value in options.items():
        print(f"[{Fore.BLUE}{key}{Fore.RESET}] - {value}")

def get_choice(options):
    while True:
        choice = input("\nEscolha uma opção: ").strip().lower()
        if choice in options:
            return choice
        print("Opção inválida. Tente novamente.")

def print_styled(message, color=Fore.WHITE, style=Style.NORMAL):
    print(message)

# Configuração de logging
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=logs_dir / 'login_search.log',
    filemode='a'
)

class LoginSearchError(Exception):
    pass

def validar_caminho(caminho: Path, tipo: str = 'dir') -> bool:
    try:
        if tipo == 'dir':
            return caminho.is_dir()
        elif tipo == 'file':
            return caminho.is_file()
    except Exception as e:
        logging.error(f"Erro ao validar caminho {caminho}: {e}")
    return False

def encontrar_pastas_db() -> List[Path]:
    return [Path(p) for p in Path('.').iterdir() if p.is_dir() and p.name.startswith('db')]

def selecionar_pasta_db(pastas_db: List[Path]) -> Optional[Path]:
    if not pastas_db:
        print("Nenhuma pasta DB encontrada no diretório atual.")
        return None
    
    print("\nSelecione uma pasta DB:")
    for i, pasta in enumerate(pastas_db, 1):
        print(f"{Fore.BLUE}{i}{Fore.RESET}. {pasta.name}")
    
    while True:
        try:
            escolha = int(input("Digite o número da pasta desejada: ").strip())
            if 1 <= escolha <= len(pastas_db):
                return pastas_db[escolha - 1]
            print("Seleção inválida.")
        except ValueError:
            print("Por favor, digite um número válido.")

def escolher_tipo_login() -> str:
    tipos = {"1": "login", "2": "email", "3": "number"}
    print("\nEscolha o tipo de login para busca:")
    print_menu(tipos, "Tipo de Login")
    return tipos[get_choice(tipos)]

def buscar_logins(diretorio: Path, termo_busca: str, tipo_login: str) -> int:
    resultados_dir = Path('resultados')
    resultados_dir.mkdir(exist_ok=True)
    
    if not termo_busca:
        raise LoginSearchError("Termo de busca não pode estar vazio")
    
    arquivos_txt = [f for f in diretorio.glob('*.txt')]
    if not arquivos_txt:
        logging.warning("Nenhum arquivo .txt encontrado")
        return 0

    contador_logins = 0
    arquivo_saida = resultados_dir / f"{tipo_login}_{termo_busca}_resultados.txt"

    with arquivo_saida.open('w', encoding='utf-8') as outfile:
        for arquivo in arquivos_txt:
            try:
                with arquivo.open('r', encoding='utf-8') as infile:
                    for linha in infile:
                        if termo_busca.lower() in linha.lower():
                            linha = linha.replace('|', ':').strip()
                            partes = linha.split(':')
                            if len(partes) >= 3:
                                login_partes = partes[-2].strip()
                                senha = partes[-1].strip()
                                if tipo_login == 'email' and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', login_partes):
                                    continue
                                elif tipo_login == 'number' and not re.match(r'^\+?\d+$', login_partes):
                                    continue
                                outfile.write(f"{login_partes}:{senha}\n")
                                contador_logins += 1
            except UnicodeDecodeError:
                logging.error(f"Erro de codificação no arquivo {arquivo}")

    logging.info(f"Resultados salvos em: {arquivo_saida}")
    logging.info(f"Total de logins encontrados: {contador_logins}")
    print(f"\nTotal de {Fore.BLUE}{contador_logins}{Fore.RESET} logins encontrados.")
    return contador_logins

def remover_duplicados():
    resultados_dir = Path('resultados')
    wordlist_dir = Path('wordlist')
    wordlist_dir.mkdir(exist_ok=True)
    
    arquivos_resultados = list(resultados_dir.glob('*.txt'))
    if not arquivos_resultados:
        print("Nenhum arquivo encontrado na pasta resultados.")
        return

    print("Arquivos na pasta resultados:")
    for i, arquivo in enumerate(arquivos_resultados, 1):
        print(f"{Fore.BLUE}{i}{Fore.RESET}. {arquivo.name}")
    
    try:
        escolha = int(input("Remove duplicados e linhas inválidas: ").strip())
        if 1 <= escolha <= len(arquivos_resultados):
            arquivo_entrada = arquivos_resultados[escolha - 1]
        else:
            print("Seleção inválida.")
            return
    except ValueError:
        print("Por favor, digite um número válido.")
        return

    regex_invalidos = re.compile(r'https?://|//[\w\.-]+|UNKNOWN|NOT_SAVED|^[^:]+:ENC\d+\*', re.IGNORECASE)
    with arquivo_entrada.open('r', encoding='utf-8') as infile:
        linhas = infile.readlines()

    linhas_validas = []
    for linha in linhas:
        linha = linha.strip()
        if linha and not regex_invalidos.search(linha):
            partes = linha.split(':')
            if len(partes) == 2 and all(partes):
                linha_unica = f"{partes[0].strip()}:{partes[1].strip()}"
                if linha_unica not in linhas_validas:
                    linhas_validas.append(linha_unica)

    arquivo_saida = wordlist_dir / "combo.txt"
    with arquivo_saida.open('w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(linhas_validas))
    
    logging.info(f"Wordlist gerada com {len(linhas_validas)} entradas válidas em {arquivo_saida}")

def split_file(filename, start_num, part_size):
    file_path = Path(filename)
    part_num = start_num
    try:
        with file_path.open('rb') as f:
            while True:
                chunk = f.read(part_size)
                if not chunk:
                    break
                part_filename = f"{part_num}.txt"
                with open(Path('divisor') / part_filename, 'wb') as part_file:
                    part_file.write(chunk)
                part_num += 1
        print(f"Divisão concluída com sucesso. {Fore.BLUE}{part_num - start_num}{Fore.RESET} partes criadas.")
    except IOError as e:
        print(f"Erro ao ler ou escrever o arquivo: {e}")

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de busca e manipulação de logins.")
    parser.add_argument('--termo', help="Termo para busca de logins")
    parser.add_argument('--split', action='store_true', help="Dividir um arquivo grande em partes menores")
    args = parser.parse_args()

    main_menu = {
        "1": "Buscar Logins",
        "2": "Dividir Arquivo",
        "3": "Remover Duplicados",
        "q": "Sair"
    }

    while True:
        print_menu(main_menu, "Menu Principal")
        choice = get_choice(main_menu)
        
        if choice == "1":  # Busca de Logins
            pastas_db = encontrar_pastas_db()
            pasta_selecionada = selecionar_pasta_db(pastas_db)
            if pasta_selecionada:
                tipo_login = escolher_tipo_login()
                termo_busca = args.termo or input("\nDigite uma palavra-chave para busca: ").strip()

                if termo_busca:
                    logins_encontrados = buscar_logins(pasta_selecionada, termo_busca, tipo_login)
                else:
                    print("\nTermo de busca não pode estar vazio.")
            
        elif choice == "2":  # Dividir Arquivo
            divisor_dir = Path('divisor')
            divisor_dir.mkdir(exist_ok=True)
            
            print("Por favor, mova o arquivo .txt que deseja dividir para a pasta 'divisor'.")
            file_to_split = input("Digite o nome do arquivo .txt na pasta 'divisor' para dividir: ")
            file_to_split_path = divisor_dir / file_to_split

            if file_to_split_path.is_file():
                start_num = int(input("Digite o número inicial para o arquivo dividido: "))
                part_size_mb = int(input("Digite o tamanho de cada divisão em MB: "))
                part_size = part_size_mb * 1024 * 1024                
                split_file(str(file_to_split_path), start_num, part_size)
            else:
                print("Arquivo não encontrado na pasta 'divisor'.")

        elif choice == "3":  # Remover Duplicados
            remover_duplicados()
        
        elif choice == "q":
            print("Saindo do programa.")
            break

if __name__ == "__main__":
    banner = """╔═══╗────────╔╗────╔════╗
║╔═╗║────╔╗─╔╝╚╗───╚══╗═║
║╚═╝╠═╦══╬╬═╩╗╔╬══╗──╔╝╔╝
║╔══╣╔╣╔╗╠╣║═╣║║╔╗║─╔╝╔╝
║║──║║║╚╝║║║═╣╚╣╚╝║╔╝═╚═╗
╚╝──╚╝╚══╣╠══╩═╩══╝╚════╝
────────╔╝║
────────╚═╝
        v21.0 Beta
       by Root2022
   Telegram: t.me/Root2022"""
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    main()