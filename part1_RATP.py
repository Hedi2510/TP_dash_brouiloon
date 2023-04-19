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
    ], className="row")
])
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
    ], className="row")
])






