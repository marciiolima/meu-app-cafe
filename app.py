import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Cafés Especiais", page_icon="☕", layout="centered")

# 2. BANCO DE DADOS DO CARDÁPIO (ATUALIZADO)
cardapio_cafes = {
    "Bala de Mel": {
        "disponivel": True,
        "perfil": "CORPO ALTO / DOÇURA ALTA / FINALIZAÇÃO LONGA",
        "notas": "BALA DE MEL / MALTE / CHOCOLATE",
        "variedade": "MUNDO NOVO",
        "regiao": "SUL / MG"
    },
    "Caramelo Selvagem": {
        "disponivel": True,
        "perfil": "DOÇURA ALTA / ACIDEZ BAIXA / CORPO DENSO",
        "notas": "FLOR DE SAL / MALTE TOSTADO",
        "variedade": "BOURBON AMARELO",
        "regiao": "SUL / MG"
    },
    "Lote 86": {
        "disponivel": True,
        "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CREME DE AVELÃ",
        "variedade": "CATUAÍ VERMELHO",
        "regiao": "SUL / MG"
    },
    "Salada": {
        "disponivel": True,
        "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ PRESENTE",
        "notas": "BAUNILHA / SALADA DE FRUTAS / FAVO DE MEL",
        "variedade": "MUNDO NOVO",
        "regiao": "SUL / MG"
    },
    "BS Honey": {
        "disponivel": True,
        "perfil": "CORPO ALTO / DOÇURA ALTA / ACIDEZ BRILHANTE E CÍTRICA / LICOROSO",
        "notas": "RAPADURA / LARANJA / CHOCOLATE",
        "variedade": "CATUCAÍ AMARELO",
        "regiao": "MATAS / MG"
    },
    "Caparaó": {
        "disponivel": True,
        "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CASTANHA DE CAJU / CHOCOLATE",
        "variedade": "CATUCAÍ VERMELHO",
        "regiao": "CAPARAÓ / MG"
    },
    "BS Natural": {
        "disponivel": True,
        "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CASTANHA DE CAJU / CHOCOLATE",
        "variedade": "BOURBON AMARELO",
        "regiao": "CAPARAÓ / MG"
    },
    "Lote 87": {
        "disponivel": True,
        "perfil": "CORPO AVELUDADO / DOÇURA ALTA / ACIDEZ LÁTICA",
        "notas": "BAUNILHA / NOZES / LARANJA",
        "variedade": "CATUAÍ VERMELHO",
        "regiao": "SUL / MG"
    },
    "Santa Rita": {
        "disponivel": True,
        "perfil": "ENCORPADO / DOÇURA ALTA / ACIDEZ LÁTICA",
        "notas": "PAVÊ DE AMEIXA",
        "variedade": "CATUCAÍ AMARELO",
        "regiao": "SUL / MG"
    },
    "Arara": {
        "disponivel": True,
        "perfil": "CORPO LICOROSO / DOÇURA ALTA / ACIDEZ PRESENTE",
        "notas": "BALA DE MEL / MATE TOSTADO",
        "variedade": "ARARA",
        "regiao": "MOGIANA / SP"
    }
}

# Filtra dinamicamente apenas os cafés que estão marcados com disponivel: True
cafes_disponiveis = [nome for nome, dados in cardapio_cafes.items() if dados["disponivel"]]

# 3. INTERFACE PRINCIPAL
st.title("☕ Central de Pedidos de Café")
st.write("Escolha suas preferências e monte seu pedido abaixo.")
st.markdown("---")

# Menu de seleção
cafe_escolhido = st.selectbox("Escolha o sabor disponível:", cafes_disponiveis)

# Bloco de Destaque Centralizado do Café Selecionado
if cafe_escolhido:
    perfil_atual = cardapio_cafes[cafe_escolhido]["perfil"]
    notas_atuais = cardapio_cafes[cafe_escolhido]["notas"]
    variedade_atual = cardapio_cafes[cafe_escolhido]["variedade"]
    regiao_atual = cardapio_cafes[cafe_escolhido]["regiao"]
    
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #eeeeee;">
            <center>
                <h1 style="font-size: 2.4rem; margin-bottom: 5px; color: #222222; font-weight: bold; letter-spacing: 1px;">✨ {cafe_escolhido.upper()} ✨</h1>
                <p style="font-size: 0.95rem; margin-top: 12px; color: #444444; font-weight: bold;">
                    PERFIL: {perfil_atual}
                </p>
                <p style="font-size: 0.9rem; margin-top: -5px; color: #666666;">
                    NOTAS SENSORIAIS: {notas_atuais}
                </p>
                <p style="font-size: 0.85rem; margin-top: -5px; color: #777777; font-style: italic;">
                    VARIEDADE: {variedade_atual}
                </p>
                <p style="font-size: 0.85rem; margin-top: -5px; color: #888888; letter-spacing: 1px; font-weight: 500;">
                    REGIÃO: {regiao_atual}
                </p>
            </center>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Opções de Customização do Pedido
tipo_moagem = st.radio("Como prefere o seu café?", ["Grão", "Moído"], horizontal=True)
peso = st.number_input("Volume desejado (g):", min_value=250, max_value=5000, value=250, step=250)

st.markdown("---")
st.subheader("📋 Dados de Contato")
nome = st.text_input("Seu Nome Completo:")
telefone = st.text_input("Seu WhatsApp:")

st.markdown("---")

# 4. RODAPÉ DINÂMICO (CÁLCULO DE MÚLTIPLOS)
pacotes_de_250 = peso // 250

st.markdown("### 🛒 Detalhe do Pedido")
st.info(f"☕ **Café:** {cafe_escolhido}   \n⚙️ **Tipo:** {tipo_moagem}   \n⚖️ **Volume Total:** {peso}g ({pacotes_de_250}x pacotes de 250g)")

# 5. BOTÃO DE CONFIRMAÇÃO
if st.button("Confirmar e Enviar Pedido", use_container_width=True):
    if nome and telefone:
        st.success(f"🎉 Sucesso! Pedido de {nome} registrado ({peso}g de {cafe_escolhido}). Entraremos em contato no {telefone}!")
    else:
        st.warning("⚠️ Atenção: Nome e Telefone são obrigatórios para fechar o pedido.")
