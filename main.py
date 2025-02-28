import customtkinter as ctk
import os
import re
import webbrowser  # Importa o módulo webbrowser
from PIL import Image  # Importa a biblioteca PIL para trabalhar com imagens


# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Nome do arquivo para armazenar os usuários
ARQUIVO_USUARIOS = "usuarios.txt"

# Verifica se o arquivo existe, se não existir, cria
if not os.path.exists(ARQUIVO_USUARIOS):
    try:
        with open(ARQUIVO_USUARIOS, "w") as f:
            pass  # Cria um arquivo vazio
        print(f"Arquivo '{ARQUIVO_USUARIOS}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar arquivo: {e}")
        exit()  # Encerra o programa se houver um erro na criação

# Carregar imagens (certifique-se de que os caminhos estejam corretos)
try:
    olho_aberto_cinza = ctk.CTkImage(light_image=Image.open(os.path.join("imagens", "olho_aberto_cinza.png")),
                                dark_image=Image.open(os.path.join("imagens", "olho_aberto_cinza.png")))
    olho_fechado_cinza = ctk.CTkImage(light_image=Image.open(os.path.join("imagens", "olho_fechado_cinza.png")),
                                 dark_image=Image.open(os.path.join("imagens", "olho_fechado_cinza.png")))
except FileNotFoundError:
    print("Erro: Imagens não encontradas. Certifique-se de que os arquivos 'olho_aberto_cinza.png' e 'olho_fechado_cinza.png' estejam na pasta 'imagens'.")
    exit()  # Encerra o programa se as imagens não forem encontradas

# Variável global para controlar a visibilidade da senha
senha_visivel = False

def salvar_usuario(username, password):
    """Salva um novo usuário no arquivo."""
    try:
        with open(ARQUIVO_USUARIOS, "a") as f:
            f.write(f"{username},{password}\n")
    except Exception as e:
        label_status.configure(text=f"Erro ao salvar usuário: {e}", text_color="red")


def verificar_usuario(username, password=None):
    """Verifica se o usuário está cadastrado e opcionalmente se a senha confere."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return False

    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            usuarios = f.readlines()
    except Exception as e:
        label_status.configure(text=f"Erro ao ler usuários: {e}", text_color="red")
        return False

    for usuario in usuarios:
        try:
            user, pwd = usuario.strip().split(",")
            if user == username:
                if password is None or pwd == password:
                    return True
        except ValueError:
            continue  # Ignora linhas inválidas
    return False


def cadastrar():
    try:
        username = entry_usuario.get().strip()
        password = entry_senha.get().strip()

        # Validação do tamanho do nome de usuário e senha
        if len(username) > 20:
            label_status.configure(text="Nome de usuário muito longo (máximo 20 caracteres).", text_color="red")
            return

        if len(password) > 20:
            label_status.configure(text="Senha muito longa (máximo 20 caracteres).", text_color="red")
            return

        if not username or not password:
            label_status.configure(text="Preencha todos os campos!", text_color="red")
            return

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            label_status.configure(text="Usuário inválido! Use apenas letras, números e _", text_color="red")
            return

        if len(password) < 6:
            label_status.configure(text="A senha deve ter pelo menos 6 caracteres!", text_color="red")
            return

        if verificar_usuario(username):
            label_status.configure(text="Usuário já cadastrado!", text_color="red")
            return

        salvar_usuario(username, password)
        label_status.configure(text="Usuário cadastrado com sucesso!", text_color="green")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")


def login():
    try:
        username = entry_usuario.get().strip()
        password = entry_senha.get().strip()

        if not username or not password:
            label_status.configure(text="Preencha todos os campos!", text_color="red")
            return

        if verificar_usuario(username, password):
            label_status.configure(text="Login realizado com sucesso!", text_color="green")
            webbrowser.open_new_tab("https://sites.google.com/view/roboticamarte/mat%C3%A9rias/python-em-a%C3%A7%C3%A3o?pli=1")  # Abre o site
        else:
            label_status.configure(text="Usuário ou senha incorretos!", text_color="red")
    except Exception as e:
        print(f"Erro ao fazer login: {e}")


def toggle_senha():
    global senha_visivel
    senha_visivel = not senha_visivel

    if senha_visivel:
        entry_senha.configure(show="")

        # Posiciona o botão de olho alinhado com o campo de senha
        mostrar_senha_button.configure(image=olho_aberto_cinza)
    else:
        entry_senha.configure(show="*")
        mostrar_senha_button.configure(image=olho_fechado_cinza)


# Criando a interface gráfica
app = ctk.CTk()
app.title("Python em Ação")
app.geometry("350x350")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label_titulo = ctk.CTkLabel(master=frame, text="Python em Ação :\n Fazer Login", font=("Arial", 20))
label_titulo.pack(pady=12)

def limitar_entrada(event):
    entry = event.widget  # Obtém o widget que gerou o evento
    conteudo = entry.get()
    if len(conteudo) > 13:
        entry.delete(13, ctk.END)  # Apaga os caracteres excedentes

# Frame para usuário e senha
frame_entradas = ctk.CTkFrame(master=frame)
frame_entradas.pack(pady=5)

# Campo de usuário
entry_usuario = ctk.CTkEntry(master=frame_entradas, placeholder_text="Usuário")
entry_usuario.bind("<KeyRelease>", limitar_entrada)
entry_usuario.grid(row=0, column=0, sticky="ew")

# Frame para senha e botão de olho
frame_senha = ctk.CTkFrame(master=frame_entradas)
frame_senha.grid(row=1, column=0, sticky="ew", pady=5)

# Campo de senha
entry_senha = ctk.CTkEntry(master=frame_senha, placeholder_text="Senha", show="*")
entry_senha.bind("<KeyRelease>", limitar_entrada)
entry_senha.grid(row=0, column=0, sticky="ew")

# Botão de olho
mostrar_senha_button = ctk.CTkButton(master=frame_senha, fg_color="light gray", image=olho_fechado_cinza, text="", width=15, height=2, command=toggle_senha, corner_radius=150)
mostrar_senha_button.grid(row=0, column=0, sticky="e", padx=(0, 5))  # Posiciona o botão à direita e com padx

# Configura as colunas para expandir
frame_entradas.columnconfigure(0, weight=1)
frame_senha.columnconfigure(0, weight=1)

btn_login = ctk.CTkButton(master=frame, text="Login", command=login)
btn_login.pack(pady=5)

label_cadastrar = ctk.CTkLabel(master=frame, text="Ainda não tenho conta", font=("Arial", 20))
label_cadastrar.pack(pady=10)

btn_cadastrar = ctk.CTkButton(master=frame, text="Cadastrar", command=cadastrar)
btn_cadastrar.pack(padx=5)

label_status = ctk.CTkLabel(master=frame, text="", font=("Arial", 12))
label_status.pack(pady=5)

try:
    # inicializando o aplicativo
    if __name__ == "__main__":
       app.mainloop()
except Exception as e:
    print(f"Erro inesperado: {e}")
