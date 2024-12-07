import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import os

# Inicializando o DataFrame na sessão
if "people_data" not in st.session_state:
    st.session_state["people_data"] = pd.DataFrame(columns=["Nome", "Sobrenome", "E-mail", "Telefone", "Foto"])

# Título do app
st.title("Cadastro de Identificação de Pessoas")

# Pasta para salvar fotos
photo_dir = "photos"
os.makedirs(photo_dir, exist_ok=True)  # Cria o diretório se não existir

# Função para capturar a foto com a webcam
def capture_photo():
    cam = cv2.VideoCapture(0)  # Inicializa a webcam
    st.warning("Pressione a tecla 's' para salvar a foto e 'q' para sair.")
    
    img_captured = None
    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            st.error("Não foi possível acessar a câmera.")
            break
        cv2.imshow("Tire sua foto (Pressione 's' para salvar)", frame)

        # Captura o input do teclado
        key = cv2.waitKey(1)
        if key == ord("s"):  # Tecla 's' para salvar a foto
            img_captured = frame
            break
        elif key == ord("q"):  # Tecla 'q' para sair sem salvar
            break

    cam.release()
    cv2.destroyAllWindows()
    return img_captured

# Entrada de dados do formulário
with st.form("Cadastro de Pessoa"):
    st.subheader("Preencha as informações abaixo:")
    nome = st.text_input("Nome:")
    sobrenome = st.text_input("Sobrenome:")
    email = st.text_input("E-mail:")
    telefone = st.text_input("Telefone:")
    tirar_foto = st.checkbox("Deseja tirar uma foto?")
    salvar = st.form_submit_button("Salvar")

foto_path = None
if salvar:
    if nome and sobrenome and email and telefone:  # Verifica se os campos obrigatórios estão preenchidos
        if tirar_foto:
            st.info("Abrindo a câmera para tirar a foto...")
            photo = capture_photo()
            if photo is not None:
                # Salva a foto no diretório local
                foto_path = os.path.join(photo_dir, f"{nome}_{sobrenome}.jpg")
                cv2.imwrite(foto_path, photo)
                st.success(f"Foto salva com sucesso em {foto_path}!")
            else:
                st.warning("Nenhuma foto foi capturada.")
        
        # Adiciona os dados ao DataFrame da sessão
        new_entry = {
            "Nome": nome,
            "Sobrenome": sobrenome,
            "E-mail": email,
            "Telefone": telefone,
            "Foto": foto_path if foto_path else None,
        }
        st.session_state["people_data"] = pd.concat(
            [st.session_state["people_data"], pd.DataFrame([new_entry])], ignore_index=True
        )
        st.success("Cadastro salvo com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos obrigatórios!")

# Exibindo os dados cadastrados
st.subheader("Pessoas Cadastradas:")
if not st.session_state["people_data"].empty:
    # Exibindo dados na tabela com fotos
    for index, row in st.session_state["people_data"].iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            if row["Foto"] and os.path.exists(row["Foto"]):
                image = Image.open(row["Foto"])
                st.image(image, caption=row["Nome"], width=100)
            else:
                st.text("Sem Foto")
        with col2:
            st.write(f"**Nome:** {row['Nome']} {row['Sobrenome']}")
            st.write(f"**E-mail:** {row['E-mail']}")
            st.write(f"**Telefone:** {row['Telefone']}")
        st.write("---")
else:
    st.info("Nenhuma pessoa cadastrada ainda.")
