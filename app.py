"""Interface didática para Dijkstra, Prim e Kruskal."""

from __future__ import annotations

import json
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from algoritmos import dijkstra, kruskal, prim


BASE = Path(__file__).resolve().parent
with (BASE / "dados_projetos.json").open(encoding="utf-8") as arquivo:
    DADOS = json.load(arquivo)

st.set_page_config(
    page_title="Projetos de Grafos",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .stApp { background: #f5f7fa; }
      [data-testid="stHeader"] { background: rgba(245,247,250,0.92); }
      h1, h2, h3 { color: #16324f; }
      div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #dce4ec; padding: 13px 16px;
        border-radius: 12px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def url_mapa_busca(local: str) -> str:
    return "https://www.google.com/maps/search/?api=1&" + urlencode({"query": local})


def url_mapa_rota(origem: str, destino: str, intermediarios: list[str], modo: str) -> str:
    parametros = {
        "api": "1",
        "origin": origem,
        "destination": destino,
        "travelmode": modo,
    }
    if intermediarios:
        parametros["waypoints"] = "|".join(intermediarios)
    return "https://www.google.com/maps/dir/?" + urlencode(parametros)


def distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    raio_km = 6371.0
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return 2 * raio_km * asin(sqrt(a))


def pares_selecionados(arestas: list[dict]) -> set[frozenset[str]]:
    return {frozenset((a["origem"], a["destino"])) for a in arestas}


def figura_esquematica(
    nos: list[str],
    arestas: list[dict],
    posicoes: dict[str, dict[str, float]],
    destaques: set[frozenset[str]],
    nos_rota: set[str],
    unidade: str,
) -> go.Figure:
    figura = go.Figure()
    for aresta in arestas:
        u, v = aresta["origem"], aresta["destino"]
        p1, p2 = posicoes[u], posicoes[v]
        em_rota = frozenset((u, v)) in destaques
        figura.add_trace(
            go.Scatter(
                x=[p1["x"], p2["x"], None],
                y=[p1["y"], p2["y"], None],
                mode="lines",
                line={"color": "#e27843" if em_rota else "#aab8c6", "width": 4 if em_rota else 1.5},
                hoverinfo="skip",
                showlegend=False,
            )
        )
        peso = aresta.get("peso")
        if peso is not None:
            figura.add_trace(
                go.Scatter(
                    x=[(p1["x"] + p2["x"]) / 2],
                    y=[(p1["y"] + p2["y"]) / 2],
                    mode="text",
                    text=[f"{peso:.1f} {unidade}"],
                    textfont={"size": 10, "color": "#516579"},
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
    figura.add_trace(
        go.Scatter(
            x=[posicoes[n]["x"] for n in nos],
            y=[posicoes[n]["y"] for n in nos],
            mode="markers+text",
            text=nos,
            textposition="top center",
            textfont={"size": 11, "color": "#17324d"},
            marker={
                "size": 14,
                "color": ["#e27843" if n in nos_rota else "#176b87" for n in nos],
                "line": {"color": "white", "width": 1.5},
            },
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    figura.update_layout(
        height=510,
        margin={"l": 8, "r": 8, "t": 18, "b": 8},
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis={"visible": False, "showgrid": False, "zeroline": False},
        yaxis={"visible": False, "showgrid": False, "zeroline": False, "scaleanchor": "x"},
        hovermode="closest",
    )
    return figura


def figura_mapa_cidade(
    nos: list[str],
    arestas: list[dict],
    coordenadas: dict[str, list[float]],
    destaques: set[frozenset[str]],
    nos_rota: set[str],
) -> go.Figure:
    """Mostra as ligações sobre o mapa de ruas; os pontos locais são referências aproximadas."""
    figura = go.Figure()
    for aresta in arestas:
        u, v = aresta["origem"], aresta["destino"]
        lat1, lon1 = coordenadas[u]
        lat2, lon2 = coordenadas[v]
        em_rota = frozenset((u, v)) in destaques
        figura.add_trace(
            go.Scattermapbox(
                lon=[lon1, lon2],
                lat=[lat1, lat2],
                mode="lines",
                line={"color": "#e27843" if em_rota else "#8998a8", "width": 5 if em_rota else 2},
                opacity=0.92 if em_rota else 0.66,
                hoverinfo="skip",
                showlegend=False,
            )
        )
    figura.add_trace(
        go.Scattermapbox(
            lon=[coordenadas[n][1] for n in nos],
            lat=[coordenadas[n][0] for n in nos],
            mode="markers+text",
            text=nos,
            textposition="top center",
            textfont={"size": 10, "color": "#17324d"},
            marker={
                "size": 12,
                "color": ["#e27843" if n in nos_rota else "#176b87" for n in nos],
                "opacity": 0.96,
            },
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    centro = [sum(coordenadas[n][i] for n in nos) / len(nos) for i in (0, 1)]
    figura.update_layout(
        height=510,
        margin={"l": 0, "r": 0, "t": 8, "b": 8},
        paper_bgcolor="white",
        mapbox={"style": "open-street-map", "center": {"lat": centro[0], "lon": centro[1]}, "zoom": 12},
    )
    return figura


def figura_aeroportos(
    nos: dict[str, dict],
    arestas: list[dict],
    destaques: set[frozenset[str]],
) -> go.Figure:
    figura = go.Figure()
    for aresta in arestas:
        origem, destino = aresta["origem"], aresta["destino"]
        p1, p2 = nos[origem], nos[destino]
        em_arvore = frozenset((origem, destino)) in destaques
        figura.add_trace(
            go.Scattergeo(
                lon=[p1["lon"], p2["lon"]],
                lat=[p1["lat"], p2["lat"]],
                mode="lines",
                line={"color": "#e27843" if em_arvore else "#b9c4cf", "width": 3.2 if em_arvore else 1.1},
                opacity=0.9 if em_arvore else 0.55,
                hoverinfo="skip",
                showlegend=False,
            )
        )
    figura.add_trace(
        go.Scattergeo(
            lon=[v["lon"] for v in nos.values()],
            lat=[v["lat"] for v in nos.values()],
            text=[f'{v["cidade"]} ({codigo})' for codigo, v in nos.items()],
            mode="markers+text",
            textposition="top center",
            textfont={"size": 9, "color": "#16324f"},
            marker={"size": 7, "color": "#176b87", "line": {"color": "white", "width": 1}},
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    figura.update_layout(
        height=540,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="white",
        geo={
            "scope": "south america",
            "projection_type": "mercator",
            "showland": True,
            "landcolor": "#f2f4f5",
            "showocean": True,
            "oceancolor": "#e9f2f6",
            "showlakes": True,
            "lakecolor": "#e9f2f6",
            "showcountries": True,
            "countrycolor": "#cbd4dc",
            "showcoastlines": True,
            "coastlinecolor": "#cbd4dc",
            "fitbounds": "locations",
        },
    )
    return figura


def tabela_com_links(
    linhas: list[dict],
    coluna_link: str = "Google Maps",
    texto_link: str = "Abrir trecho",
) -> None:
    tabela = pd.DataFrame(linhas)
    if tabela.empty:
        st.info("Não há trechos para mostrar nesta seleção.")
        return
    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        column_config={coluna_link: st.column_config.LinkColumn(coluna_link, display_text=texto_link)},
    )


st.title("Grafos em Movimento")
st.caption("Dijkstra · Prim · Kruskal")

aba_dijkstra, aba_prim, aba_kruskal = st.tabs(
    ["Dijkstra", "Prim", "Kruskal"]
)


with aba_dijkstra:
    projeto = DADOS["dijkstra"]
    nos = projeto["nos"]
    arestas = projeto["arestas"]
    st.subheader("Menor caminho em Lorena")
    esquerda, direita = st.columns(2)
    origem = esquerda.selectbox("Origem", nos, index=0, key="dijkstra_origem")
    destino_padrao = nos.index("Parque das Rodovias") if "Parque das Rodovias" in nos else len(nos) - 1
    destino = direita.selectbox("Destino", nos, index=destino_padrao, key="dijkstra_destino")
    if origem == destino:
        st.info("Escolha dois pontos diferentes para calcular um trajeto.")
    else:
        caminho, custo, predecessores = dijkstra(nos, arestas, origem, destino)
        if not caminho:
            st.error("Não existe conexão entre esses pontos no grafo informado.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Distância", f"{custo:.1f} km")
            col2.metric("Trechos", str(len(caminho) - 1))
            col3.metric("Pontos", str(len(caminho)))
            st.info(" → ".join(caminho))
            arestas_rota = [
                next(a for a in arestas if {a["origem"], a["destino"]} == {u, v})
                for u, v in zip(caminho, caminho[1:])
            ]
            st.plotly_chart(
                figura_mapa_cidade(
                    nos,
                    arestas,
                    projeto["coord_gps"],
                    pares_selecionados(arestas_rota),
                    set(caminho),
                ),
                use_container_width=True,
            )
            rota_url = url_mapa_rota(
                f"{origem}, Lorena, SP",
                f"{destino}, Lorena, SP",
                [f"{p}, Lorena, SP" for p in caminho[1:-1]],
                "transit",
            )
            a, b = st.columns(2)
            a.link_button("Abrir rota no Google Maps", rota_url, use_container_width=True)
            b.download_button(
                "Baixar CSV",
                pd.DataFrame(arestas_rota).to_csv(index=False).encode("utf-8-sig"),
                file_name="percurso_dijkstra.csv",
                mime="text/csv",
                use_container_width=True,
            )
    st.caption("Mapa real. Pontos e distâncias de Lorena são aproximados.")


with aba_prim:
    projeto = DADOS["prim"]
    aeroportos = projeto["aeroportos"]
    arestas = []
    for origem, destino in projeto["rotas"]:
        a, b = aeroportos[origem], aeroportos[destino]
        km = distancia_haversine(a["lat"], a["lon"], b["lat"], b["lon"])
        arestas.append({"origem": origem, "destino": destino, "peso": km})
    st.subheader("Conectar aeroportos")
    inicio = st.selectbox("Aeroporto inicial", list(aeroportos), index=0, key="prim_inicio")
    arvore, custo, componentes = prim(list(aeroportos), arestas, inicio)
    col1, col2, col3 = st.columns(3)
    col1.metric("Aeroportos", str(len(aeroportos)))
    col2.metric("Ligações", str(len(arvore)))
    col3.metric("Total", f"{custo:,.0f} km")
    st.plotly_chart(figura_aeroportos(aeroportos, arestas, pares_selecionados(arvore)), use_container_width=True)
    linhas = []
    for a in arvore:
        nome_a = aeroportos[a["origem"]]["cidade"]
        nome_b = aeroportos[a["destino"]]["cidade"]
        linhas.append(
            {
                "Trecho da árvore": f'{a["origem"]} · {nome_a} → {a["destino"]} · {nome_b}',
                "Distância geográfica (km)": round(a["peso"], 1),
                "Google Maps": url_mapa_busca(f'{a["destino"]} {nome_b} aeroporto'),
            }
        )
    st.download_button(
        "Baixar CSV",
        pd.DataFrame(linhas).to_csv(index=False).encode("utf-8-sig"),
        file_name="arvore_prim_latam.csv",
        mime="text/csv",
        use_container_width=True,
    )
    with st.expander("Ver ligações"):
        tabela_com_links(linhas, texto_link="Localizar")
    st.caption("Distâncias em linha reta; recorte de rotas LATAM.")


with aba_kruskal:
    projeto = DADOS["kruskal"]
    nos = projeto["nos"]
    arestas = projeto["arestas"]
    st.subheader("Conectar bairros com menos vias")
    arvore, custo = kruskal(nos, arestas)
    col1, col2, col3 = st.columns(3)
    col1.metric("Bairros", str(len(nos)))
    col2.metric("Trechos", str(len(arvore)))
    col3.metric("Total", f"{custo:.1f} km")
    st.plotly_chart(
        figura_mapa_cidade(
            nos,
            arestas,
            projeto["coord_gps"],
            pares_selecionados(arvore),
            {n for a in arvore for n in (a["origem"], a["destino"])},
        ),
        use_container_width=True,
    )
    linhas = []
    for a in arvore:
        origem = f'{a["origem"]}, Lorena, SP'
        destino = f'{a["destino"]}, Lorena, SP'
        linhas.append(
            {
                "Via selecionada": f'{a["origem"]} → {a["destino"]}',
                "Comprimento estimado (km)": a["peso"],
                "Google Maps": url_mapa_rota(origem, destino, [], "driving"),
            }
        )
    st.download_button(
        "Baixar CSV",
        pd.DataFrame(linhas).to_csv(index=False).encode("utf-8-sig"),
        file_name="vias_kruskal_lorena.csv",
        mime="text/csv",
        use_container_width=True,
    )
    with st.expander("Ver trechos"):
        tabela_com_links(linhas)
    st.caption("Mapa real. Pontos e distâncias de Lorena são aproximados.")
