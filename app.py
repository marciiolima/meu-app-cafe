import streamlit as st
import re
import pandas as pd
from supabase import create_client, Client

# 1. CONFIGURAÇÃO DA PÁGINA E CONEXÃO COM SUPABASE
st.set_page_config(page_title="Peça seu Café", page_icon="☕", layout="centered")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

SENHA_ADMIN = "CafeADM"
CHAVE_PIX_EMAIL = "marciiolima@gmail.com"

# Inicialização de estados do sistema
if "login_admin" not in st.session_state:
    st.session_state.login_admin = False
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "etapa_venda" not in st.session_state:
    st.session_state.etapa_venda = "carrinho"

# 2. DICIONÁRIO ESTRUTURADO DOS CAFÉS
DETALHES_CAFES = {
    "Bala de Mel": {"perfil": "CORPO ALTO / DOÇURA ALTA / FINALIZAÇÃO LONGA", "notas": "BALA DE MEL / MALTE / CHOCOLATE", "variedade": "MUNDO NOVO", "regiao": "SUL / MG", "cor_fundo": "#FFF0F5", "cor_texto": "#8B0086"},
    "Caramelo Selvagem": {"perfil": "DOÇURA ALTA / ACIDEZ BAIXA / CORPO DENSO", "notas": "FLOR DE SAL / MALTE TOSTADO", "variedade": "BOURBON AMARELO", "regiao": "SUL / MG", "cor_fundo": "#FFFEE0", "cor_texto": "#8B7300"},
    "Lote 86": {"perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CREME DE AVELÃ", "variedade": "CATUAÍ VERMELHO", "regiao": "SUL / MG", "cor_fundo": "#FFEBEB", "cor_texto": "#A80000"},
    "Salada": {"perfil": "CORPO SEDOSO / DOÇURA ALTA / ACIDEZ PRESENTE", "notas": "BAUNILHA / SALADA DE FRUTAS / FAVO DE MEL", "variedade": "MUNDO NOVO", "regiao": "SUL / MG", "cor_fundo": "#F5F5DC", "cor_texto": "#5C5C40"},
    "BS Honey": {"perfil": "CORPO ALTO / DOÇURA ALTA / ACIDEZ BRILHANTE E CÍTRICA / LICOROSO", "notas": "RAPADURA / LARANJA / CHOCOLATE", "variedade": "CATUCAÍ AMARELO", "regiao": "MATAS / MG", "cor_fundo": "#F4E7E7", "cor_texto": "#800020"},
    "Caparaó": {"perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CASTANHA DE CAJU / CHOCOLATE", "variedade": "CATUCAÍ VERMELHO", "regiao": "CAPARAÓ / MG", "cor_fundo": "#FFECF5", "cor_texto": "#D10074"},
    "BS Natural": {"perfil": "CORPO AMANTEIGADO / DOÇURA ALTA / ACIDEZ BAIXA", "notas": "CASTANHA DE CAJU / CHOCOLATE", "variedade": "BOURBON AMARELO", "regiao": "CAPARAÓ / MG", "cor_fundo": "#FFECF5", "cor_texto": "#D10074"},
    "Lote 87": {"perfil": "CORPO AVELUDADO / DOÇURA ALTA / ACIDEZ LÁTICA", "notas": "BAUNILHA / NOZES / LARANJA", "variedade": "CATUAÍ VERVELHO", "regiao": "SUL / MG", "cor_fundo": "#FDF9E2", "cor_texto": "#A68000"},
    "Santa Rita": {"perfil": "ENCORPADO / DOÇURA ALTA / ACIDEZ LÁTICA", "notas": "PAVÊ DE AMEIXA", "variedade": "CATUCAÍ AMARELO", "regiao": "SUL / MG", "cor_fundo": "#E0FFFF", "cor_texto": "#008B8B"},
    "Arara": {"perfil": "CORPO LICOROSO / DOÇURA ALTA / ACIDEZ PRESENTE", "notas": "BALA DE MEL / MATE TOSTADO", "variedade": "ARARA", "regiao": "MOGIANA / SP", "cor_fundo": "#E6F7F0", "cor_texto": "#00875A"}
}

def carregar_disponibilidade_banco():
    try:
        # Busca usando os novos nomes de coluna criados
        dados = supabase.table("cardapio").select("column_sabor, column_disponivel").execute().data
        return {item["column_sabor"]: item["column_disponivel"] for item in dados}
    except Exception as e:
        # Se der erro ou a tabela estiver vazia, assume que todos estão disponíveis
        return {sabor: True for sabor in DETALHES_CAFES.keys()}

def deslogar_admin():
    st.session_state.login_admin = False
    st.session_state.senha_admin_input = ""

# 3. BARRA LATERAL (AUTENTICAÇÃO)
st.sidebar.title("🔐 Área Restrita")
if not st.session_state.login_admin:
    senha_digitada = st.sidebar.text_input("Senha do Administrador:", type="password", key="senha_admin_input")
    if senha_digitada == SENHA_ADMIN:
        st.session_state.login_admin = True
        st.rerun()

# --- VISÃO DO ADMINISTRADOR ---
if st.session_state.login_admin:
    st.sidebar.success("Modo Admin Ativo")
    st.title("🛠️ Painel de Controle Administrativo")
    
    st.subheader("📋 Controle de Disponibilidade")
    status_atual_banco = carregar_disponibilidade_banco()
    
    novos_status = {}
    for sabor in DETALHES_CAFES.keys():
        status_inicial = status_atual_banco.get(sabor, True)
        novos_status[sabor] = st.toggle(f"Disponível: {sabor}", value=status_inicial, key=f"toggle_{sabor}")
        
    if st.button("💾 Salvar Alterações do Cardápio", type="primary", use_container_width=True):
        try:
            # Upsert funciona perfeitamente agora que column_sabor é Primary Key
            lista_updates = [
                {"column_sabor": sabor, "column_disponivel": disp} 
                for sabor, disp in novos_status.items()
            ]
            supabase.table("cardapio").upsert(lista_updates).execute()
            
            st.success("🎉 Alterações gravadas permanentemente no Supabase!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar disponibilidade no Supabase: {e}")
        
    st.markdown("---")
    st.subheader("📊 Relatório Consolidado para Envase (PCP)")
    
    resposta = supabase.table("pedidos").select("*").order("created_at", desc=True).execute()
    pedidos_banco = resposta.data

    if not pedidos_banco:
        st.info("Nenhum pedido registrado.")
    else:
        lista_itens_completos = []
        for ped in pedidos_banco:
            nome_cliente = ped.get("column_nome", "DESCONHECIDO")
            
            for item in ped["column_itens"]:
                if "tag_financeira" in item:
                    continue
                peso_unitario = item.get("tamanho_embalagem", item.get("peso", 250))
                quantidade = item.get("quantidade", 1)
                lista_itens_completos.append({
                    "Cliente": nome_cliente,
                    "Sabor": item["cafe"],
                    "Tipo (Moagem)": item["moagem"],
                    "Embalagem": f"{peso_unitario}g",
                    "Qtd de Pacotes": quantidade
                })
        
        if lista_itens_completos:
            df = pd.DataFrame(lista_itens_completos)
            df_agrupado = df.groupby(["Cliente", "Sabor", "Tipo (Moagem)", "Embalagem"]).sum().reset_index()
            st.dataframe(df_agrupado, use_container_width=True, hide_index=True)
            
            csv_data = df_agrupado.to_csv(index=False, sep=";", encoding="utf-8-sig")
            st.download_button(label="📥 Baixar Ordem de Envase (CSV)", data=csv_data, file_name="ordem_envase.csv", mime="text/csv", use_container_width=True)
        else:
            st.info("Nenhum pacote de café pendente nos pedidos atuais.")
        
    st.markdown("---")
    st.sidebar.button("Sair do Modo Admin", type="secondary", on_click=deslogar_admin, use_container_width=True)

# --- VISÃO DO CLIENTE ---
else:
    status_banco = carregar_disponibilidade_banco()
    cafes_disponiveis = [nome for nome in DETALHES_CAFES.keys() if status_banco.get(nome, True)]

    # --- ETAPA 1: MONTAR CARRINHO ---
    if st.session_state.etapa_venda == "carrinho":
        st.title("Peça seu Café")
        st.write("Monte seu carrinho de compras escolhendo os sabores abaixo.")
        st.markdown("---")

        if not cafes_disponiveis:
            st.warning("⚠️ Desculpe, todos os nossos cafés estão temporariamente esgotados!")
        else:
            cafe_escolhido = st.selectbox("Escolha o sabor para adicionar:", cafes_disponiveis)

            if cafe_escolhido:
                dados_cafe = DETALHES_CAFES[cafe_escolhido]
                st.markdown(
                    f"""
                    <div style="background-color: {dados_cafe['cor_fundo']}; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid {dados_cafe['cor_texto']}40;">
                        <center>
                            <h1 style="font-size: 2.4rem; margin-bottom: 5px; color: {dados_cafe['cor_texto']}; font-weight: bold; letter-spacing: 1px;">{cafe_escolhido.upper()}</h1>
                            <p style="font-size: 0.95rem; margin-top: 12px; color: #444444; font-weight: bold;">PERFIL: {dados_cafe['perfil']}</p>
                            <p style="font-size: 0.9rem; margin-top: -5px; color: #666666;">NOTAS SENSORIAIS: {dados_cafe['notas']}</p>
                        </center>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            tipo_moagem = st.radio("Como prefere este café?", ["Grão", "Moído"], horizontal=True)
            col1, col2 = st.columns(2)
            with col1:
                tamanho_embalagem = st.selectbox("Tamanho da embalagem:", [250, 500], format_func=lambda x: f"Pacote de {x}g")
            with col2:
                quantidade_pacotes = st.number_input("Quantidade de pacotes:", min_value=1, max_value=50, value=1, step=1)

            if st.button("🛒 Adicionar ao Carrinho", use_container_width=True):
                st.session_state.carrinho.append({
                    "cafe": cafe_escolhido, 
                    "moagem": tipo_moagem, 
                    "tamanho_embalagem": tamanho_embalagem,
                    "quantidade": quantidade_pacotes
                })
                st.toast(f"✅ Adicionado ao carrinho!")

            if st.session_state.carrinho:
                if st.button("🗑️ Limpar Carrinho", type="secondary"):
                    st.session_state.carrinho = []
                    st.rerun()

            st.markdown("---")
            st.subheader("🛒 Seu Carrinho de Compras")

            if not st.session_state.carrinho:
                st.info("Seu carrinho está vazio.")
            else:
                total_geral_peso = 0
                for i, item in enumerate(st.session_state.carrinho, 1):
                    tamanho = item["tamanho_embalagem"]
                    qtd = item["quantidade"]
                    st.markdown(f"🔹 **Item {i}:** {qtd}x pacote(s) de {tamanho}g — {item['cafe']} ({item['moagem']})")
                    total_geral_peso += (tamanho * qtd)
                
                peso_kg = total_geral_peso / 1000
                
                if peso_kg <= 1.0:
                    preco_por_kg = 102
                elif peso_kg <= 2.0:
                    preco_por_kg = 96
                else:
                    preco_por_kg = 95
                
                subtotal = peso_kg * preco_por_kg
                st.info(f"⚖️ Resumo Atual: {total_geral_peso}g ({peso_kg:.2f} kg) \n💵 Preço da faixa: R$ {preco_por_kg:.2f}/kg | Subtotal: R$ {subtotal:.2f}")

            st.markdown("---")
            st.subheader("📋 Dados de Contato e Envio")
            nome_raw = st.text_input("Seu Nome:", max_chars=15, key="nome_input")
            nome_valido = "".join(re.findall(r"[a-zA-ZÀ-ÿ\s]", nome_raw)).upper()

            telefone_raw = st.text_input("Seu WhatsApp (com DDD):", max_chars=11, placeholder="319XXXXXXXX", key="tel_input")
            numeros_tel = "".join(re.findall(r"\d", telefone_raw))

            if len(numeros_tel) == 11:
                telefone_mascarado = f"({numeros_tel[:2]}) {numeros_tel[2:3]}{numeros_tel[3:7]}-{numeros_tel[7:]}"
            else:
                telefone_mascarado = ""

            if st.button("💳 Avançar para o Pagamento", use_container_width=True, type="primary"):
                if not st.session_state.carrinho:
                    st.error("⚠️ Seu carrinho está vazio!")
                elif len(nome_valido.strip()) == 0:
                    st.warning("⚠️ Insira um nome válido.")
                elif len(numeros_tel) != 11:
                    st.warning("⚠️ O telefone precisa ter 11 números.")
                else:
                    st.session_state.dados_cliente_temp = {
                        "nome": nome_valido,
                        "telefone": telefone_mascarado
                    }
                    st.session_state.etapa_venda = "pagamento"
                    st.rerun()

    # --- ETAPA 2: TELA DE PAGAMENTO ---
    elif st.session_state.etapa_venda == "pagamento":
        st.title("💳 Fechamento do Pedido e Pagamento")
        st.write("Confira os valores e faça a transferência PIX para concluir seu pedido.")
        st.markdown("---")
        
        cliente = st.session_state.dados_cliente_temp
        
        total_geral_peso = sum(item["tamanho_embalagem"] * item["quantidade"] for item in st.session_state.carrinho)
        peso_kg = total_geral_peso / 1000
        
        if peso_kg <= 1.0:
            preco_por_kg = 102
            faixa_nome = "Até 1kg (Padrão)"
        elif peso_kg <= 2.0:
            preco_por_kg = 96
            faixa_nome = "Mais de 1kg (Desconto)"
        else:
            preco_por_kg = 95
            faixa_nome = "Mais de 2kg (Atacado)"
            
        valor_cafe = peso_kg * preco_por_kg
        frete = 2.00
        valor_total = valor_cafe + frete
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📋 Resumo do Pedido")
            st.write(f"**Cliente:** {cliente['nome']}")
            st.write(f"**WhatsApp:** {cliente['telefone']}")
            st.write(f"**Peso Total:** {peso_kg:.2f} kg ({total_geral_peso}g)")
            
        with col2:
            st.markdown("### 💰 Cálculo do Valor")
            st.write(f"**Faixa aplicada:** {faixa_nome}")
            st.write(f"**Preço do quilo:** R$ {preco_por_kg:.2f}/kg")
            st.write(f"**Subtotal do Café:** R$ {valor_cafe:.2f}")
            st.write(f"**Taxa de Frete:** R$ {frete:.2f}")
            st.write(f"### **Valor Total: R$ {valor_total:.2f}**")
            
        st.markdown("---")
        
        st.subheader("🔑 Pagamento via PIX")
        st.warning(f"🚨 **VALOR EXATO A TRANSFERIR:** R$ {valor_total:.2f}\n\n**CHAVE PIX (E-MAIL):** {CHAVE_PIX_EMAIL}")
        st.info("Abra o aplicativo do seu banco, escolha transferir por chave PIX E-mail e digite o endereço acima.")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ Voltar e Alterar Itens", use_container_width=True):
                st.session_state.etapa_venda = "carrinho"
                st.rerun()
                
        with c2:
            if st.button("🔥 Confirmar e Finalizar Pedido", use_container_width=True, type="primary"):
                
                itens_com_metadados = list(st.session_state.carrinho)
                itens_com_metadados.append({
                    "tag_financeira": True,
                    "valor_total_pedido": valor_total,
                    "frete_incluso": frete,
                    "peso_total_kg": peso_kg,
                    "chave_utilizada": CHAVE_PIX_EMAIL
                })
                
                dados_pedido = {
                    "column_nome": cliente["nome"],
                    "column_telefone": cliente["telefone"],
                    "column_itens": itens_com_metadados
                }
                
                try:
                    supabase.table("pedidos").insert(dados_pedido).execute()
                    st.success(f"🎉 Sucesso! Pedido de R$ {valor_total:.2f} confirmado e enviado à produção.")
                    st.session_state.carrinho = []
                    st.session_state.etapa_venda = "carrinho"
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar o pedido: {e}")
