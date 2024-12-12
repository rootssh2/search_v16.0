# Login Search Tool 🔍🔐

## Descrição
Ferramenta de busca e manipulação de logins desenvolvida em Python, com funcionalidades para pesquisar, filtrar e processar arquivos de logins.

## 🚀 Funcionalidades
- **Busca de Logins**: Pesquise logins por palavra-chave
- **Tipos de Busca**: 
  - Login
  - Email
  - Número
  - IPTV
- **Remoção de Duplicados**: Remove entradas duplicadas de arquivos de logins
- **Divisão de Arquivos**: Divide arquivos grandes em partes menores

## 📋 Requisitos
- Python 3.7+
- Bibliotecas:
  - colorama
  - argparse
  - pathlib
  - logging
  - re (expressões regulares)

## 🛠️ Instalação

1. Clone o repositório
```bash
git clone https://seu-usuario/login-search-tool.git
cd login-search-tool
```

2. Instale as dependências
```bash
pip install colorama
```

## 🖥️ Uso

### Menu Principal
- `1`: Buscar Logins
- `2`: Dividir Arquivo
- `3`: Remover Duplicados
- `q`: Sair

### Exemplo de Uso
```bash
python search_v22.0.py
```

### Busca de Logins
1. Selecione uma pasta DB
2. Escolha o tipo de login
3. Digite uma palavra-chave de busca
4. Resultados serão salvos na pasta `resultados/`

### Remover Duplicados
1. Selecione o arquivo na pasta `resultados/`
2. Logins duplicados serão removidos
3. Resultado será salvo em `wordlist/combo.txt`

### Divisão de Arquivos
1. Coloque o arquivo na pasta `divisor/`
2. Escolha o número inicial do arquivo
3. Defina o tamanho de cada parte em MB

## 🔒 Avisos de Segurança
- Utilize a ferramenta apenas para fins legais e éticos
- Respeite políticas de privacidade e termos de uso

## 🤝 Contribuições
Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

## 👥 Autor
by Root2022

## 📞 Contato
Telegram: t.me/Root2022

## 🛡️ Disclaimer
Esta ferramenta é fornecida "como está", sem garantias de qualquer tipo.
