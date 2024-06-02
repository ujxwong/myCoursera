# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique values from the 'Launch Site' column
unique_launch_sites = spacex_df['Launch Site'].unique()

# Create a dictionary with keys matching the unique values
launch_sites_list = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in unique_launch_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(id='site-dropdown',
            options=launch_sites_list,
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        #dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={0: '0', 100: '100'}
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        # Create a pie chart for all sites
        piechart = px.pie(data_frame=spacex_df, names='Launch Site', values='class', title='Total Launches for All Sites')

    else:
        # Create a pie chart for the specific site
        specific_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]

        success_count = len(specific_df[specific_df['class'] == 1])
        failed_count = len(specific_df[specific_df['class'] == 0])
 
        # Create a pie chart for the specific site
        piechart = px.pie(
            data_frame=specific_df,
            names=['Success', 'Failed'],
            title=f'Total Launches for {site_dropdown}',
            labels={'1': 'Success', '0': 'Failed'},
            values=[success_count, failed_count]
        )
        
    return piechart
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def build_scatter_chart(site_dropdown, payload_range):
    if site_dropdown == 'ALL':
        # Create a scatter plot for all sites
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        scatter_chart = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Success (All Sites)',
            labels={'class': 'Launch Outcome'}
        )
    else:
        # Filter the dataframe for the specific site
        specific_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_specific_df = specific_df[(specific_df['Payload Mass (kg)'] >= payload_range[0]) &
                                          (specific_df['Payload Mass (kg)'] <= payload_range[1])]
        scatter_chart = px.scatter(
            filtered_specific_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Success ({site_dropdown})',
            labels={'class': 'Launch Outcome'}
        )

    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)
