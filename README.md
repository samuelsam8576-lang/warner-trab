# Algoritmos de grafos em três projetos

Aplicativo didático em Python com uma interface separada para cada problema da atividade:

1. **Dijkstra:** caminho de menor distância entre pontos de Lorena.
2. **Prim:** árvore geradora mínima no recorte de 17 aeroportos e 21 rotas diretas divulgadas pela LATAM.
3. **Kruskal:** conjunto de vias de menor comprimento para conectar bairros de Lorena.

## Como abrir

Instale o Python 3.10 ou superior. No terminal, dentro desta pasta, execute:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá o aplicativo. Cada algoritmo tem uma aba própria, com seletores, grafo, resultado e opção para baixar a tabela em CSV.

A interface foi mantida direta: escolha o algoritmo, selecione os pontos e veja o resultado no mapa. As explicações completas e as fontes ficam neste README.

## Como o grafo foi modelado

Um grafo tem vértices, arestas e pesos. Aqui, os vértices são pontos de referência de Lorena ou aeroportos. As arestas representam trechos didáticos de transporte, rotas aéreas diretas ou vias candidatas. Os pesos representam quilômetros.

O conjunto de rotas aéreas vem de comunicados públicos da LATAM. O peso de cada conexão usa a distância geográfica em linha reta entre as coordenadas dos aeroportos. Portanto, esse peso não é a distância percorrida pela aeronave, a duração do voo ou o custo operacional.

Os comprimentos do grafo de ônibus e do grafo de pavimentação são **estimativas didáticas** para demonstrar os algoritmos. O mapa de ruas é real, mas os pontos de bairro são referências aproximadas, não paradas oficiais georreferenciadas. A Prefeitura publica linhas e horários, incluindo Rodoviária–Bairro da Cruz e Parque das Rodovias–Cecap/Aldo Nassif, mas este protótipo não considera horários, sentido de circulação, trânsito, espera, custo de obra ou estado do pavimento. Antes de apresentar resultados como dados reais, confira cada ponto e cada trajeto no Google Maps e troque os pesos pelo comprimento medido.

O Google Maps está ligado nas tabelas e nos botões de cada aba para facilitar a conferência dos pontos e dos trajetos.

## Arquivos

- `app.py`: interface Streamlit e visualização dos grafos.
- `algoritmos.py`: implementação de Dijkstra, Prim e Kruskal.
- `dados_projetos.json`: vértices, conexões e pesos de demonstração.
- `requirements.txt`: bibliotecas usadas.

## Fontes consultadas

- Prefeitura de Lorena, horários de ônibus: <https://www.lorena.sp.gov.br/wordpress/index.php/horario-de-onibus-lorena-2/>
- Prefeitura de Lorena, programação de linhas por bairros: <https://www.lorena.sp.gov.br/wordpress/index.php/parque-rodovias-x-cecap-3/>
- Prefeitura de Lorena, horários da linha Rodoviária–Bairro da Cruz: <https://www.lorena.sp.gov.br/wordpress/index.php/horario-de-onibus-lorena-2/>
- Prefeitura de Lorena, recapeamento em bairros: <https://www.lorena.sp.gov.br/wordpress/index.php/2023/01/23/prefeitura-inicia-obras-de-recapeamento-da-av-targino-vilela-nunes/>
- LATAM, anúncio de rotas do Embraer E195-E2: <https://www.latamairlines.com/br/pt/imprensa/noticias/latam-airlines-brasil-anuncia-42-rotas-da-primeira-fase-de-opera>
- LATAM, conexões da companhia no Nordeste: <https://www.latamairlines.com/br/pt/imprensa/noticias/latam-investe-na-conectividade-internacional-do-nordeste-brasile>

Consulta das páginas: 27/10/2026. A oferta de voos e os horários de transporte podem mudar.
