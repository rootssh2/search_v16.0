# Login Search v16.0

Bem-vindo ao **Login Search v16.0**! Este script foi desenvolvido para realizar buscas em arquivos de texto contendo informações de login, filtrando e organizando os dados em diferentes formatos, como `login:senha`, `email:senha` ou `número:senha`.

## Funcionalidades

- **Busca de logins** em arquivos `.txt` dentro de diretórios especificados.
- **Filtro por tipo de login**: `login:senha`, `email:senha` ou `número:senha`.
- **Remoção de duplicados** e linhas inválidas automaticamente.
- **Salvamento dos resultados** em arquivos organizados por tipo de login.
- **Geração de wordlist limpa** pronta para uso.
- **Logs detalhados** para monitoramento das operações realizadas.

## Requisitos

- Python 3.x
- Bibliotecas necessárias:
  - `colorama`
  - `logging`

### Instalação de dependências

Para instalar a biblioteca `colorama`, execute o seguinte comando:

```bash
pip install colorama
