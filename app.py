import streamlit as st
import re

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Peça seu Café", page_icon="☕", layout="centered")

# Inicializa o carrinho de compras na memória da sessão
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# 2. BANCO DE DADOS DO CARDÁPIO COM MAPA DE CORES HEXADECIMAIS
# Cada café agora tem sua cor em formato HEX (background limpo e letras legíveis)
cardapio_cafes = {
    "Bala de Mel": {
        "disponivel": True,
        "perfil": "CORPO ALTO / DOÇURA ALTA / FINALIZAÇÃO LONGA",
        "notas": "BALA DE MEL / MALTE / CHOCOLATE",
        "variedade": "MUNDO NOVO",
        "regiao": "SUL / MG",
        "cor_fundo": "#FFF0F5",  # Rosa Claro (LavenderBlush)
        "cor_texto": "#8B0086"
    },
    "Caramelo Selvagem": {
        "disponivel": True,
        "perfil": "DOÇURA ALTA / ACIDEZ BAIXA / CORPO DENSO",
        "notas": "FLOR DE SAL / MALTE TOSTADO",
        "variedade": "BOURBON AMARELO",
        "regiao": "SUL / MG",
        "cor_fundo": "#FFFEE0",  # Amarelo Claro
        "cor_texto": "#8B7300"
    },
    "Lote 86": {
        "disponivel": True,
        "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CREME DE AVELÃ",
        "variedade": "CATUAÍ VERMELHO",
        "regiao": "SUL / MG",
        "cor_fundo": "#FFEBEB",  # Vermelho Claro
        "cor_texto": "#A80000"
    },
    "Salada": {
        "disponivel": True,
        "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ PRESENTE",
        "notas": "BAUNILHA / SALADA DE FRUTAS / FAVO DE MEL",
        "variedade": "MUNDO NOVO",
        "regiao": "SUL / MG",
        "cor_fundo": "#F5F5DC",  # Bege (Beige)
        "cor_texto": "#5C5C40"
    },
    "BS Honey": {
        "disponivel": True,
        "perfil": "CORPO ALTO / DOÇURA ALTA / ACIDEZ BRILHANTE E CÍTRICA / LICOROSO",
        "notas": "RAPADURA / LARANJA / CHOCOLATE",
        "variedade": "CATUCAÍ AMARELO",
        "regiao": "MATAS / MG",
        "cor_fundo": "#F4E7E7",  # Bordô Claro
        "cor_texto": "#800020"   # Bordô / Vinho
    },
    "Caparaó": {
        "disponivel": True,
        "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CASTANHA DE CAJU / CHOCOLATE",
        "variedade": "CATUCAÍ VERMELHO",
        "regiao": "CAPARAÓ / MG",
        "cor_fundo": "#FFECF5",  # Rosa-Choque Suave
        "cor_texto": "#D10074"   # Rosa-Choque Intenso
    },
    "BS Natural": {
        "disponivel": True,
        "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA",
        "notas": "CASTANHA DE CAJU / CHOCOLATE",
        "variedade": "BOURBON AMARELO",
        "regiao": "CAPARAÓ / MG",
        "cor_fundo": "#FFECF5",  
        "cor_texto": "#D10074"
    },
    "Lote 87": {
        "disponivel": True,
        "perfil": "CORPO AVELUDADO / DOÇURA ALTA / ACIDEZ LÁTICA",
        "notas": "BAUNILHA / NOZES / LARANJA",
        "variedade": "CATUAÍ VERMELHO",
        "regiao": "SUL / MG",
        "cor_fundo": "#FDF9E2",  # Mostarda Suave
        "cor_texto": "#A68000"   # Mostarda
    },
    "Santa Rita": {
        "disponivel": True,
        "perfil": "ENCORPADO / DOÇURA ALTA / ACIDEZ LÁTICA",
        "notas": "PAVÊ DE AMEIXA",
        "variedade": "CATUCAÍ AMARELO",
        "regiao": "SUL / MG",
        "cor_fundo": "#E0FFFF",  # Azul-Turquesa Claro
        "cor_texto": "#008B8B"   # Azul-Turquesa Escuro
    },
    "Arara": {
        "disponivel": True,
        "perfil": "CORPO LICOROSO / DOÇURA ALTA / ACIDEZ PRESENTE",
        "notas": "BALA DE MEL / MATE TOSTADO",
        "variedade": "ARARA",
        "regiao": "MOGIANA / SP",
        "cor_fundo": "#E6F7F0",  # Esmeralda Claro
        "cor_texto": "#00875A"   # Esmeralda
    }
}

cafes_disponiveis = [nome for nome, dados in cardapio_cafes.items() if dados["disponivel"]]

# 3. INTERFACE PRINCIPAL
st.title("Peça seu Café")
st.write("Monte seu carrinho de compras escolhendo os sabores abaixo.")
st.markdown("---")

# Menu de seleção do café atual
cafe_escolhido = st.selectbox("Escolha o sabor para adicionar:", cafes_disponiveis)

# Bloco de Destaque Sem Ícones e com Cores Atribuídas Dinamicamente
if cafe_escolhido:
    perfil_atual = cardapio_cafes[cafe_escolhido]["perfil"]
    notas_atuais = cardapio_cafes[cafe_escolhido]["notas"]
    variedade_atual = cardapio_cafes[cafe_escolhido]["variedade"]
    regiao_atual = cardapio_cafes[cafe_escolhido]["regiao"]
    cor_bg = cardapio_cafes[cafe_escolhido]["cor_fundo"]
    cor_tx = cardapio_cafes[cafe_escolhido]["cor_texto"]
    
    st.markdown(
        f"""
        <div style="background-color: {cor_bg}; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid {cor_tx}40;">
            <center>
                <h1 style="font-size: 2.4rem; margin-bottom: 5px; color: {cor_tx}; font-weight: bold; letter-spacing: 1px;">{cafe_escolhido.upper()}</h1>
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

# Opções de Customização do item atual
tipo_moagem = st.radio("Como prefere este café?", ["Grão", "Moído"], horizontal=True)
peso = st.number_input("Volume deste item (g):", min_value=250, max_value=5000, value=250, step=250)

# BOTÃO INTERMEDIÁRIO: ADICIONAR AO CARRINHO
if st.button("🛒 Adicionar ao Carrinho", use_container_width=True):
    item_pedido = {
        "cafe": cafe_escolhido,
        "moagem": tipo_moagem,
        "peso": peso
    }
    st.session_state.carrinho.append(item_pedido)
    st.toast(f"✅ {cafe_escolhido} ({peso}g) adicionado ao carrinho!")

# Botão para limpar o carrinho se o cliente quiser recomeçar
if st.session_state.carrinho:
    if st.button("🗑️ Limpar Carrinho", type="secondary"):
        st.session_state.carrinho = []
        st.rerun()

st.markdown("---")

# 4. EXIBIÇÃO DO CARRINHO E RODAPÉ DINÂMICO
st.subheader("🛒 Seu Carrinho de Compras")

if not st.session_state.carrinho:
    st.info("Seu carrinho está vazio. Adicione pelo menos um café acima.")
    peso_total = 0
else:
    texto_carrinho = ""
    peso_total = 0
    
    for i, item in enumerate(st.session_state.carrinho, 1):
        pacotes_item = item["peso"] // 250
        texto_carrinho += f"🔹 **Item {i}:** {item['cafe']} ({item['moagem']}) — {item['peso']}g ({pacotes_item}x pacotes)\n\n"
        peso_total += item["peso"]
    
    st.markdown(texto_carrinho)
    
    pacotes_totais = peso_total // 250
    st.info(f"⚖️ **RESUMO DO PEDIDO:** \n📦 **Volume Total Somado:** {peso_total}g   \n📦 **Total de Embalagens:** {pacotes_totais}x pacotes de 250g")

st.markdown("---")

# 5. DADOS DE CONTATO
st.subheader("📋 Dados para Finalização")
nome_raw = st.text_input("Seu Nome (Máx 15 letras):", key="nome_input")
nome_valido = "".join(re.findall(r"[a-zA-ZÀ-ÿ\s]", nome_raw))[:15]

telefone_raw = st.text_input("Seu WhatsApp (Apenas números):", placeholder="(XX) 9XXXX-XXXX", key="tel_input")
numeros_tel = "".join(re.findall(r"\d", telefone_raw))[:11]

telefone_mascarado = ""
if len(numeros_tel) > 0:
    if len(numeros_tel) <= 2:
        telefone_mascarado = f"({numeros_tel}"
    elif len(numeros_tel) <= 7:
        telefone_mascarado = f"({numeros_tel[:2]}) {numeros_tel[2:]}"
    else:
        telefone_mascarado = f"({numeros_tel[:2]}) {numeros_tel[2:7]}-{numeros_tel[7:]}"

if nome_raw and nome_raw != nome_valido:
    st.caption(f"📝 Nome ajustado automaticamente: **{nome_valido}**")
if telefone_raw and telefone_raw != telefone_mascarado:
    st.caption(f"📱 Formato da máscara aplicado: **{telefone_mascarado}**")

st.markdown("---")

# 6. BOTÃO DE ENVIO FINAL
if st.button("🔥 Finalizar e Enviar Pedido", use_container_width=True, type="primary"):
    if not st.session_state.carrinho:
        st.error("⚠️ Seu carrinho está vazio! Adicione pelo menos um café antes de finalizar.")
    elif len(nome_valido.strip()) == 0:
        st.warning("⚠️ Por favor, insira um nome válido (apenas letras).")
    elif len(numeros_tel) != 11:
        st.warning("⚠️ Telefone inválido. Certifique-se de preencher o formato completo: (XX) 9XXXX-XXXX.")
    else:
        st.success(f"🎉 Perfeito, {nome_valido}! Seu pedido total de {peso_total}g ({peso_total // 250}x pacotes) foi registrado. Entraremos em contato no {telefone_mascarado}!")
