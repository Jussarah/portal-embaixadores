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

# ✏️ ESPAÇO PARA VOCÊ PREENCHER DEPOIS ---------------------------------------
# Cole aqui o link da planilha do Google Sheets com a lista oficial de embaixadores
# (ou guarde em Secrets do Streamlit com o nome SHEET_URL). Pode deixar vazio por enquanto.
SHEET_URL_PADRAO = ""
# Colunas que aparecem na tabela vazia, até a planilha ser conectada. Ajuste os nomes quando quiser.
COLUNAS_PADRAO = ["Nome", "ID", "TikTok", "YouTube", "Instagram"]
# -----------------------------------------------------------------------------

LOGO = '<svg width="46" height="46" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="tf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f8bff"/><stop offset=".55" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ff5fb8"/></linearGradient></defs><path d="M32 34C18 36 6 28 6 14c14-2 25 6 26 20z" fill="url(#tf)"/><path d="M32 34c14 2 26-6 26-20-14-2-25 6-26 20z" fill="url(#tf)" opacity=".72"/><path d="M32 34c-10 6-18 16-14 24 10-2 15-12 14-24z" fill="url(#tf)" opacity=".55"/><path d="M32 34c10 6 18 16 14 24-10-2-15-12-14-24z" fill="url(#tf)" opacity=".38"/><circle cx="32" cy="34" r="3.2" fill="#fff"/></svg>'


# --------------------------------------------------------------------------- #
# Estado
# --------------------------------------------------------------------------- #
def segredo(nome):
    try:
        return st.secrets.get(nome, "")
    except Exception:
        return ""


def init_state():
    st.session_state.setdefault("links", [])
    st.session_state.setdefault("txt_links", "")
    st.session_state.setdefault("videos", U.videos_vazio())
    st.session_state.setdefault("p_ini", date.today() - timedelta(days=30))
    st.session_state.setdefault("p_fim", date.today())
    st.session_state.setdefault("p_redes", REDES)
    st.session_state.setdefault("bulk_links", "")
    st.session_state.setdefault("r_canais", "")
    st.session_state.setdefault("r_ini", date.today() - timedelta(days=30))
    st.session_state.setdefault("r_fim", date.today())
    st.session_state.setdefault("r_min", 1000)
    st.session_state.setdefault("diretorio", pd.DataFrame(columns=COLUNAS_PADRAO))
    st.session_state.setdefault("sheet_url", SHEET_URL_PADRAO or segredo("SHEET_URL"))


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
    return segredo("YOUTUBE_API_KEY")


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
        ["🔗  Corretor de links", "👥  Embaixadores", "📡  Radar de vídeos", "📊  Análise de vídeos", "📥  Relatórios"],
        label_visibility="collapsed",
    )
    with st.expander("🔑 YouTube API (opcional)"):
        chave_digitada = st.text_input("Chave da API", type="password",
                                       help="Gratuita no Google Cloud. Preenche views e curtidas de vídeos do YouTube.")
    yt_key = chave_digitada or youtube_key()
    st.markdown("---")
    if st.button("♻️ Reiniciar dados"):
        for k in ("links", "videos", "txt_links", "diretorio", "dir_check", "arq_lido", "radar"):
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
# Aba: Diretório de embaixadores
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=600, show_spinner="Lendo a planilha...")
def ler_sheet(url):
    return pd.read_csv(U.sheet_csv_url(url), dtype=str).fillna("")


def ler_arquivo(arq):
    if arq.name.lower().endswith(".csv"):
        df = pd.read_csv(arq, dtype=str)
    else:
        df = pd.read_excel(arq, dtype=str)
    return df.fillna("")


def verificar_links():
    problemas, corrigido, cols = U.verificar_diretorio(st.session_state.diretorio)
    st.session_state.dir_check = {"problemas": problemas, "corrigido": corrigido, "cols": cols}


def aba_embaixadores():
    st.subheader("Diretório de embaixadores")
    st.caption("A lista oficial de embaixadores, vinda do Google Sheets ou de um arquivo que você enviar.")

    with st.expander("⚙️ Fonte dos dados", expanded=st.session_state.diretorio.empty):
        st.text_input(
            "Link da planilha do Google Sheets", key="sheet_url",
            placeholder="https://docs.google.com/spreadsheets/d/...",
            help="A planilha precisa estar compartilhada como 'Qualquer pessoa com o link pode ver'.",
        )
        if st.button("🔄 Carregar ou recarregar planilha"):
            url = st.session_state.sheet_url.strip()
            if not url:
                st.warning("Cole o link da planilha primeiro.")
            else:
                ok = False
                try:
                    ler_sheet.clear()
                    st.session_state.diretorio = ler_sheet(url)
                    st.session_state.pop("dir_check", None)
                    ok = True
                except Exception:
                    st.error("Não consegui ler a planilha. Confira se o compartilhamento está como "
                             "'Qualquer pessoa com o link' e se o link está certo.")
                if ok:
                    st.rerun()
        arq = st.file_uploader("Ou envie um arquivo CSV ou Excel", type=["csv", "xlsx"])
        if arq is not None:
            marca = (arq.name, arq.size)
            if st.session_state.get("arq_lido") != marca:
                ok = False
                try:
                    st.session_state.diretorio = ler_arquivo(arq)
                    st.session_state.arq_lido = marca
                    st.session_state.pop("dir_check", None)
                    ok = True
                except Exception as e:
                    st.error(f"Não consegui ler o arquivo ({e}).")
                if ok:
                    st.rerun()

    painel = st.container()

    with st.expander("✏️ Adicionar ou editar embaixadores", expanded=st.session_state.diretorio.empty):
        st.caption("Digite ou cole linhas direto na tabela. As alterações valem enquanto o app estiver aberto; "
                   "para guardar, baixe a lista em Excel (botão na seção de links).")
        st.session_state.diretorio = st.data_editor(
            st.session_state.diretorio, num_rows="dynamic", hide_index=True, width="stretch", key="ed_dir",
        )

    df = st.session_state.diretorio
    n = 0 if df.empty else int(df.apply(lambda r: any(not U.eh_vazio(v) for v in r), axis=1).sum())
    chk = st.session_state.get("dir_check")

    with painel:
        kpis([
            ("Embaixadores registrados", U.fmt(n)),
            ("Colunas detectadas", len(df.columns)),
            ("Links para revisar", U.fmt(len(chk["problemas"])) if chk else "—"),
        ])
        st.write("")
        if n == 0:
            st.info("Ainda não há embaixadores. Conecte a planilha em Fonte dos dados ou adicione "
                    "manualmente em Adicionar ou editar embaixadores.")
            return
        busca = st.text_input("Buscar embaixador", placeholder="nome, ID ou @usuário")
        mostrado = df
        if busca.strip():
            achou = df.apply(lambda c: c.astype(str).str.contains(busca.strip(), case=False, na=False, regex=False))
            mostrado = df[achou.any(axis=1)]
            st.caption(f"{len(mostrado)} resultado(s) para '{busca.strip()}'.")
        st.dataframe(mostrado, hide_index=True, width="stretch", height=420)

        st.markdown("##### Verificar links")
        st.caption("Procura as colunas com links, corrige o que dá e lista o que precisa da sua revisão.")
        st.button("🛠️ Verificar e corrigir links da lista", on_click=verificar_links)
        if chk:
            st.caption("Colunas de link analisadas: " + (", ".join(chk["cols"]) or "nenhuma"))
            if chk["problemas"].empty:
                st.success("Todos os links estão no padrão.")
            else:
                st.dataframe(
                    chk["problemas"], hide_index=True, width="stretch",
                    column_config={"Link corrigido": st.column_config.LinkColumn("Link corrigido")},
                )
            st.download_button(
                "📊 Baixar lista com links corrigidos (Excel)",
                data=U.excel_simples({"Embaixadores": chk["corrigido"], "Links para revisar": chk["problemas"]}),
                file_name="embaixadores_corrigidos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


# --------------------------------------------------------------------------- #
# Aba: Radar de vídeos
# --------------------------------------------------------------------------- #
def enviar_para_analise():
    r = st.session_state.radar["df"]
    novos = pd.DataFrame({
        "Link": r["Link"], "Embaixador": r["Canal"], "Rede": r["Rede"], "Data": r["Data"],
        "Visualizações": r["Visualizações"], "Curtidas": r["Curtidas"], "Salvamentos": 0,
    })
    junto = pd.concat([U.normalizar_videos(st.session_state.videos), U.normalizar_videos(novos)], ignore_index=True)
    st.session_state.videos = junto.drop_duplicates(subset="Link", keep="first").reset_index(drop=True)
    st.session_state.radar_enviado = len(novos)


def aba_radar():
    st.subheader("Radar de vídeos")
    st.caption("Informe os canais e o período. O radar lista os vídeos que passaram das views mínimas.")
    st.text_area(
        "Canais para rastrear (um por linha)", key="r_canais", height=130,
        placeholder="https://youtube.com/@CanalX\nhttps://facebook.com/PaginaY\nhttps://tiktok.com/@CreadorZ",
    )
    c1, c2, c3 = st.columns(3)
    c1.date_input("De", key="r_ini", format="DD/MM/YYYY")
    c2.date_input("Até", key="r_fim", format="DD/MM/YYYY")
    c3.number_input("Views mínimas", min_value=0, step=100, key="r_min")

    if not yt_key:
        st.info("A busca automática de canais do YouTube precisa da chave da YouTube API (barra lateral, "
                "em API do YouTube). Sem ela, todos os canais ficam para preenchimento manual.")

    if st.button("📡 Ativar radar"):
        linhas = [l.strip() for l in st.session_state.r_canais.splitlines() if l.strip()]
        if not linhas:
            st.warning("Cole pelo menos um canal.")
        elif st.session_state.r_ini > st.session_state.r_fim:
            st.error("A data inicial é maior que a final.")
        else:
            achados, pendentes, erros, lidos = [], [], [], 0
            barra = st.progress(0.0, text="Rastreando canais...")
            for i, linha in enumerate(linhas):
                rede = U.detectar_rede(linha)
                ref = U.youtube_canal_ref(linha) if rede == "YouTube" else None
                if rede == "YouTube" and yt_key and ref:
                    try:
                        achados += U.radar_youtube(ref, yt_key, st.session_state.r_ini,
                                                   st.session_state.r_fim, st.session_state.r_min)
                        lidos += 1
                    except ValueError as e:
                        erros.append((linha, str(e)))
                else:
                    pendentes.append((linha, rede))
                barra.progress((i + 1) / len(linhas), text=f"Rastreando canais... {i + 1}/{len(linhas)}")
            barra.empty()
            cols = ["Canal", "Título", "Data", "Visualizações", "Curtidas", "Link", "Rede"]
            df = pd.DataFrame(achados, columns=cols)
            if not df.empty:
                df = df.sort_values("Visualizações", ascending=False).reset_index(drop=True)
            st.session_state.radar = {"df": df, "pendentes": pendentes, "erros": erros, "lidos": lidos}

    if st.session_state.get("radar_enviado"):
        st.success(f"{st.session_state.pop('radar_enviado')} vídeo(s) enviados para a aba Análise de vídeos.")

    r = st.session_state.get("radar")
    if not r:
        return
    df = r["df"]
    kpis([
        ("Canais rastreados", r["lidos"]),
        ("Vídeos encontrados", U.fmt(len(df))),
        ("Visualizações somadas", U.fmt(df["Visualizações"].sum() if len(df) else 0)),
    ])
    st.write("")
    if df.empty:
        st.info("Nenhum vídeo passou das views mínimas neste período.")
    else:
        st.dataframe(
            df, hide_index=True, width="stretch",
            column_config={
                "Link": st.column_config.LinkColumn("Link"),
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "Visualizações": st.column_config.NumberColumn(format="%d"),
                "Curtidas": st.column_config.NumberColumn(format="%d"),
            },
        )
        b1, b2, _ = st.columns([1.6, 1.6, 2])
        b1.button("➕ Enviar para Análise de vídeos", on_click=enviar_para_analise)
        saida = df.copy()
        saida["Data"] = saida["Data"].dt.strftime("%d/%m/%Y")
        b2.download_button(
            "📊 Baixar resultado (Excel)", data=U.excel_simples({"Radar": saida}),
            file_name="radar_videos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    if r["erros"]:
        with st.expander(f"⚠️ {len(r['erros'])} canal(is) com erro", expanded=True):
            for linha, msg in r["erros"]:
                st.write(f"{linha}: {msg}")
    if r["pendentes"]:
        with st.expander(f"✍️ {len(r['pendentes'])} canal(is) para preenchimento manual", expanded=True):
            st.caption("Instagram, TikTok, Facebook e Kwai não liberam esses dados de forma automática e gratuita. "
                       "Anote os vídeos na aba Análise de vídeos.")
            for linha, rede in r["pendentes"]:
                st.write(f"{rede}: {linha}")


# --------------------------------------------------------------------------- #
# Aba 2: Análise de vídeos
# --------------------------------------------------------------------------- #
def adicionar_em_lote():
    links = st.session_state.bulk_links.split()
    existentes = set(st.session_state.videos["Link"].astype(str))
    novos = [l for l in dict.fromkeys(links) if l not in existentes]
    if not novos:
        st.session_state.video_msg = "Nenhum link novo para adicionar."
        return
    linhas = pd.DataFrame({
        "Link": novos, "Embaixador": "", "Perfil": [U.perfil_do_link(l) for l in novos], "Rede": [U.detectar_rede(l) for l in novos],
        "Data": pd.Timestamp(date.today()), "Visualizações": 0, "Curtidas": 0, "Salvamentos": 0,
    })
    st.session_state.videos = pd.concat([U.normalizar_videos(st.session_state.videos), linhas], ignore_index=True)
    st.session_state.bulk_links = ""
    st.session_state.video_msg = (f"{len(novos)} link(s) adicionados. Agora preencha data, visualizações, curtidas "
                                  "e salvamentos na tabela abaixo: o app só detecta a rede pelo link.")


def aba_videos():
    st.subheader("Análise de vídeos por período")
    videos = st.session_state.videos
    msg = st.session_state.pop("video_msg", None)
    if msg:
        st.info(msg)

    resumo = st.session_state.pop("busca_resumo", None)
    if resumo:
        if resumo["auto"]:
            st.success(f"{resumo['auto']} de {resumo['total']} link(s) preenchidos automaticamente.")
        if resumo["falhas"]:
            with st.expander(f"✍️ {len(resumo['falhas'])} link(s) para preencher manualmente", expanded=True):
                st.caption("A rede bloqueou a leitura automática. Os links já estão na tabela abaixo: "
                           "digite views, curtidas, salvamentos e a data. Vídeos sem data ficam fora dos totais "
                           "do período até você preencher.")
                for l, rede, motivo in resumo["falhas"]:
                    st.write(f"{rede}: {l} ({motivo})")

    if st.session_state.pop("limpar_bulk", False):
        st.session_state.bulk_links = ""
    st.markdown("##### Cole os links e busque os dados")
    st.caption("O app tenta ler visualizações, curtidas, data e perfil de cada link. O que a rede não liberar "
               "fica para você preencher na tabela.")
    st.text_area("Links dos vídeos (um por linha)", key="bulk_links", height=110,
                 placeholder="https://www.tiktok.com/@usuario/video/123...\nhttps://youtube.com/watch?v=...")
    b1, b2, _ = st.columns([1.8, 1.8, 2])
    buscar = b1.button("🔎 Buscar dados dos links")
    b2.button("Só adicionar os links", on_click=adicionar_em_lote)
    if buscar:
        existentes = set(st.session_state.videos["Link"].astype(str))
        links = [l for l in dict.fromkeys(st.session_state.bulk_links.split()) if l not in existentes]
        if not links:
            st.warning("Cole pelo menos um link novo.")
        else:
            linhas, falhas, auto = [], [], 0
            barra = st.progress(0.0, text="Buscando dados...")
            for i, l in enumerate(links):
                rede = U.detectar_rede(l)
                row = {"Link": l, "Embaixador": "", "Perfil": U.perfil_do_link(l), "Rede": rede, "Data": pd.NaT,
                       "Visualizações": 0, "Curtidas": 0, "Salvamentos": 0}
                try:
                    d = U.buscar_dados_link(l, yt_key)
                    row.update({
                        "Embaixador": d["canal"], "Perfil": d["perfil"] or row["Perfil"],
                        "Data": d["data"] if d["data"] is not None else pd.NaT,
                        "Visualizações": d["views"], "Curtidas": d["likes"],
                        "Salvamentos": d["saves"] or 0,
                    })
                    auto += 1
                except Exception as e:
                    falhas.append((l, rede, str(e)))
                linhas.append(row)
                barra.progress((i + 1) / len(links), text=f"Buscando dados... {i + 1}/{len(links)}")
            barra.empty()
            st.session_state.videos = pd.concat(
                [U.normalizar_videos(st.session_state.videos), U.normalizar_videos(pd.DataFrame(linhas))],
                ignore_index=True)
            st.session_state.busca_resumo = {"auto": auto, "falhas": falhas, "total": len(links)}
            st.session_state.limpar_bulk = True
            st.rerun()

    with st.expander("➕ Adicionar um vídeo manualmente"):
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
                if int(views) == 0 and int(likes) == 0 and int(saves) == 0:
                    if rede == "YouTube":
                        motivo = "Para o YouTube, marque a busca automática e informe a chave da API na barra lateral."
                    else:
                        motivo = (f"O {rede} não permite buscar esses números automaticamente, "
                                  "então eles precisam ser digitados.")
                    st.session_state.video_msg = (f"Vídeo adicionado ({rede}), mas views, curtidas e salvamentos "
                                                  f"ficaram em 0. {motivo} Preencha direto na tabela abaixo.")
                st.rerun()

    st.markdown("##### Período")
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.date_input("De", key="p_ini", format="DD/MM/YYYY")
    c2.date_input("Até", key="p_fim", format="DD/MM/YYYY")
    c3.multiselect("Redes", REDES, key="p_redes")

    resumo_box = st.container()

    st.markdown("##### Tabela de vídeos")
    st.caption("Edite os números direto na tabela. Para apagar, selecione a linha e use a lixeira.")
    s1, s2, _ = st.columns([1.4, 1.6, 2.4])
    ord_col = s1.selectbox("Organizar por", ["Data", "Visualizações", "Curtidas", "Salvamentos", "Embaixador", "Rede"],
                           key="ord_col")
    ord_dir = s2.radio("Ordem", ["Decrescente", "Crescente"], horizontal=True, key="ord_dir")
    base = U.normalizar_videos(st.session_state.videos).sort_values(
        ord_col, ascending=(ord_dir == "Crescente"), kind="stable", na_position="last").reset_index(drop=True)
    editada = st.data_editor(
        base,
        num_rows="dynamic", hide_index=True, width="stretch", key="ed_videos",
        column_config={
            "Link": st.column_config.TextColumn("Link do vídeo", width="large"),
            "Embaixador": st.column_config.TextColumn("Embaixador / canal"),
            "Perfil": st.column_config.LinkColumn("Perfil"),
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
elif modulo.startswith("👥"):
    aba_embaixadores()
elif modulo.startswith("📡"):
    aba_radar()
elif modulo.startswith("📊"):
    aba_videos()
else:
    aba_relatorios()

st.markdown(
    f'<div class="footer">Tifly • criado por zsarytta • {datetime.now():%d/%m/%Y %H:%M}</div>',
    unsafe_allow_html=True,
)
