import streamlit as st
import re

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Peça seu Café", page_icon="☕", layout="centered")

# Definição da senha do Painel Administrativo
SENHA_ADMIN = "CafeADM"

# 2. INICIALIZAÇÃO DO BANCO DE DADOS NA MEMÓRIA DA SESSÃO
if "cardapio" not in st.session_state:
    st.session_state.cardapio = {
        "Bala de Mel": {"disponivel": True, "perfil": "CORPO ALTO / DOÇURA ALTA / FINALIZAÇÃO LONGA", "notas": "BALA DE MEL / MALTE / CHOCOLATE", "variedade": "MUNDO NOVO", "regiao": "SUL / MG", "cor_fundo": "#FFF0F5", "cor_texto": "#8B0086"},
        "Caramelo Selvagem": {"disponivel": True, "perfil": "DOÇURA ALTA / ACIDEZ BAIXA / CORPO DENSO", "notas": "FLOR DE SAL / MALTE TOSTADO", "variedade": "BOURBON AMARELO", "regiao": "SUL / MG", "cor_fundo": "#FFFEE0", "cor_texto": "#8B7300"},
        "Lote 86": {"disponivel": True, "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CREME DE AVELÃ", "variedade": "CATUAÍ VERMELHO", "regiao": "SUL / MG", "cor_fundo": "#FFEBEB", "cor_texto": "#A80000"},
        "Salada": {"disponivel": True, "perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ PRESENTE", "notas": "BAUNILHA / SALADA DE FRUTAS / FAVO DE MEL", "variedade": "MUNDO NOVO", "regiao": "SUL / MG", "cor_fundo": "#F5F5DC", "cor_texto": "#5C5C40"},
        "BS Honey": {"disponivel": True, "perfil": "CORPO ALTO / DOÇURA ALTA / ACIDEZ BRILHANTE E CÍTRICA / LICOROSO", "notas": "RAPADURA / LARANJA / CHOCOLATE", "variedade": "CATUCAÍ AMARELO", "regiao": "MATAS / MG", "cor_fundo": "#F4E7E7", "cor_texto": "#800020"},
        "Caparaó": {"disponivel": True, "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CASTANHA DE CAJU / CHOCOLATE", "variedade": "CATUCAÍ VERMELHO", "regiao": "CAPARAÓ / MG", "cor_fundo": "#FFECF5", "cor_texto": "#D10074"},
        "BS Natural": {"disponivel": True, "perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CASTANHA DE CAJU / CHOCOLATE", "variedade": "BOURBON AMARELO", "regiao": "CAPARAÓ / MG", "cor_fundo": "#FFECF5", "cor_texto": "#D10074"},
        "Lote 87": {"disponivel": True, "perfil": "CORPO AVELUDADO / DOÇURA ALTA / ACIDEZ LÁTICA", "notas": "BAUNILHA / NOZES / LARANJA", "variedade": "CATUAÍ VERMELHO", "regiao": "SUL / MG", "cor_fundo": "#FDF9E2", "cor_texto": "#A68000"},
        "Santa Rita": {"disponivel": True, "perfil": "ENCORPADO / DOÇURA ALTA / ACIDEZ LÁTICA", "notas": "PAVÊ DE AMEIXA", "variedade": "CATUCAÍ AMARELO", "regiao": "SUL / MG", "cor_fundo": "#E0FFFF", "cor_texto": "#008B8B"},
        "Arara": {"disponivel": True, "perfil": "CORPO LICOROSO / DOÇURA ALTA / ACIDEZ PRESENTE", "notas": "BALA DE MEL / MATE TOSTADO", "variedade": "ARARA", "regiao": "MOGIANA / SP", "cor_fundo": "#E6F7F0", "cor_texto": "#00875A"}
    }
}

if "historico_pedidos" not in st.session_state:
    st.session_state.historico_pedidos = []

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# 3. BARRA LATERAL (ACESSO DO ADMINISTRADOR)
st.sidebar.title("🔐 Área Restrita")
senha_digitada = st.sidebar.text_input("Senha do Administrador:", type="password", key="senha_admin_input")

is_admin = (senha_digitada == SENHA_ADMIN)

# --- VISÃO DO ADMINISTRADOR ---
if is_admin:
    st.sidebar.success("Modo Admin Ativo")
    st.title("🛠️ Painel de Controle Administrativo")
    st.write("Gerencie a disponibilidade do menu e visualize os pedidos.")
    
    st.subheader("📋 Controle de Disponibilidade do Cardápio")
    for sabor, dados in st.session_state.cardapio.items():
        status_novo = st.toggle(f"Disponível: {sabor}", value=dados["disponivel"], key=f"toggle_{sabor}")
        if status_novo != dados["disponivel"]:
            st.session_state.cardapio[sabor]["disponivel"] = status_novo
            st.rerun()
        
    st.markdown("---")
    
    st.subheader("📦 Histórico de Pedidos")
    if not st.session_state.historico_pedidos:
        st.info("Nenhum pedido recebido ainda.")
    else:
        for idx, ped in enumerate(st.session_state.historico_pedidos, 1):
            with st.expander(f"Pedido #{idx} - {ped['nome']}"):
                st.write(f"**Cliente:** {ped['nome']}")
                st.write(f"**Contato:** {ped['telefone']}")
                st.write("**Itens encomendados:**")
                for item in ped["itens"]:
                    st.write(f"• {item['cafe']} ({item['moagem']}) — {item['peso']}g")
                    
    if st.sidebar.button("Sair do Modo Admin"):
        st.session_state.senha_admin_input = ""
        st.rerun()

# --- VISÃO DO CLIENTE ---
else:
    cafes_disponiveis = [nome for nome, dados in st.session_state.cardapio.items() if dados["disponivel"]]

    st.title("Peça seu Café")
    st.write("Monte seu carrinho de compras escolhendo os sabores abaixo.")
    st.markdown("---")

    if not cafes_disponiveis:
        st.warning("⚠️ Desculpe, todos os nossos cafés estão temporariamente esgotados!")
    else:
        cafe_escolhido = st.selectbox("Escolha o sabor para adicionar:", cafes_disponiveis)

        if cafe_escolhido:
            dados_cafe = st.session_state.cardapio[cafe_escolhido]
            st.markdown(
                f"""
                <div style="background-color: {dados_cafe['cor_fundo']}; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid {dados_cafe['cor_texto']}40;">
                    <center>
                        <h1 style="font-size: 2.4rem; margin-bottom: 5px; color: {dados_cafe['cor_texto']}; font-weight: bold; letter-spacing: 1px;">{cafe_escolhido.upper()}</h1>
                        <p style="font-size: 0.95rem; margin-top: 12px; color: #444444; font-weight: bold;">PERFIL: {dados_cafe['perfil']}</p>
                        <p style="font-size: 0.9rem; margin-top: -5px; color: #666666;">NOTAS SENSORIAIS: {dados_cafe['notas']}</p>
                        <p style="font-size: 0.85rem; margin-top: -5px; color: #777777; font-style: italic;">VARIEDADE: {dados_cafe['variedade']}</p>
                        <p style="font-size: 0.85rem; margin-top: -5px; color: #888888; letter-spacing: 1px; font-weight: 500;">REGIÃO: {dados_cafe['regiao']}</p>
                    </center>
                </div>
                """, 
                unsafe_allow_html=True
            )

        tipo_moagem = st.radio("Como prefere este café?", ["Grão", "Moído"], horizontal=True)
        peso = st.number_input("Volume deste item (g):", min_value=250, max_value=5000, value=250, step=250)

        if st.button("🛒 Adicionar ao Carrinho", use_container_width=True):
            st.session_state.carrinho.append({"cafe": cafe_escolhido, "moagem": tipo_moagem, "peso": peso})
            st.toast(f"✅ {cafe_escolhido} adicionado!")

        if st.session_state.carrinho:
            if st.button("🗑️ Limpar Carrinho", type="secondary"):
                st.session_state.carrinho = []
                st.rerun()

        st.markdown("---")
        st.subheader("🛒 Seu Carrinho de Compras")

        if not st.session_state.carrinho:
            st.info("Seu carrinho está vazio.")
            peso_total = 0
        else:
            peso_total = 0
            for i, item in enumerate(st.session_state.carrinho, 1):
                st.markdown(f"🔹 **Item {i}:** {item['cafe']} ({item['moagem']}) — {item['peso']}g")
                peso_total += item["peso"]
            
            st.info(f"⚖️ **RESUMO:** \n📦 **Volume Total:** {peso_total}g ({peso_total // 250}x pacotes de 250g)")

        st.markdown("---")
        st.subheader("📋 Dados para Finalização")
        
        # NOME: Força o limite de 15 caracteres no teclado e transforma tudo em CAIXA ALTA (.upper())
        nome_raw = st.text_input("Seu Nome (Máx 15 letras):", max_chars=15, key="nome_input")
        nome_valido = "".join(re.findall(r"[a-zA-ZÀ-ÿ\s]", nome_raw)).upper()

        # TELEFONE: Força o limite estrito de 11 dígitos numéricos
        telefone_raw = st.text_input("Seu WhatsApp (Apenas os 11 números com DDD):", max_chars=11, placeholder="319XXXXXXXX", key="tel_input")
        numeros_tel = "".join(re.findall(r"\d", telefone_raw))

        # Aplica a máscara visual rigidamente se o cara digitou os 11 números certos
        if len(numeros_tel) == 11:
            telefone_mascarado = f"({numeros_tel[:2]}) {numeros_tel[2:3]}{numeros_tel[3:7]}-{numeros_tel[7:]}"
        else:
            telefone_mascarado = ""

        # Feedbacks visuais em tempo real abaixo das caixas
        if nome_raw and nome_raw != nome_valido:
            st.caption(f"📝 Nome formatado: **{nome_valido}**")
            
        if telefone_raw:
            if len(numeros_tel) != len(telefone_raw):
                st.caption("⚠️ **Apenas números são aceitos neste campo!**")
            elif len(numeros_tel) == 11:
                st.caption(f"📱 Formato aplicado: **{telefone_mascarado}**")

        if st.button("🔥 Finalizar e Enviar Pedido", use_container_width=True, type="primary"):
            if not st.session_state.carrinho:
                st.error("⚠️ Seu carrinho está vazio!")
            elif len(nome_valido.strip()) == 0:
                st.warning("⚠️ Insira um nome válido (apenas letras).")
            elif len(numeros_tel) != 11:
                st.warning("⚠️ O telefone precisa ter exatamente 11 números (DDD + 9 dígitos).")
            else:
                novo_pedido = {
                    "nome": nome_valido,
                    "telefone": telefone_mascarado,
                    "itens": list(st.session_state.carrinho)
                }
                st.session_state.historico_pedidos.append(novo_pedido)
                st.success(f"🎉 Perfeito! O pedido de {nome_valido} foi registrado com o contato {telefone_mascarado}.")
                st.session_state.carrinho = []
