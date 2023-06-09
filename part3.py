import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Charger les données RATP
df_ratp = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
print(df_ratp.head())

# Top 10 des stations avec le plus grand trafic
top10 = df_ratp.groupby("Station").sum().sort_values("Trafic", ascending=False)[:10].reset_index()

# Trafic par ville (Top 10)
trafic_ville = df_ratp.groupby("Ville").sum().sort_values("Trafic", ascending=False)[:10].reset_index()

# Création de la figure pour le graphique à barres
fig_bar_ratp = go.Figure(data=[go.Bar(x=top10["Station"], y=top10["Trafic"], text=top10["Trafic"], textposition='auto', marker_color='green')])
fig_bar_ratp.update_layout(title="TOP 10 stations with the biggest traffic")


# Création de la figure pour le graphique en camembert
fig_pie_ratp = px.pie(trafic_ville, values='Trafic', names='Ville', title='Pie chart trafic per cities')

# Charger les données IDF
df_idf = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
print(df_idf.head())

# Nombre de stations par exploitant
stations_par_exploitants = df_idf.groupby("exploitant").count().reset_index()
fig_bar_idf = px.bar(stations_par_exploitants, x="exploitant", y="nom_long", color="exploitant", title="Number of stations per operator")

# Nombre de stations par ligne
stations_par_ligne = df_idf.groupby("ligne").count().reset_index()
fig_bar_ligne = px.bar(stations_par_ligne, x="ligne", y="nom_long", color="ligne", title="Number of stations per lines")

# Création du layout de l'application
app = Dash(__name__)
app.layout = html.Div([
    html.Center(html.H1("RATP data visualization", style={'background-color': 'lightblue'})),
    html.Div([
        html.Div([
            dcc.Graph(id='graph_bar_ratp', figure=fig_bar_ratp)
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='graph_pie_ratp', figure=fig_pie_ratp)
        ], className="six columns"),
    ], className="row"),
    html.Center(html.H2("IDF data visualization", style={'font-size': '36px', 'background-color': 'lightblue'})),
    html.Div([
        html.Div([
            dcc.Dropdown(id='dropdown_exploitants',
                         options=[{'label': i, 'value': i} for i in df_idf['exploitant'].unique()],
                         value='SNCF',
                         placeholder='Select exploitant'),
            dcc.Graph(id='graph_bar_idf', figure=fig_bar_idf)
        ], className="six columns"),
        html.Div([
            dcc.Dropdown(id='dropdown_reseau',
                         options=[{'label': i, 'value': i} for i in df_ratp['Réseau'].unique()],
                         value='Métro',
                         placeholder='Select réseau'),
            dcc.Graph(id='graph_bar_ligne', figure=fig_bar_ligne)
        ], className="six columns"),
    ], className="row")
])

@app.callback(
    Output('graph_bar_ratp', 'figure'),
    Input('dropdown_reseau', 'value')
)
def update_bar_chart_reseau(reseau):
    filtered_df = df_ratp[df_ratp['Réseau'] == reseau]
    return px.bar(filtered_df, x='Station', y='Trafic', text='Trafic', title='Trafic per station')

@app.callback(
    Output('graph_bar_idf', 'figure'),
    Input('dropdown_exploitants', 'value')
)
def update_bar_chart_exploitants(exploitants):
    filtered_df = df_idf[df_idf['exploitant'] == exploitants]
    stations_par_exploitants = filtered_df.groupby("exploitant").count().reset_index()
    return px.bar(stations_par_exploitants, x="exploitant", y="nom", color="exploitant", title="Number of stations per operator")

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)

