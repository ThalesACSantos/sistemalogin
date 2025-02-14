sistemaloginimport customtkinter as ctk
import os
import re

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Nome do arquivo para armazenar os usuários
ARQUIVO_USUARIOS = "usuarios.txt"


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
        else:
            label_status.configure(text="Usuário ou senha incorretos!", text_color="red")
    except Exception as e:
        print(f"Erro ao fazer login: {e}")


# Criando a interface gráfica
app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("400x300")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label_titulo = ctk.CTkLabel(master=frame, text="Login / Cadastro", font=("Arial", 20))
label_titulo.pack(pady=12)

entry_usuario = ctk.CTkEntry(master=frame, placeholder_text="Usuário")
entry_usuario.pack(pady=5)

entry_senha = ctk.CTkEntry(master=frame, placeholder_text="Senha", show="*")
entry_senha.pack(pady=5)

btn_login = ctk.CTkButton(master=frame, text="Login", command=login)
btn_login.pack(pady=5)

btn_cadastrar = ctk.CTkButton(master=frame, text="Cadastrar", command=cadastrar)
btn_cadastrar.pack(pady=5)

label_status = ctk.CTkLabel(master=frame, text="", font=("Arial", 12))
label_status.pack(pady=5)

try:
    # inicializando o aplicativo
    if __name__ == "__main__":
       app.mainloop()
except Exception as e:
    print(f"Erro inesperado: {e}")
