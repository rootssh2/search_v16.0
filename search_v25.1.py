import os
import argparse
from typing import List, Optional
from colorama import init, Fore, Back, Style
from pathlib import Path
import logging
import re
from tqdm import tqdm

init(autoreset=True)

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(options, title="Menu"):
    global banner
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
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
    
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
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
    tipos = {"1": "login", "2": "email", "3": "number", "4": "iptv"}
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
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

    with tqdm(total=len(arquivos_txt), desc="Procurando logins", unit="arquivo") as pbar:
        with arquivo_saida.open('w', encoding='utf-8') as outfile:
            for arquivo in arquivos_txt:
                try:
                    with arquivo.open('r', encoding='utf-8') as infile:
                        for linha in infile:
                            if termo_busca.lower() in linha.lower():
                                if tipo_login == 'iptv':
                                    iptv_match = re.search(r'([\w\.-]+)/get\.php\?username=([\w\d]+)&password=([\w\d]+)', linha)
                                    if iptv_match:
                                        username = iptv_match.group(2)
                                        password = iptv_match.group(3)
                                        outfile.write(f"{username}:{password}\n")
                                        contador_logins += 1
                                        pbar.set_description(f"Logins encontrados: {contador_logins}")
                                else:
                                    linha = linha.replace('|', ':').strip()
                                    partes = linha.split(':')
                                    if len(partes) >= 3:
                                        login_partes = partes[-2].strip()
                                        senha = partes[-1].strip()
                                        if (tipo_login == 'email' and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', login_partes)) or \
                                           (tipo_login == 'number' and re.match(r'^\+?\d+$', login_partes)) or \
                                           tipo_login == 'login':
                                            outfile.write(f"{login_partes}:{senha}\n")
                                            contador_logins += 1
                                            pbar.set_description(f"Logins encontrados: {contador_logins}")
                except UnicodeDecodeError:
                    logging.error(f"Erro de codificação no arquivo {arquivo}")
                
                pbar.update(1)

    logging.info(f"Resultados salvos em: {arquivo_saida}")
    logging.info(f"Total de logins encontrados: {contador_logins}")
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    print(f"\nTotal de {Fore.BLUE}{contador_logins}{Fore.RESET} logins encontrados.")
    return contador_logins

def remover_duplicados():
    resultados_dir = Path('resultados')
    wordlist_dir = Path('wordlist')
    wordlist_dir.mkdir(exist_ok=True)
    
    arquivos_resultados = list(resultados_dir.glob('*.txt'))
    if not arquivos_resultados:
        clean()
        print(f"{Fore.BLUE}{banner}{Fore.RESET}")
        print("Nenhum arquivo encontrado na pasta resultados.")
        return

    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    print("Arquivos na pasta resultados:")
    for i, arquivo in enumerate(arquivos_resultados, 1):
        print(f"{Fore.BLUE}{i}{Fore.RESET}. {arquivo.name}")
    
    try:
        escolha = int(input("\nDigite o número do arquivo para remover duplicados: ").strip())
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
    linhas_unicas = set()
    total_linhas = len(linhas)
    
    for linha in linhas:
        linha = linha.strip()
        if linha and not regex_invalidos.search(linha):
            partes = linha.split(':')
            if len(partes) == 2 and all(partes):
                linha_unica = f"{partes[0].strip()}:{partes[1].strip()}"
                if linha_unica not in linhas_unicas:
                    linhas_unicas.add(linha_unica)
                    linhas_validas.append(linha_unica)

    duplicados_removidos = total_linhas - len(linhas_validas)
    
    print(f"\nComo deseja salvar os logins?\n"
          f"[{Fore.BLUE}1{Fore.RESET}] login:pass\n"
          f"[{Fore.BLUE}2{Fore.RESET}] login|pass")
    formato_escolha = get_choice({"1": "login:pass", "2": "login|pass"})

    if formato_escolha == "1":
        formato = ":"
    else:
        formato = "|"

    # Modificado para incluir o termo de busca no nome do arquivo
    termo_busca = arquivo_entrada.stem.split('_')[1]
    arquivo_saida = wordlist_dir / f"combo_{termo_busca}.txt"
    with arquivo_saida.open('w', encoding='utf-8') as outfile:
        for linha in linhas_validas:
            login, passw = linha.split(':')
            outfile.write(f"{login.strip()}{formato}{passw.strip()}\n")
    
    logging.info(f"Wordlist gerada com {len(linhas_validas)} entradas válidas em {arquivo_saida}")
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    print(f"Wordlist atualizada com {Fore.BLUE}{duplicados_removidos}{Fore.RESET} Logins Duplicados Removidos.")
    print(f"Logins salvos no formato {Fore.BLUE}{formato_escolha}{Fore.RESET}.")

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
        clean()
        print(f"{Fore.BLUE}{banner}{Fore.RESET}")
        print(f"Divisão concluída com sucesso. {Fore.BLUE}{part_num - start_num}{Fore.RESET} partes criadas.")
    except IOError as e:
        print(f"Erro ao ler ou escrever o arquivo: {e}")

def limpar_db():
    wordlist_dir = Path('wordlist')
    if not wordlist_dir.exists() or not any(wordlist_dir.glob('*.txt')):
        print("Nenhum arquivo .txt encontrado na pasta wordlist.")
        return

    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    print("Arquivos na pasta wordlist:")
    arquivos_wordlist = list(wordlist_dir.glob('*.txt'))
    for i, arquivo in enumerate(arquivos_wordlist, 1):
        print(f"{Fore.BLUE}{i}{Fore.RESET}. {arquivo.name}")

    try:
        escolha = int(input("\nDigite o número do arquivo para limpar: ").strip())
        if 1 <= escolha <= len(arquivos_wordlist):
            arquivo_entrada = arquivos_wordlist[escolha - 1]
        else:
            print("Seleção inválida.")
            return
    except ValueError:
        print("Por favor, digite um número válido.")
        return

    regex_email = re.compile(r'((?:[A-Za-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])):')
    
    regex_senhas = re.compile(r':(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$|:(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$|:(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$|:(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')

    linhas_limpas = []
    total_linhas = 0

    with arquivo_entrada.open('r', encoding='utf-8') as infile:
        for linha in infile:
            total_linhas += 1
            partes = linha.strip().split(':')
            if len(partes) == 2:
                email, senha = partes
                if regex_email.match(email + ':') and regex_senhas.search(':' + senha):
                    linhas_limpas.append(f"{email}:{senha}")

    arquivo_saida = wordlist_dir / f"{arquivo_entrada.stem}_limpo.txt"
    with arquivo_saida.open('w', encoding='utf-8') as outfile:
        for linha in linhas_limpas:
            outfile.write(f"{linha}\n")

    logging.info(f"Arquivo limpo gerado com {len(linhas_limpas)} entradas válidas em {arquivo_saida}")
    clean()
    print(f"{Fore.BLUE}{banner}{Fore.RESET}")
    print(f"Arquivo limpo com {Fore.BLUE}{total_linhas - len(linhas_limpas)}{Fore.RESET} entradas inválidas removidas.")

banner = """╔═══╗────────╔╗────╔════╗
║╔═╗║────╔╗─╔╝╚╗───╚══╗═║
║╚═╝╠═╦══╬╬═╩╗╔╬══╗──╔╝╔╝
║╔══╣╔╣╔╗╠╣║═╣║║╔╗║─╔╝╔╝
║║──║║║╚╝║║║═╣╚╣╚╝║╔╝═╚═╗
╚╝──╚╝╚══╣╠══╩═╩══╝╚════╝
────────╔╝║
────────╚═╝
       v25.1 Final
       by Root2022
   Telegram: t.me/Root2022"""

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de busca e manipulação de logins.")
    parser.add_argument('--termo', help="Termo para busca de logins")
    parser.add_argument('--split', action='store_true', help="Dividir um arquivo grande em partes menores")
    args = parser.parse_args()

    main_menu = {
        "1": "Buscar Logins",
        "2": "Dividir Arquivos",
        "3": "Remover Duplicados",
        "4": "Limpeza de DBs",
        "q": "Sair"
    }

    while True:
        clean()
        print(f"{Fore.BLUE}{banner}{Fore.RESET}")
        print_menu(main_menu, "Menu Principal")
        choice = get_choice(main_menu)
        
        if choice == "1":  
            pastas_db = encontrar_pastas_db()
            pasta_selecionada = selecionar_pasta_db(pastas_db)
            if pasta_selecionada:
                tipo_login = escolher_tipo_login()
                termo_busca = args.termo or input("\nDigite uma palavra-chave para busca: ").strip()

                if termo_busca:
                    logins_encontrados = buscar_logins(pasta_selecionada, termo_busca, tipo_login)
                    print("\nOperação concluída. Escolha uma opção:")
                    print(f"[{Fore.BLUE}M{Fore.RESET}] - Voltar ao menu")
                    print(f"[{Fore.BLUE}Q{Fore.RESET}] - Sair")
                    sub_choice = get_choice({"m": "Voltar ao menu", "q": "Sair"})
                    if sub_choice == "q":
                        break
                else:
                    print("\nTermo de busca não pode estar vazio.")
            
        elif choice == "2":  
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
                print("\nOperação concluída. Escolha uma opção:")
                print(f"[{Fore.BLUE}M{Fore.RESET}] - Voltar ao menu")
                print(f"[{Fore.BLUE}Q{Fore.RESET}] - Sair")
                sub_choice = get_choice({"m": "Voltar ao menu", "q": "Sair"})
                if sub_choice == "q":
                    break
            else:
                print("Arquivo não encontrado na pasta 'divisor'.")

        elif choice == "3":  
            remover_duplicados()
            print("\nOperação concluída. Escolha uma opção:")
            print(f"[{Fore.BLUE}M{Fore.RESET}] - Voltar ao menu")
            print(f"[{Fore.BLUE}Q{Fore.RESET}] - Sair")
            sub_choice = get_choice({"m": "Voltar ao menu", "q": "Sair"})
            if sub_choice == "q":
                break

        elif choice == "4":  
            limpar_db()
            print("\nOperação concluída. Escolha uma opção:")
            print(f"[{Fore.BLUE}M{Fore.RESET}] - Voltar ao menu")
            print(f"[{Fore.BLUE}Q{Fore.RESET}] - Sair")
            sub_choice = get_choice({"m": "Voltar ao menu", "q": "Sair"})
            if sub_choice == "q":
                break

        elif choice == "q":
            print("Saindo do programa.")
            break

if __name__ == "__main__":
    main()