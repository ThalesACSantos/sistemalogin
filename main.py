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

# Variável global para controlar a visibilidade da senha
senha_visivel = False

# Carregar imagens (certifique-se de que os caminhos estejam corretos)
try:
    olho_aberto = ctk.CTkImage(light_image=Image.open(os.path.join("imagens", "olho_aberto.png")),
                                dark_image=Image.open(os.path.join("imagens", "olho_aberto.png")))
    olho_fechado = ctk.CTkImage(light_image=Image.open(os.path.join("imagens", "olho_fechado.png")),
                                 dark_image=Image.open(os.path.join("imagens", "olho_fechado.png")))
except FileNotFoundError:
    print("Erro: Imagens não encontradas. Certifique-se de que os arquivos 'olho_aberto.png' e 'olho_fechado.png' estejam na pasta 'imagens'.")
    exit()  # Encerra o programa se as imagens não forem encontradas


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

    # Obtém a coordenada y do campo de senha
    try:
        senha_y = entry_senha.winfo_y()
        if senha_y > 0:
            mostrar_senha_button.place(x=250, y=senha_y)
        else:
            mostrar_senha_button.place(x=250, y=113)  # Posiciona o botão ao lado do campo de senha
    except Exception as e:
        print(f"Erro ao tentar posicionar {e}")

    if senha_visivel:
        entry_senha.configure(show="")

        # Posiciona o botão de olho alinhado com o campo de senha
        mostrar_senha_button.configure(image=olho_aberto)
    else:
        entry_senha.configure(show="*")
        mostrar_senha_button.configure(image=olho_fechado)


# Criando a interface gráfica
app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("350x350")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label_titulo = ctk.CTkLabel(master=frame, text="Python em Ação :\n Fazer Login", font=("Arial", 20))
label_titulo.pack(pady=12)

entry_usuario = ctk.CTkEntry(master=frame, placeholder_text="Usuário")
entry_usuario.pack(pady=5)

entry_senha = ctk.CTkEntry(master=frame, placeholder_text="Senha", show="*")
entry_senha.pack(pady=5)

# Botão para mostrar/ocultar senha
mostrar_senha_button = ctk.CTkButton(master=frame, bg_color="white", image=olho_fechado, text="", width=30, height=30, command=toggle_senha)
mostrar_senha_button.place(x=250, y=113)  # Posiciona o botão ao lado do campo de senha

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
