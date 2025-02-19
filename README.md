![loginCadastro2](https://github.com/user-attachments/assets/7f14454b-f33d-4f8d-bad7-ac353e09d063)

# Sistema de Login com CustomTkinter

Este é um sistema de login simples desenvolvido em Python com a biblioteca CustomTkinter. Ele permite que os usuários se cadastrem e façam login, armazenando as informações em um arquivo de texto.

## Funcionalidades

- Cadastro de novos usuários com validação de nome de usuário (apenas letras, números e _) e senha (mínimo de 6 caracteres).
- Login de usuários existentes com verificação de nome de usuário e senha.
- Interface gráfica amigável com CustomTkinter.
- Mensagens de status informativas para o usuário.

## Como usar

1. Clone este repositório.
2. Certifique-se de ter o Python instalado em seu sistema.
3. Instale as dependências necessárias:
   ```bash
   pip install customtkinter
4. Instale as dependências necessárias do PIL:
   ```bash
   pip install Pillow
5. Execute o script main.py:
   ```bash
   python main.py


## Estrutura do código
## main.py: 
Contém o código principal do sistema de login, incluindo a interface gráfica e as funções de cadastro e login.

## usuarios.txt: 
Arquivo de texto que armazena as informações dos usuários (nome de usuário e senha separados por vírgula).

# Dependências

## CustomTkinter: 
Biblioteca para criação de interfaces gráficas personalizadas em Python.

## Observações
As senhas são armazenadas em texto plano no arquivo usuarios.txt, o que não é recomendado para sistemas de login em produção. Em vez disso, use técnicas de hash para armazenar as senhas de forma segura.
O código foi desenvolvido para fins de demonstração e pode ser aprimorado para atender a requisitos mais complexos.

## Contribuições
Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

