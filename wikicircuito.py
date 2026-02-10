import streamlit as st
import json, os
import qrcode
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="WikiCircuito ULTRA", layout="wide")

# ===================== 🎨 ESTILO
st.markdown("""
<style>
.stApp {background:linear-gradient(145deg,#0f172a,#1e293b);color:#e2e8f0;}
h1,h2,h3 {color:#38bdf8;}
.card {background:#1e293b;padding:20px;border-radius:14px;margin-bottom:18px;border:1px solid #334155;}
button {background:#0ea5e9;color:white;border-radius:10px;}
div[data-baseweb="select"] svg {fill:white!important;}
</style>
""", unsafe_allow_html=True)

# ===================== 📁 ARQUIVOS
ARQ_PROJ="projetos.json"
ARQ_USER="usuarios.json"
ARQ_HIST="historico.json"
ARQ_EST="estoque.json"

def load(arq,padrao):
    if os.path.exists(arq):
        with open(arq,"r") as f: return json.load(f)
    return padrao

def save(arq,data):
    with open(arq,"w") as f: json.dump(data,f,indent=4)

# ===================== DADOS
usuarios = load(ARQ_USER,{
    "aluno":{"senha":"123","tipo":"Aluno"},
    "tecnico":{"senha":"123","tipo":"Técnico"}
})
projetos = load(ARQ_PROJ,[])
historico = load(ARQ_HIST,{})
estoque = load(ARQ_EST,{})

descricao_componentes = {
    "led": "Emite luz quando energizado.",
    "resistor": "Limita corrente elétrica.",
    "arduino uno": "Placa microcontroladora.",
    "motor dc": "Gera movimento.",
    "l298n": "Driver para motores."
}

# ===================== SESSION
for k in ["logado","user","tipo","confirmar_saida"]:
    if k not in st.session_state:
        st.session_state[k] = False if k!="user" and k!="tipo" else None

# ===================== LOGIN
st.title("WikiCircuito PRO")

if not st.session_state.logado:
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")

    # 🔹 BOTÃO ESQUECEU A SENHA (SÓ ALUNO)
    if u == "aluno":
        if st.button("Esqueceu a senha?"):
            st.info("Procure o técnico responsável pelo laboratório para redefinir sua senha.")

    if st.button("Entrar"):
        if u in usuarios and usuarios[u]["senha"] == s:
            st.session_state.logado = True
            st.session_state.user = u
            st.session_state.tipo = usuarios[u]["tipo"]
            st.rerun()
        else:
            st.error("Login inválido")

    st.stop()

# ===================== SIDEBAR
with st.sidebar:
    st.success(f"👤 {st.session_state.user} ({st.session_state.tipo})")

    if not st.session_state.confirmar_saida:
        if st.button("Sair"):
            st.session_state.confirmar_saida=True
            st.rerun()
    else:
        st.warning("Confirmar saída?")
        if st.button("✅ Sim"):
            st.session_state.logado=False
            st.session_state.user=None
            st.session_state.tipo=None
            st.session_state.confirmar_saida=False
            st.rerun()
        if st.button("❌ Cancelar"):
            st.session_state.confirmar_saida=False
            st.rerun()

    st.markdown("---")

    if st.session_state.tipo=="Técnico":
        menu=st.selectbox("Menu",[
            "Projetos",
            "Cadastrar Projeto",
            "Buscar Componente",
            "QR Codes",
            "Estoque",
        ])
    else:
        menu=st.selectbox("Menu",[
            "Projetos",
            "Buscar Componente",
            "QR Codes",
        ])

# ===================== QR
def gerar_qr(txt):
    img=qrcode.make(txt)
    buf=BytesIO()
    img.save(buf)
    return buf.getvalue()

# ===================== PROJETOS
if menu=="Projetos":
    st.header("Projetos do Laboratório")
    if not projetos:
        st.info("Nenhum projeto cadastrado.")
    for p in projetos:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.subheader(p["nome"])
        st.write("Nível:",p["dif"])
        st.write(p["desc"])
        st.write("Componentes:",", ".join(p["comps"]))
        st.markdown('</div>',unsafe_allow_html=True)

# ===================== CADASTRO
elif menu=="Cadastrar Projeto":
    if st.session_state.tipo!="Técnico":
        st.error("Acesso restrito.")
        st.stop()

    st.header("Novo Projeto")
    nome=st.text_input("Nome")
    desc=st.text_area("Descrição")
    dif=st.selectbox("Dificuldade",["Iniciante","Intermediário","Avançado"])
    comps=st.text_input("Componentes (vírgula)")

    if st.button("Salvar"):
        lista=[c.strip().lower() for c in comps.split(",")]
        projetos.append({"nome":nome,"desc":desc,"dif":dif,"comps":lista})
        save(ARQ_PROJ,projetos)

        for c in lista:
            estoque[c]=estoque.get(c,0)+1
        save(ARQ_EST,estoque)

        st.success("Projeto cadastrado!")

# ===================== BUSCA
elif menu=="Buscar Componente":
    comp=st.text_input("Digite o componente").lower()
    if comp:
        historico.setdefault(st.session_state.user,[]).append(comp)
        save(ARQ_HIST,historico)

        ach=[p for p in projetos if comp in p["comps"]]
        for a in ach: st.success(a["nome"])

# ===================== QR CODES
elif menu=="QR Codes":
    st.header("QR dos Componentes")
    comps=sorted({c for p in projetos for c in p["comps"]})
    cols=st.columns(4)
    for i,c in enumerate(comps):
        with cols[i%4]:
            st.image(gerar_qr(c),width=120)
            st.write(c.upper())
            if st.session_state.tipo=="Aluno":
                st.caption(descricao_componentes.get(c,"Componente eletrônico"))

# ===================== ESTOQUE
elif menu=="Estoque":
    st.header("Estoque")
    df=pd.DataFrame(list(estoque.items()),columns=["Componente","Quantidade"])
    st.dataframe(df)
    