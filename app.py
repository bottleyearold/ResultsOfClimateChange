
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
import math
import dash_bootstrap_components as dbc

# Load your data
data_path = '/Users/fionamagee/Desktop/ResultOfClimateChange/NaturalDisaterDataSet.csv'
data = pd.read_csv(data_path)
file_path1 = '/Users/fionamagee/Desktop/ResultOfClimateChange/ChangeInSeaLevels.csv'
data1 = pd.read_csv(file_path1)

# Clean the 'Indicator' column
data['Indicator'] = data['Indicator'].str.replace('Climate related disasters frequency, Number of Disasters: ', '')
data = data[data['Indicator'] != 'TOTAL']

# Drop unnecessary columns
columns_to_drop = ['ObjectId', 'ISO2', 'ISO3', 'Unit', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor']
data = data.drop(columns=columns_to_drop)

# Rename columns for clarity
data.rename(columns={'Country': 'country'}, inplace=True)

# Convert the dataset from wide format to long format
melted_data = pd.melt(data, id_vars=['country', 'Indicator'], value_vars=[f'F{year}' for year in range(1980, 2023)],
                      var_name='year', value_name='Count')
melted_data['year'] = melted_data['year'].str.replace('F', '')
melted_data['year'] = melted_data['year'].astype(int)  # Convert year to int for easier handling


columns_to_drop = ['ObjectId', 'ISO2', 'ISO3', 'Indicator', 'Unit', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor']
data_cleaned = data1.drop(columns=columns_to_drop)

# Convert the Date column to datetime
data_cleaned['Date'] = pd.to_datetime(data_cleaned['Date'].str.lstrip('D'), format='%m/%d/%Y', errors='coerce')

# Extract the year from the Date column
data_cleaned['Year'] = data_cleaned['Date'].dt.year

# Rename columns for clarity
data_cleaned.rename(columns={'Measure': 'measure'}, inplace=True)

# Convert the dataset from wide format to long format
data_tidy = pd.melt(data_cleaned, id_vars=['measure', 'Year'], var_name='variable', value_name='Sea_Level_Change')
data_tidy['Year'] = pd.to_numeric(data_tidy['Year'], errors='coerce', downcast='integer')

data_tidy['Sea_Level_Change'] = pd.to_numeric(data_tidy['Sea_Level_Change'], errors='coerce')

# Drop any rows that might have NaN values after coercion
data_tidy.dropna(subset=['Year', 'Sea_Level_Change'], inplace=True)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, './assets/main.css'])

server = app.server

navbar = html.Div(
    [
        dbc.NavbarBrand("Information and Statistics", href="#", style={"color": "white", "width": "100%", "display": "block", "textAlign": "center", "padding-bottom": "8px", "padding-top": "10px","font-size": "20px", 'font-weight': '500'}),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Overview", href="#", style= {"padding-left": "35px", "padding-right": "35px", 'color': 'white'})),
                dbc.NavItem(dbc.NavLink("Result of Climate Change", href="#", style= {"padding-left": "35px", "padding-right": "35px", 'color': 'white'})),
                dbc.NavItem(dbc.NavLink("Temperature Change", href="https://finaldashboard-4.onrender.com", style= {"padding-left": "35px", "padding-right": "35px", 'color': 'white'})),
                dbc.NavItem(dbc.NavLink("More References", href="MoreReference.html", style= {"padding-left": "35px", "padding-right": "35px", 'color': 'white'})),
            ],
            className="ms-auto",
            navbar=True,
            style={"width": "100%", "display": "flex", "justifyContent": "center", "padding-bottom": "8px", 'border-bottom': '2px solid white'}
        ),
    ],
    style={
        "backgroundColor": "#132c48ff",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "width": "100%",
    }
)

app.layout = html.Div([
    html.Div([
        navbar,
    ]),
    html.H1('Results of Climate Change', style={'padding-left':'20px', 'padding-top': '20px'}),
    html.P('Climate change is causing widespread and severe impacts on our planet. Rising global temperatures are leading to more frequent and intense heatwaves, exacerbating droughts in some regions while increasing heavy rainfall and flooding in others. Melting ice caps and glaciers contribute to rising sea levels, threatening coastal communities with erosion and inundation. Ocean acidification, a result of increased carbon dioxide levels, is damaging marine ecosystems, affecting coral reefs and the species that depend on them. Additionally, changing weather patterns are disrupting agriculture, leading to food shortages and economic instability. The health of populations is also at risk, with increased occurrences of heat-related illnesses and vector-borne diseases. These impacts necessitate urgent action to mitigate climate change and adapt to its effects.', style={'padding-left':'20px', 'padding-right': '20px'}),

    html.Div([

    html.Div([
    html.Div(id='default-text', children='Select', style={'display': 'none'}),

    html.Div([
    
        html.Div(
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in np.sort(melted_data['country'].unique())],
                placeholder="World",  # Placeholder changed to 'World'
                multi=False
            ),
            style={'width': '50%', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.RangeSlider(
                id='year-range-slider',
                min=melted_data['year'].min(),
                max=melted_data['year'].max(),
                step=1,
        
                value=[melted_data['year'].min(), melted_data['year'].max()],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            style={'width': '50%', 'display': 'inline-block'}
        ),
    ],style={'display': 'flex', 'flex-direction': 'row'}
    ),
    dcc.Graph(id='bar-chart')
], className='graph-area'),
    html.Img(
        src='./assets/infographic.png', className = 'polar-bear-area'
    ), 
], className= 'content-area'),

html.Div([
    html.Div([
        html.H1('Understanding the Multifaceted Dangers of Climate Change ', style= {'padding-left':'30px'}),
        html.P('Climate change represents one of the most significant global challenges of the 21st century. It is a complex issue with far-reaching effects that go beyond the environmental sphere, impacting economic, social, and political dimensions of human societies worldwide. Here are the key reasons why climate change poses such a profound threat to life on Earth:', style= {'padding-left':'30px'}),
        html.Ol([
        html.Li('Rising Sea Levels: As global temperatures increase, ice caps and glaciers melt, leading to a rise in sea levels. This can result in the loss of coastal habitats, increased flooding, and the displacement of communities, as well as the potential submersion of low-lying islands and cities.'),
        html.Li('Extreme Weather Events: Climate change is linked to an increase in the frequency and severity of extreme weather events like hurricanes, heatwaves, droughts, and heavy rainfall, which can lead to devastating consequences for communities and economies.'),
        html.Li('Disruption of Ecosystems: Warming temperatures can disrupt the balance of different ecosystems, leading to the loss of biodiversity.'),
        html.Li('Health Risks: Higher temperatures and altered weather patterns can worsen air quality and increase the prevalence of diseases transmitted by water and insects.'),
        html.Li('Food Security: Climate change can affect agricultural production due to changes in rainfall patterns, droughts, and increased temperatures.'),
        ], style= {'padding-left':'50px', 'padding-bottom': '20px'}),
        html.Div([
        

    html.Div(
    dcc.Dropdown(
        id='measure-dropdown',
        # Initially, all options are available
        options=[{'label': i, 'value': i} for i in np.sort(data_tidy['measure'].unique())],
        # Default value set to 'World'
        value='World',
        multi=False
    ),style={'width': '50%', 'display': 'inline-block'}),

    html.Div(
    dcc.RangeSlider(
        id='year-slider',
        min=int(data_tidy['Year'].min()),
        max=int(data_tidy['Year'].max()),
        value=[int(data_tidy['Year'].min()), int(data_tidy['Year'].max())],
        step=1,
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ), style={'width': '50%', 'display': 'inline-block'}
    ),
    dcc.Graph(id='line-chart', style={'padding-bottom': '20px'}), 
],style={'flex': '1', 'minWidth': '700px','padding-left':'30px'}, )
    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '50%', 'alignItems': 'flex-start'}),
    html.Div([
        html.Img(src='./assets/tornado.png', style= {'padding-left': '20px','padding-right': '20px','padding-bottom': '20px', 'padding-top': '100px',  'height':'500px', 'width': '600px', 'margin-left': '100px' }),  # Replace with your image sources
        html.Img(src='./assets/flood.png', style= {'padding-left': '20px','padding-right': '20px','padding-bottom': '20px', 'padding-top': '40px', 'height':'450px', 'width': '600px', 'margin-left': '100px'}),
    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '50%', 'alignItems': 'flex-start',  'overflow': 'visible'})
], style={'display': 'flex', 'flex-direction': 'row'})

])
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('default-text', 'style')],
    [Input('country-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_figure(selected_country, selected_years):
    # If no country is selected, assume 'World' is the default
    if not selected_country:
        selected_country = 'World'

    # If 'World' is the current selection, aggregate all data
    if selected_country == 'World':
        filtered_data = melted_data.copy()
    else:
        # Otherwise, filter by the selected country
        filtered_data = melted_data[melted_data['country'] == selected_country]
    
    # Filter by the selected years
    filtered_data = filtered_data[(filtered_data['year'] >= selected_years[0]) & (filtered_data['year'] <= selected_years[1])]

    # Group and sum the data for the bar chart
    grouped_data = filtered_data.groupby(['Indicator', 'year'], as_index=False).sum()

    # Create the figure
    fig = px.bar(grouped_data, x='year', y='Count', color='Indicator',
                 title="Frequency of Climate-Related Disasters",
                 labels={'Count': 'Number of Disasters', 'year': 'Year'},
                 barmode='stack')

    # Determine whether to show or hide the 'default-text' based on selection
    text_style = {'display': 'block'} if selected_country == 'World' else {'display': 'none'}

    return fig, text_style

@app.callback(
    Output('line-chart', 'figure'),
    [Input('measure-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_measure, year_range):

    
    # Convert the year range values to integers
    year_start, year_end = map(int, year_range)

    # Filter the data based on the selected measure and year range
    filtered_data = data_tidy[(data_tidy['Year'] >= year_start) & (data_tidy['Year'] <= year_end)]

    if selected_measure:
        filtered_data = filtered_data[filtered_data['measure'] == selected_measure]

    # Group the filtered data by 'Year' and calculate the mean 'Sea_Level_Change' for each year
    annual_average = filtered_data.groupby('Year')['Sea_Level_Change'].mean().reset_index()

    # Create the figure with the annual average data
    fig = px.line(annual_average, x='Year', y='Sea_Level_Change', title='Average Annual Sea Level Change for ' + selected_measure)

    # Update layout of the figure
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Sea Level Change (mm)',
        showlegend=False
    )

    return fig

@app.callback(
    Output('measure-dropdown', 'options'),
    [Input('measure-dropdown', 'value')]
)
def remove_world_option(selected_measure):
    if selected_measure != 'World':
        return [{'label': i, 'value': i} for i in np.sort(data_tidy['measure'].unique()) if i != 'World']
    # If 'World' is selected or it is the initial load, return all options
    return [{'label': i, 'value': i} for i in np.sort(data_tidy['measure'].unique())]
# Run the app
if __name__ == '__main__':
    app.run(jupyter_mode='tab', debug=True, port= 8054) 