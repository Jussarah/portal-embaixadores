from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

import utils as U

st.set_page_config(page_title="Tifly | by zsarytta", page_icon="💠", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600&family=Sora:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { font-family: 'Sora', sans-serif; }
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(1100px 560px at 88% -8%, rgba(139,92,246,.38), transparent 60%),
    radial-gradient(900px 520px at -8% 108%, rgba(255,95,184,.24), transparent 60%),
    linear-gradient(135deg, #090d29 0%, #141047 55%, #1f1250 100%);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d1037 0%, #1b1253 100%);
  border-right: 1px solid rgba(255,255,255,.08);
}
h1, h2, h3, h5 { font-family: 'Unbounded', sans-serif !important; letter-spacing: .01em; color: #ffffff; }

.hero { padding: 6px 0 4px 0; }
.hero .title { font-family: 'Unbounded', sans-serif; font-size: 2.2rem; font-weight: 600; color: #fff; line-height: 1.15; }
.hero .sub { color: #c9c6ff; font-size: .95rem; margin-top: 4px; }
.divider { height: 2px; background: linear-gradient(90deg, #4f8bff, #8b5cf6, #ff5fb8); border-radius: 2px; margin: 12px 0 24px 0; }

.brand { display: flex; align-items: center; gap: 12px; margin: 18px 0 4px 2px; }
.brand .name { font-family: 'Unbounded', sans-serif; font-size: 1.6rem; font-weight: 600; color: #fff; line-height: 1.05; }
.brand .by { font-size: .82rem; color: #ff8fcf; margin-top: 2px; }
.menu-title { font-size: .85rem; color: #bdbaff; margin: 10px 0 2px 2px; }
.status { background: rgba(70, 220, 160, .12); border: 1px solid rgba(70,220,160,.45); color: #7ff0c4;
  border-radius: 14px; padding: 12px 14px; font-size: .9rem; }

.kpi { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); border-radius: 18px;
  padding: 16px 20px; backdrop-filter: blur(10px); box-shadow: 0 0 26px rgba(139,92,246,.18); }
.kpi .lbl { font-size: .8rem; color: #bdbaff; }
.kpi .val { font-family: 'Unbounded', sans-serif; font-size: 1.75rem; font-weight: 700;
  background: linear-gradient(90deg, #8fb4ff, #ff7ac8); -webkit-background-clip: text; background-clip: text; color: transparent; }

.stButton > button, [data-testid="stDownloadButton"] button, [data-testid="stFormSubmitButton"] button {
  background: linear-gradient(90deg, #4f8bff, #8b5cf6 55%, #ff5fb8); color: #fff; border: 0; border-radius: 14px;
  padding: .6rem 1.4rem; font-weight: 600; box-shadow: 0 8px 24px rgba(139,92,246,.35);
}
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover { filter: brightness(1.12); color: #fff; }
.stTextArea textarea, .stTextInput input, .stDateInput input, .stNumberInput input {
  background: rgba(255,255,255,.07) !important; color: #fff !important;
  border: 1px solid rgba(255,255,255,.18) !important; border-radius: 12px !important;
}
.footer { color: #8f8cc4; font-size: .8rem; border-top: 1px solid rgba(255,255,255,.1); margin-top: 36px; padding-top: 14px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

REDES = U.PLATAFORMAS + ["Outra"]

LOGO = '<svg width="46" height="46" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="tf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f8bff"/><stop offset=".55" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ff5fb8"/></linearGradient></defs><path d="M32 34C18 36 6 28 6 14c14-2 25 6 26 20z" fill="url(#tf)"/><path d="M32 34c14 2 26-6 26-20-14-2-25 6-26 20z" fill="url(#tf)" opacity=".72"/><path d="M32 34c-10 6-18 16-14 24 10-2 15-12 14-24z" fill="url(#tf)" opacity=".55"/><path d="M32 34c10 6 18 16 14 24-10-2-15-12-14-24z" fill="url(#tf)" opacity=".38"/><circle cx="32" cy="34" r="3.2" fill="#fff"/></svg>'


# --------------------------------------------------------------------------- #
# Estado
# --------------------------------------------------------------------------- #
def init_state():
    st.session_state.setdefault("links", [])
    st.session_state.setdefault("txt_links", "")
    st.session_state.setdefault("videos", U.videos_vazio())
    st.session_state.setdefault("p_ini", date.today() - timedelta(days=30))
    st.session_state.setdefault("p_fim", date.today())
    st.session_state.setdefault("p_redes", REDES)


init_state()


def kpi_html(label, value):
    return f'<div class="kpi"><div class="lbl">{label}</div><div class="val">{value}</div></div>'


def kpis(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.markdown(kpi_html(label, value), unsafe_allow_html=True)


def periodo():
    ini, fim = st.session_state.p_ini, st.session_state.p_fim
    redes = st.session_state.p_redes
    return ini, fim, redes, U.filtrar_periodo(st.session_state.videos, ini, fim, redes)


def youtube_key():
    try:
        return st.secrets.get("YOUTUBE_API_KEY", "")
    except Exception:
        return ""


# --------------------------------------------------------------------------- #
# Barra lateral
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.markdown('<div class="status">● Sistema online<br><small>Tifly • painel de embaixadores</small></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="brand">' + LOGO + '<div><div class="name">Tifly</div>'
        '<div class="by">by zsarytta</div></div></div><div class="divider"></div>'
        '<div class="menu-title">Menu</div>',
        unsafe_allow_html=True,
    )
    modulo = st.radio(
        "Menu",
        ["🔗  Corretor de links", "📊  Análise de vídeos", "📥  Relatórios"],
        label_visibility="collapsed",
    )
    with st.expander("🔑 YouTube API (opcional)"):
        chave_digitada = st.text_input("Chave da API", type="password",
                                       help="Gratuita no Google Cloud. Preenche views e curtidas de vídeos do YouTube.")
    yt_key = chave_digitada or youtube_key()
    st.markdown("---")
    if st.button("♻️ Reiniciar dados"):
        for k in ("links", "videos", "txt_links"):
            st.session_state.pop(k, None)
        init_state()
        st.rerun()

st.markdown(
    '<div class="hero"><div class="title">Tifly</div>'
    '<div class="sub">Seu painel de embaixadores: links de perfil corretos e desempenho de vídeos em um só lugar.</div></div>'
    '<div class="divider"></div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------- #
# Aba 1: Corretor de links
# --------------------------------------------------------------------------- #
def processar_links():
    antigos = [r["Original"] for r in st.session_state.links]
    novo = st.session_state.txt_links
    st.session_state.links = U.corrigir_lista("\n".join(antigos) + "\n" + novo)
    st.session_state.txt_links = ""


def limpar_links():
    st.session_state.links = []


def aba_links():
    st.subheader("Corretor de links de perfil")
    st.caption("Funciona com Instagram, TikTok, YouTube, Facebook e Kwai. Cole um link por vez ou vários de uma vez.")
    st.text_area("Cole os links de perfil", key="txt_links", height=140,
                 placeholder="https://www.instagram.com/usuario/?igsh=abc123\nhttps://tiktok.com/@usuario?lang=pt-BR")
    c1, c2, _ = st.columns([1.6, 1.4, 3])
    c1.button("✨ Corrigir links", on_click=processar_links)
    c2.button("Limpar lista", on_click=limpar_links)

    links = st.session_state.links
    if not links:
        st.info("Cole os links acima e clique em Corrigir links para ver o resultado.")
        return
    df = pd.DataFrame(links)
    cont = df["Status"].value_counts()
    kpis([
        ("Links na lista", len(df)),
        ("Corrigidos", int(cont.get(U.ST_FIX, 0))),
        ("Para verificar", int(cont.get(U.ST_CHECK, 0)) + int(cont.get(U.ST_DUP, 0))),
        ("Inválidos", int(cont.get(U.ST_BAD, 0))),
    ])
    st.write("")
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={"Link corrigido": st.column_config.LinkColumn("Link corrigido")},
    )
    prontos = df[df["Status"].isin([U.ST_OK, U.ST_FIX])]["Link corrigido"].tolist()
    if prontos:
        st.markdown("##### Links prontos para copiar")
        st.code("\n".join(prontos), language=None)


# --------------------------------------------------------------------------- #
# Aba 2: Análise de vídeos
# --------------------------------------------------------------------------- #
def aba_videos():
    st.subheader("Análise de vídeos por período")
    videos = st.session_state.videos

    with st.expander("➕ Adicionar vídeo", expanded=len(videos) == 0):
        with st.form("form_video", clear_on_submit=True):
            link = st.text_input("Link do vídeo")
            c1, c2 = st.columns(2)
            emb = c1.text_input("Embaixador")
            data = c2.date_input("Data de postagem", value=date.today(), format="DD/MM/YYYY")
            c3, c4, c5 = st.columns(3)
            views = c3.number_input("Visualizações", min_value=0, step=1)
            likes = c4.number_input("Curtidas", min_value=0, step=1)
            saves = c5.number_input("Salvamentos", min_value=0, step=1)
            auto = st.checkbox("Buscar views e curtidas automaticamente (só YouTube, precisa da chave na barra lateral)")
            enviado = st.form_submit_button("Adicionar vídeo")
        if enviado:
            if not link.strip():
                st.warning("Cole o link do vídeo.")
            else:
                rede = U.detectar_rede(link)
                data_ts = pd.Timestamp(data)
                if auto and rede == "YouTube":
                    vid = U.youtube_video_id(link)
                    if not yt_key:
                        st.warning("Informe a chave da YouTube API na barra lateral para a busca automática.")
                    elif not vid:
                        st.warning("Não consegui identificar o vídeo neste link do YouTube.")
                    else:
                        try:
                            stats = U.buscar_youtube(vid, yt_key)
                            views, likes, data_ts = stats["views"], stats["likes"], stats["data"]
                        except Exception as e:
                            st.warning(f"Busca automática falhou ({e}). Usei os números digitados.")
                nova = pd.DataFrame([{
                    "Link": link.strip(), "Embaixador": emb.strip(), "Rede": rede, "Data": data_ts,
                    "Visualizações": int(views), "Curtidas": int(likes), "Salvamentos": int(saves),
                }])
                st.session_state.videos = pd.concat([U.normalizar_videos(videos), nova], ignore_index=True)
                st.rerun()

    st.markdown("##### Período")
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.date_input("De", key="p_ini", format="DD/MM/YYYY")
    c2.date_input("Até", key="p_fim", format="DD/MM/YYYY")
    c3.multiselect("Redes", REDES, key="p_redes")

    resumo_box = st.container()

    st.markdown("##### Tabela de vídeos")
    st.caption("Edite os números direto na tabela. Para apagar, selecione a linha e use a lixeira.")
    editada = st.data_editor(
        U.normalizar_videos(st.session_state.videos),
        num_rows="dynamic", hide_index=True, width="stretch", key="ed_videos",
        column_config={
            "Link": st.column_config.TextColumn("Link do vídeo", width="large"),
            "Rede": st.column_config.SelectboxColumn("Rede", options=REDES),
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Visualizações": st.column_config.NumberColumn(format="%d", min_value=0),
            "Curtidas": st.column_config.NumberColumn(format="%d", min_value=0),
            "Salvamentos": st.column_config.NumberColumn(format="%d", min_value=0),
        },
    )
    st.session_state.videos = U.normalizar_videos(editada)

    ini, fim, redes, filtrado = periodo()
    with resumo_box:
        if ini > fim:
            st.error("A data inicial é maior que a final.")
        t = U.totais(filtrado)
        kpis([(k, U.fmt(v)) for k, v in t.items()])
        if len(filtrado):
            st.write("")
            por_rede = U.resumo_por_rede(filtrado)
            g1, g2 = st.columns([3, 2])
            g1.bar_chart(por_rede.set_index("Rede")[["Visualizações", "Curtidas", "Salvamentos"]],
                         color=["#4f8bff", "#8b5cf6", "#ff5fb8"])
            g2.dataframe(por_rede, hide_index=True, width="stretch")
        else:
            st.info("Nenhum vídeo neste período. Adicione vídeos ou ajuste as datas.")


# --------------------------------------------------------------------------- #
# Aba 3: Relatórios
# --------------------------------------------------------------------------- #
def aba_relatorios():
    st.subheader("Relatórios")
    ini, fim, redes, filtrado = periodo()
    st.caption(f"Período do relatório: {ini:%d/%m/%Y} a {fim:%d/%m/%Y}. "
               "Para mudar datas e redes, use a aba Análise de vídeos.")
    t = U.totais(filtrado)
    kpis([(k, U.fmt(v)) for k, v in t.items()])
    st.write("")
    if filtrado.empty and not st.session_state.links:
        st.info("Ainda não há dados para exportar. Corrija links ou adicione vídeos primeiro.")
        return
    links_df = pd.DataFrame(st.session_state.links)
    stamp = f"{ini:%Y%m%d}_{fim:%Y%m%d}"
    c1, c2, _ = st.columns([1, 1, 2])
    c1.download_button(
        "📊 Baixar planilha (Excel)", data=U.gerar_excel(links_df, filtrado, ini, fim),
        file_name=f"relatorio_embaixadores_{stamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    c2.download_button(
        "📄 Baixar relatório (PDF)", data=U.gerar_pdf(filtrado, ini, fim),
        file_name=f"relatorio_embaixadores_{stamp}.pdf", mime="application/pdf",
    )


if modulo.startswith("🔗"):
    aba_links()
elif modulo.startswith("📊"):
    aba_videos()
else:
    aba_relatorios()

st.markdown(
    f'<div class="footer">Tifly • criado por zsarytta • {datetime.now():%d/%m/%Y %H:%M}</div>',
    unsafe_allow_html=True,
)
