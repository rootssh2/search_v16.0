# Ferramenta de Busca de Logins - v25.1

## Visão Geral

Este script em Python foi projetado para procurar, manipular e limpar credenciais de login em vários arquivos de texto. Ele oferece funcionalidades para:

- **Busca de Logins** baseada em critérios específicos em diretórios designados.
- **Divisão de Arquivos Grandes** em partes menores.
- **Remoção de Logins Duplicados** dos conjuntos de resultados.
- **Limpeza de Dados** usando expressões regulares específicas para filtrar entradas inválidas ou indesejadas.

## Funcionalidades

- **Busca de Logins:** Procura por logins baseados na entrada do usuário dentro de pastas 'db' ou em uma estrutura de diretório 'cloud'.
- **Divisão de Arquivos:** Divide arquivos de texto grandes em arquivos menores para melhor gerenciamento.
- **Remoção de Duplicatas:** Remove entradas duplicadas de arquivos de login, permitindo a personalização do formato de saída.
- **Limpeza de Dados:** Limpa dados de login usando padrões de regex predefinidos para garantir que apenas e-mails e senhas válidas sejam mantidos.

## Dependências

- [colorama](https://pypi.org/project/colorama/) - Para saída colorida no terminal.
- [tqdm](https://pypi.org/project/tqdm/) - Para barras de progresso na execução das tarefas.

Instale as dependências com:

```bash
pip install colorama tqdm
