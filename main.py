import customtkinter as ctk
import os
import re
import webbrowser
from PIL import Image

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

def salvar_usuario(username, email, password):
    """Salva um novo usuário no arquivo."""
    try:
        with open(ARQUIVO_USUARIOS, "a") as f:
            f.write(f"{username},{email},{password}\n")
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")

def verificar_usuario_existente(username=None, email=None):
    """Verifica se o usuário ou e-mail já estão cadastrados."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return False

    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            usuarios = f.readlines()
    except Exception as e:
        print(f"Erro ao ler usuários: {e}")
        return False

    for usuario_info in usuarios:
        try:
            partes = usuario_info.strip().split(",")
            if len(partes) == 3:  # Verifica se a linha tem o formato esperado
                cadastrado_username, cadastrado_email, _ = partes
                if username and cadastrado_username == username:
                    return True
                if email and cadastrado_email == email:
                    return True
        except ValueError:
            continue  # Ignora linhas inválidas
    return False

def verificar_login(username, password):
    """Verifica se o usuário está cadastrado e se a senha confere para o login."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return False

    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            usuarios = f.readlines()
    except Exception as e:
        print(f"Erro ao ler usuários: {e}")
        return False

    for usuario_info in usuarios:
        try:
            cadastrado_username, _, cadastrado_password = usuario_info.strip().split(",")
            if cadastrado_username == username and cadastrado_password == password:
                return True
        except ValueError:
            continue  # Ignora linhas inválidas
    return False

def login():
    username = entry_usuario.get().strip()
    password = entry_senha.get().strip()

    if not username or not password:
        label_status.configure(text="Preencha todos os campos!", text_color="red")
        return

    if verificar_login(username, password):
        label_status.configure(text="Login realizado com sucesso!", text_color="green")
        webbrowser.open_new_tab("https://sites.google.com/view/roboticamarte/mat%C3%A9rias/python-em-a%C3%A7%C3%A3o?pli=1")
    else:
        label_status.configure(text="Usuário ou senha incorretos!", text_color="red")

def toggle_senha_login():
    global senha_visivel
    senha_visivel = not senha_visivel

    if senha_visivel:
        entry_senha.configure(show="")
        mostrar_senha_button.configure(image=olho_aberto_cinza)
    else:
        entry_senha.configure(show="*")
        mostrar_senha_button.configure(image=olho_fechado_cinza)

def toggle_senha_cadastro(entry_senha_cadastro, entry_confirmar_senha_cadastro, btn_olho_senha_cadastro, btn_olho_confirmar_senha_cadastro, status_senha_cadastro, status_confirmar_senha_cadastro):
    global senha_visivel
    senha_visivel = not senha_visivel

    if senha_visivel:
        entry_senha_cadastro.configure(show="")
        entry_confirmar_senha_cadastro.configure(show="")
        btn_olho_senha_cadastro.configure(image=olho_aberto_cinza)
        btn_olho_confirmar_senha_cadastro.configure(image=olho_aberto_cinza)
        status_senha_cadastro.configure(text="Senha visível", text_color="gray")
        status_confirmar_senha_cadastro.configure(text="Senha visível", text_color="gray")
    else:
        entry_senha_cadastro.configure(show="*")
        entry_confirmar_senha_cadastro.configure(show="*")
        btn_olho_senha_cadastro.configure(image=olho_fechado_cinza)
        btn_olho_confirmar_senha_cadastro.configure(image=olho_fechado_cinza)
        status_senha_cadastro.configure(text="", text_color="gray")
        status_confirmar_senha_cadastro.configure(text="", text_color="gray")

def validar_email(email):
    # Regex para validar o formato do e-mail
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def tela_cadastro():
    app.withdraw()  # Esconde a tela de login

    cadastro_app = ctk.CTkToplevel(app)
    cadastro_app.title("Cadastre-se")
    cadastro_app.geometry("400x500")
    cadastro_app.grab_set()  # Bloqueia a interação com a janela principal

    frame_cadastro = ctk.CTkFrame(master=cadastro_app)
    frame_cadastro.pack(pady=20, padx=40, fill="both", expand=True)

    label_titulo_cadastro = ctk.CTkLabel(master=frame_cadastro, text="Cadastro de Usuário", font=("Arial", 20))
    label_titulo_cadastro.pack(pady=12)

    entry_nome_cadastro = ctk.CTkEntry(master=frame_cadastro, placeholder_text="Nome de Usuário")
    entry_nome_cadastro.pack(pady=5, fill="x")

    entry_email_cadastro = ctk.CTkEntry(master=frame_cadastro, placeholder_text="E-mail")
    entry_email_cadastro.pack(pady=5, fill="x")

    # Frame para a senha e botão de olho na tela de cadastro
    frame_senha_cadastro = ctk.CTkFrame(master=frame_cadastro)
    frame_senha_cadastro.pack(pady=5, fill="x")

    entry_senha_cadastro = ctk.CTkEntry(master=frame_senha_cadastro, placeholder_text="Senha", show="*")
    entry_senha_cadastro.pack(side="left", fill="x", expand=True)

    status_senha_cadastro = ctk.CTkLabel(master=frame_senha_cadastro, text="", font=("Arial", 10), text_color="gray")
    status_senha_cadastro.pack(side="top", anchor="e", padx=(0, 5))

    btn_olho_senha_cadastro = ctk.CTkButton(master=frame_senha_cadastro, fg_color="light gray", image=olho_fechado_cinza, text="", width=15, height=2)
    btn_olho_senha_cadastro.pack(side="right", padx=(0, 5))

    # Frame para a confirmação de senha e botão de olho na tela de cadastro
    frame_confirmar_senha_cadastro = ctk.CTkFrame(master=frame_cadastro)
    frame_confirmar_senha_cadastro.pack(pady=5, fill="x")

    entry_confirmar_senha_cadastro = ctk.CTkEntry(master=frame_confirmar_senha_cadastro, placeholder_text="Confirmar Senha", show="*")
    entry_confirmar_senha_cadastro.pack(side="left", fill="x", expand=True)

    status_confirmar_senha_cadastro = ctk.CTkLabel(master=frame_confirmar_senha_cadastro, text="", font=("Arial", 10), text_color="gray")
    status_confirmar_senha_cadastro.pack(side="top", anchor="e", padx=(0, 5))

    btn_olho_confirmar_senha_cadastro = ctk.CTkButton(master=frame_confirmar_senha_cadastro, fg_color="light gray", image=olho_fechado_cinza, text="", width=15, height=2)
    btn_olho_confirmar_senha_cadastro.pack(side="right", padx=(0, 5))

    # Configura o comando do botão de olho para a tela de cadastro
    btn_olho_senha_cadastro.configure(command=lambda: toggle_senha_cadastro(entry_senha_cadastro, entry_confirmar_senha_cadastro, btn_olho_senha_cadastro, btn_olho_confirmar_senha_cadastro, status_senha_cadastro, status_confirmar_senha_cadastro))
    btn_olho_confirmar_senha_cadastro.configure(command=lambda: toggle_senha_cadastro(entry_senha_cadastro, entry_confirmar_senha_cadastro, btn_olho_senha_cadastro, btn_olho_confirmar_senha_cadastro, status_senha_cadastro, status_confirmar_senha_cadastro))

    label_status_cadastro = ctk.CTkLabel(master=frame_cadastro, text="", font=("Arial", 12))
    label_status_cadastro.pack(pady=5)

    def realizar_cadastro():
        username = entry_nome_cadastro.get().strip()
        email = entry_email_cadastro.get().strip()
        password = entry_senha_cadastro.get().strip()
        confirm_password = entry_confirmar_senha_cadastro.get().strip()

        if not username or not email or not password or not confirm_password:
            label_status_cadastro.configure(text="Preencha todos os campos!", text_color="red")
            return

        if not validar_email(email):
            label_status_cadastro.configure(text="E-mail inválido!", text_color="red")
            return

        if password != confirm_password:
            label_status_cadastro.configure(text="As senhas não coincidem!", text_color="red")
            return

        if len(password) < 6:
            label_status_cadastro.configure(text="A senha deve ter pelo menos 6 caracteres!", text_color="red")
            return

        if verificar_usuario_existente(username=username):
            label_status_cadastro.configure(text="Nome de usuário já cadastrado!", text_color="red")
            return

        if verificar_usuario_existente(email=email):
            label_status_cadastro.configure(text="E-mail já cadastrado!", text_color="red")
            return

        salvar_usuario(username, email, password)
        label_status_cadastro.configure(text="Usuário cadastrado com sucesso!", text_color="green")
        # Após o cadastro bem-sucedido, você pode fechar a tela de cadastro
        # e voltar para a tela de login.
        cadastro_app.after(1500, lambda: [cadastro_app.destroy(), app.deiconify()]) # Fecha e volta para tela de login

    btn_cadastrar_novo = ctk.CTkButton(master=frame_cadastro, text="Cadastrar", command=realizar_cadastro)
    btn_cadastrar_novo.pack(pady=10)

    def fechar_cadastro():
        cadastro_app.destroy()
        app.deiconify()  # Mostra a tela de login novamente

    cadastro_app.protocol("WM_DELETE_WINDOW", fechar_cadastro)  # Trata o fechamento da janela


def limitar_entrada(event):
    entry = event.widget
    conteudo = entry.get()
    if len(conteudo) > 13:
        entry.delete(13, ctk.END)

# Criando a interface gráfica
app = ctk.CTk()
app.title("Python em Ação")
app.geometry("350x350")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label_titulo = ctk.CTkLabel(master=frame, text="Python em Ação :\n Fazer Login", font=("Arial", 20))
label_titulo.pack(pady=12)

frame_entradas = ctk.CTkFrame(master=frame)
frame_entradas.pack(pady=5)

entry_usuario = ctk.CTkEntry(master=frame_entradas, placeholder_text="Usuário")
entry_usuario.bind("<KeyRelease>", limitar_entrada)
entry_usuario.grid(row=0, column=0, sticky="ew")

frame_senha = ctk.CTkFrame(master=frame_entradas)
frame_senha.grid(row=1, column=0, sticky="ew", pady=5)

entry_senha = ctk.CTkEntry(master=frame_senha, placeholder_text="Senha", show="*")
entry_senha.bind("<KeyRelease>", limitar_entrada)
entry_senha.grid(row=0, column=0, sticky="ew")

mostrar_senha_button = ctk.CTkButton(master=frame_senha, fg_color="light gray", image=olho_fechado_cinza, text="", width=15, height=2, command=toggle_senha_login, corner_radius=150)
mostrar_senha_button.grid(row=0, column=0, sticky="e", padx=(0, 5))

frame_entradas.columnconfigure(0, weight=1)
frame_senha.columnconfigure(0, weight=1)

btn_login = ctk.CTkButton(master=frame, text="Login", command=login)
btn_login.pack(pady=5)

label_cadastrar = ctk.CTkLabel(master=frame, text="Ainda não tenho conta", font=("Arial", 20))
label_cadastrar.pack(pady=10)

btn_cadastrar = ctk.CTkButton(master=frame, text="Cadastrar", command=tela_cadastro)
btn_cadastrar.pack(padx=5)

label_status = ctk.CTkLabel(master=frame, text="", font=("Arial", 12))
label_status.pack(pady=5)

if __name__ == "__main__":
    app.mainloop()
