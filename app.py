import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Charger les données RATP
df_ratp = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')

# Top 10 des stations avec le plus grand trafic
top10 = df_ratp.groupby("Station").sum().sort_values("Trafic", ascending=False)[:10].reset_index()

# Trafic par ville (Top 5)
trafic_ville = df_ratp.groupby("Ville").sum().sort_values("Trafic", ascending=False)[:5].reset_index()

# Charger les données IDF
df_idf = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
df_idf[['lat', 'lng']] = df_idf['Geo Point'].str.split(',', expand=True)
df_idf['lat'] = df_idf['lat'].str.strip().astype(float)
df_idf['lng'] = df_idf['lng'].str.strip().astype(float)

# Nombre de stations par exploitant
stations_par_exploitants = df_idf.groupby("exploitant").count().reset_index()
fig_bar_idf = px.bar(stations_par_exploitants, x="exploitant", y="nom_long", color="exploitant", title="Nombre de stations par exploitant")

# Trafic par mode de transport (pie chart)
trafic_mode = df_ratp.groupby("Réseau").sum().reset_index()
fig_pie_idf = px.pie(trafic_mode, values='Trafic', names='Réseau', title='Répartition du trafic par mode de transport')


# Nombre de stations par ligne
stations_par_ligne = df_idf.groupby("ligne").count().reset_index()
fig_bar_ligne = px.bar(stations_par_ligne, x="ligne", y="nom_long", color="ligne", title="Nombre de stations par ligne")

# Création de la figure pour la carte
fig_map_idf = px.scatter_mapbox(df_idf, lat="lat", lon="lng", color="ligne", hover_name="nom", zoom=10, height=600)
fig_map_idf.update_layout(mapbox_style="open-street-map")

# Création du layout de l'application
app = Dash(__name__)
app.layout = html.Div([
    html.Center(html.H1("RATP data visualization", style={'background-color': 'lightblue'})),
    html.Div([
        html.Div([
            dcc.Graph(id='graph_bar_ratp', figure=fig_bar_idf)
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='graph_pie_ratp', figure=fig_pie_idf)
        ], className="six columns"),
    ], className="row"),
    html.Center(html.H2("IDF data visualization", style={'font-size': '36px', 'background-color': 'lightblue'})),
    html.Div([
        html.Div([
            dcc.Graph(id='graph_bar_idf', figure=fig_bar_idf)
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='graph_bar_ligne', figure=fig_bar_ligne)
        ], className="six columns"),
    ], className="row"),
    html.Center(html.H2("Map of subway stations in Paris", style={'font-size': '36px', 'background-color': 'lightblue'})),
    dcc.Graph(id='map_idf', figure=fig_map_idf)
])

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
