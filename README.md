# Login Search Tool

Este é um script Python para buscar, manipular e processar logins de arquivos `.txt`. Ele oferece funcionalidades para pesquisar logins em pastas de banco de dados, remover duplicados e dividir grandes arquivos em partes menores.

## Funcionalidades

- **Busca de Logins**: Permite buscar logins e senhas em arquivos `.txt` dentro de pastas de banco de dados.
- **Remover Duplicados**: Remove logins duplicados ou inválidos e gera uma nova `wordlist`.
- **Dividir Arquivo**: Divide arquivos grandes em partes menores para facilitar o manuseio.

## Requisitos

- Python 3.x
- Bibliotecas necessárias:
  - `argparse`
  - `colorama`
  - `re`
  - `pathlib`
  - `logging`

Instale as dependências com o seguinte comando:

```bash
pip install -r requirements.txt
