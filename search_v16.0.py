import os
import re
import logging
from typing import List, Optional
from colorama import init, Fore

init(autoreset=True)

banner = """
╔═══╗────────╔╗────╔════╗
║╔═╗║────╔╗─╔╝╚╗───╚══╗═║
║╚═╝╠═╦══╬╬═╩╗╔╬══╗──╔╝╔╝
║╔══╣╔╣╔╗╠╣║═╣║║╔╗║─╔╝╔╝
║║──║║║╚╝║║║═╣╚╣╚╝║╔╝═╚═╗
╚╝──╚╝╚══╣╠══╩═╩══╝╚════╝
────────╔╝║
────────╚═╝
          v16.0
    by t.me/Root2022
"""

print(Fore.BLUE + banner)

# Criar pasta logs se não existir
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename=os.path.join(logs_dir, 'login_search.log')
)

class LoginSearchError(Exception):
    """Classe de exceção personalizada para erros de busca de login."""
    pass

def validar_caminho(caminho: str, tipo: str = 'dir') -> bool:
    """
    Valida se o caminho existe e é do tipo esperado.
    
    Args:
        caminho (str): Caminho a ser validado
        tipo (str): Tipo de validação ('dir' ou 'file')
    
    Returns:
        bool: Verdadeiro se o caminho for válido
    """
    try:
        if tipo == 'dir':
            return os.path.isdir(caminho)
        elif tipo == 'file':
            return os.path.isfile(caminho)
    except Exception as e:
        logging.error(f"Erro ao validar caminho {caminho}: {e}")
    return False

def encontrar_pastas_db() -> List[str]:
    """
    Encontra todas as pastas que começam com 'db' no diretório atual.
    
    Returns:
        List[str]: Lista de pastas encontradas
    """
    pastas_db = [pasta for pasta in os.listdir('.') if os.path.isdir(pasta) and pasta.startswith('db')]
    return pastas_db

def selecionar_pasta_db(pastas_db: List[str]) -> Optional[str]:
    """
    Permite ao usuário selecionar uma pasta da lista de pastas DB.
    
    Args:
        pastas_db (List[str]): Lista de pastas começando com 'db'
    
    Returns:
        Optional[str]: Caminho da pasta selecionada ou None
    """
    if not pastas_db:
        print("Nenhuma pasta DB encontrada no diretório atual.")
        return None
    
    print("Pastas DB encontradas:")
    for i, pasta in enumerate(pastas_db, 1):
        print(f"{i}. {pasta}")
    
    try:
        escolha = int(input("Digite o número da pasta desejada: ").strip())
        if 1 <= escolha <= len(pastas_db):
            return pastas_db[escolha - 1]
        else:
            print("Seleção inválida.")
            return None
    except ValueError:
        print("Por favor, digite um número válido.")
        return None

def escolher_tipo_login() -> str:
    """
    Permite ao usuário escolher o tipo de login para busca.
    
    Returns:
        str: Tipo de login selecionado ('login', 'email', 'number')
    """
    print("\nEscolha o tipo de login para busca:")
    print("1. login:pass")
    print("2. email:pass")
    print("3. number:pass")
    
    while True:
        try:
            escolha = input("Digite o número da opção desejada: ").strip()
            
            if escolha == "1":
                return "login"
            elif escolha == "2":
                return "email"
            elif escolha == "3":
                return "number"
            else:
                print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
            return ""

def buscar_logins(diretorio: str, termo_busca: str, tipo_login: str) -> int:
    """
    Busca logins em arquivos .txt de um diretório.
    
    Args:
        diretorio (str): Caminho do diretório
        termo_busca (str): Termo para busca
        tipo_login (str): Tipo de login para filtrar ('login', 'email', 'number')
    
    Returns:
        int: Número de logins encontrados
    """
    try:
        # Criar pasta resultados se não existir
        pasta_resultados = 'resultados'
        os.makedirs(pasta_resultados, exist_ok=True)
        
        # Validações de entrada
        if not termo_busca:
            raise LoginSearchError("Termo de busca não pode estar vazio")
        
        # Busca arquivos .txt
        arquivos_txt = [f for f in os.listdir(diretorio) if f.endswith('.txt')]
        
        if not arquivos_txt:
            logging.warning("Nenhum arquivo .txt encontrado")
            return 0
        
        # Processamento de arquivos
        contador_logins = 0
        arquivo_saida = os.path.join(pasta_resultados, f"{tipo_login}_{termo_busca}_resultados.txt")
        
        with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
            for arquivo_txt in arquivos_txt:
                caminho_completo = os.path.join(diretorio, arquivo_txt)
                
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as infile:
                        for linha in infile:
                            if termo_busca.lower() in linha.lower():
                                # Processamento de linha
                                linha = linha.replace('|', ':').strip()
                                partes = linha.split(':')
                                
                                if len(partes) >= 3:
                                    login_partes = partes[-2].strip()
                                    senha = partes[-1].strip()
                                    
                                    # Filtro por tipo de login
                                    filtro_valido = False
                                    
                                    if tipo_login == 'login':
                                        # Igual ao código original: todos os logins
                                        filtro_valido = True
                                    
                                    elif tipo_login == 'email':
                                        # email: padrão de email válido
                                        filtro_valido = re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', login_partes)
                                    
                                    elif tipo_login == 'number':
                                        # número: apenas dígitos, pode ter + no início
                                        filtro_valido = re.match(r'^\+?\d+$', login_partes)
                                    
                                    if filtro_valido and login_partes and senha:
                                        outfile.write(f"{login_partes}:{senha}\n")
                                        contador_logins += 1
                
                except UnicodeDecodeError:
                    logging.error(f"Erro de codificação no arquivo {arquivo_txt}")
        
        logging.info(f"Resultados salvos em: {arquivo_saida}")
        logging.info(f"Total de logins encontrados: {contador_logins}")
        return contador_logins
    
    except PermissionError:
        logging.error("Sem permissão para acessar o diretório")
    except FileNotFoundError:
        logging.error("Diretório não encontrado")
    except LoginSearchError as e:
        logging.error(str(e))
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
    
    return 0 
    
def remover_duplicados() -> None:
    """
    Remove linhas duplicadas e inválidas de um arquivo na pasta resultados.
    """
    try:
        # Criar pasta wordlist se não existir
        pasta_wordlist = 'wordlist'
        os.makedirs(pasta_wordlist, exist_ok=True)
        
        # Listar arquivos na pasta resultados
        pasta_resultados = 'resultados'
        arquivos_resultados = [f for f in os.listdir(pasta_resultados) if f.endswith('.txt')]
        
        if not arquivos_resultados:
            print("Nenhum arquivo encontrado na pasta resultados.")
            return
        
        print("Arquivos na pasta resultados:")
        for i, arquivo in enumerate(arquivos_resultados, 1):
            print(f"{i}. {arquivo}")
        
        # Selecionar arquivo
        try:
            escolha = int(input("Remove duplicados e linhas inválidas: ").strip())
            if 1 <= escolha <= len(arquivos_resultados):
                arquivo_entrada = os.path.join(pasta_resultados, arquivos_resultados[escolha - 1])
            else:
                print("Seleção inválida.")
                return
        except ValueError:
            print("Por favor, digite um número válido.")
            return
        
        # Regex para identificar linhas inválidas
        regex_invalidos = re.compile(
            r'https?://|//[\w\-\.]+|UNKNOWN|NOT_SAVED|^[^:]+:ENC\d+\*', 
            re.IGNORECASE
        )
        
        # Leitura e processamento
        with open(arquivo_entrada, 'r', encoding='utf-8') as infile:
            linhas = infile.readlines()
        
        # Remove duplicados e linhas inválidas
        linhas_unicas = set()
        linhas_validas = []
        for linha in linhas:
            linha = linha.strip()
            if linha and not regex_invalidos.search(linha):
                # Mantém apenas linhas no formato login:senha
                partes = linha.split(':')
                if len(partes) == 2:
                    login = partes[0].strip()
                    senha = partes[1].strip()
                    if login and senha:
                        linha_unica = f"{login}:{senha}"
                        if linha_unica not in linhas_unicas:
                            linhas_unicas.add(linha_unica)
                            linhas_validas.append(linha_unica)

        # Salvar as linhas válidas e únicas em um novo arquivo
        arquivo_saida = os.path.join(pasta_wordlist, "combo.txt")
        with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
            for linha in linhas_validas:
                outfile.write(f"{linha}\n")
        
        logging.info(f"Wordlist gerada com {len(linhas_validas)} entradas válidas em {arquivo_saida}")
    
    except Exception as e:
        logging.error(f"Erro ao processar duplicados: {e}")

def main():
    try:
        pastas_db = encontrar_pastas_db()
        pasta_selecionada = selecionar_pasta_db(pastas_db)
        
        if pasta_selecionada:
            tipo_login = escolher_tipo_login()
            termo_busca = input("\nDigite uma palavra-chave para busca: ").strip()

            if termo_busca:
                logins_encontrados = buscar_logins(pasta_selecionada, termo_busca, tipo_login)
                print(f"\nTotal de logins encontrados: {logins_encontrados}")
            else:
                print("\nTermo de busca não pode estar vazio.")
            
            remover_duplicados()

    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        logging.error(f"Erro inesperado no processo principal: {e}")
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()                  