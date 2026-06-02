import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Café Especial", page_icon="☕", layout="centered")

# 2. BANCO DE DADOS DO CARDÁPIO
cardapio_cafes = {
    "Bala de Mel": {
        "disponivel": True,
        "perfil": "CORPO ALTO / DOÇURA ALTA / FINALIZAÇÃO LONGA",
        "notas": "BALA DE MEL / MALTE / CHOCOLATE",
        "regiao": "SUL / MG"
    },
    "Bourbon Amarelo": {
        "disponivel": True,
        "perfil": "CORPO MÉDIO / ACIDEZ CÍTRICA TRABALHADA",
        "notas": "RAPADURA / FRUTAS AMARELAS",
        "regiao": "CERRADO MINEIRO"
    },
    "Geisha Gourmet": {
        "disponivel": False, 
        "perfil": "CORPO LEVE / NOTAS FLORAIS / JASMIM",
        "notas": "FLORES BRANCAS / LIMÃO SICILIANO",
        "regiao": "MANTIQUEIRA DE MINAS"
    }
}

# Filtra os cafés disponíveis
cafes_disponiveis = [nome for nome, dados in cardapio_cafes.items() if dados["disponivel"]]

# 3. INTERFACE E ENTRADA DE DADOS (INPUTS)
st.title("☕ Central de Pedidos de Café")
st.write("Escolha suas preferências e monte seu pedido abaixo.")
st.markdown("---")

cafe_escolhido = st.selectbox("Escolha o sabor disponível:", cafes_disponiveis)

# Bloco Destaque Centralizado do Café
if cafe_escolhido:
    perfil_atual = cardapio_cafes[cafe_escolhido]["perfil"]
    notas_atuais = cardapio_cafes[cafe_escolhido]["notas"]
    regiao_atual = cardapio_cafes[cafe_escolhido]["regiao"]
    
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #eeeeee;">
            <center>
                <h1 style="font-size: 2.3rem; margin-bottom: 0px; color: #333333;">✨ {cafe_escolhido.upper()} ✨</h1>
                <p style="font-size: 0.95rem; margin-top: 10px; color: #555555; font-weight: bold;">
                    PERFIL: {perfil_atual}
                </p>
                <p style="font-size: 0.9rem; margin-top: -5px; color: #666666;">
                    NOTAS SENSORIAIS: {notas_atuais}
                </p>
                <p style="font-size: 0.85rem; margin-top: -5px; color: #888888; letter-spacing: 1px;">
                    REGIÃO: {regiao_atual}
                </p>
            </center>
        </div>
        """, 
        unsafe_allow_html=True
    )

tipo_moagem = st.radio("Como prefere o seu café?", ["Grão", "Moído"], horizontal=True)
peso = st.number_input("Volume desejado (g):", min_value=250, max_value=5000, value=250, step=250)

st.markdown("---")
st.subheader("📋 Dados de Contato")
nome = st.text_input("Seu Nome Completo:")
telefone = st.text_input("Seu WhatsApp:")

st.markdown("---")

# 4. RODAPÉ DINÂMICO (CÁLCULOS E RESUMO)
pacotes_de_250 = peso // 250

st.markdown("### 🛒 Detalhe do Pedido")
st.info(f"☕ **Café:** {cafe_escolhido}   \n⚙️ **Tipo:** {tipo_moagem}   \n⚖️ **Volume Total:** {peso}g ({pacotes_de_250}x pacotes de 250g)")

# 5. BOTÃO DE ENVIO
if st.button("Confirmar e Enviar Pedido", use_container_width=True):
    if nome and telefone:
        st.success(f"🎉 Sucesso! Pedido de {nome} registrado ({peso}g de {cafe_escolhido}). Entraremos em contato no {telefone}!")
    else:
        st.warning("⚠️ Atenção: Nome e Telefone são obrigatórios para fechar o pedido.")