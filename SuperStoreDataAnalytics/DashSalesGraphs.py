# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the Sales data into pandas dataframe
Sales = pd.read_csv("Superstore.csv",encoding='windows-1252')
NegativeProfit = Sales[Sales['Profit'] <= 0]
PostiveProfit = Sales[Sales['Profit'] > 0]
NegativeProfit['Profit'] = NegativeProfit['Profit']*(-1)
Sales['Order Date'] = pd.to_datetime(Sales['Order Date'],dayfirst = True)
#Copyed sum code from my notebook
DateSalesAndProfit = Sales.groupby('Order Date',as_index = False).sum()
onefour = int(len(DateSalesAndProfit)/4)
twofour = int(onefour * 2)
threefour = int(twofour + len(DateSalesAndProfit)/4)
fourfour = int(twofour * 2)


#Dash application
app = dash.Dash(__name__)

#App layout
app.layout = html.Div(children=[html.H1('Super Store Sales Data',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='Profit-dropdown',
                                                                                    options=[
                                                                                    {'label': 'Negative Profit', 'value': 'NegativeProfit'},
                                                                                    {'label': 'Postive Profit', 'value': 'PostiveProfit'}
                                                                                    ],
                                                                                    value='Postive Profit',
                                                                                    placeholder="Postive Profit",
                                                                                    searchable=True
                                                                                            ),
                                dcc.Dropdown(id = 'Feature-dropdown',
                                                                options = [{'label':'Ship Mode', 'value' : 'Ship Mode' },
                                                                            {'label':'Top 5 States', 'value' : 'State'},
                                                                            {'label':'Category', 'value' : 'Category'},
                                                                            {'label':'Sub-Category', 'value' : 'Sub-Category'},
                                                                            {'label':'Segment', 'value' : 'Segment'}],
                                                                            value = 'Category',
                                                                            placeholder = 'Category',
                                                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Date Slider For Profit vs Time Graph"),
                                # TASK 3: Add a slider to select payload range,
                                dcc.Dropdown(id = '4thsSelecter', options = [{'label': '1st quarter','value': '1/4'},
                                                                             {'label':'2int quarter','value':'2/4'},
                                                                             {'label':'3rd quarter','value':'3/4'},
                                                                             {'label':'4th quarter','value':'4/4'}],
                                                                             value = '1/4',
                                                                             placeholder  = '1st quarter'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='Order-Date-scatter-chart'))
                                
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='Profit-dropdown', component_property='value'),Input(component_id='Feature-dropdown',component_property='value')])
def get_pie_chart(entered_site,feature):
    if entered_site == 'PostiveProfit':
        if feature == 'Sub-Category':
            fig = px.pie(PostiveProfit, values='Profit', 
            names='Sub-Category', 
            title='Pie Chart of Postive Profit Sub-Category')
            return fig
        if feature == 'Category':
            fig = px.pie(PostiveProfit, values='Profit', 
            names='Category', 
            title='Pie Chart of Postive Profit Category')
            return fig
        if feature == 'State':
            ByState = PostiveProfit.groupby('State').sum().sort_values('Profit' , ascending = False)
            ListOfStates = PostiveProfit.groupby('State').sum().sort_values('Profit' , ascending = False).index.values[0:5]
            fig = px.pie(ByState[0:5], values='Profit', 
            names=ListOfStates, 
            title='Pie Chart of Postive Profit State')
            return fig
        if feature == 'Segment':
            fig = px.pie(PostiveProfit, values='Profit', 
            names='Segment', 
            title='Pie Chart of Postive Profit Segment')
        if feature == 'Ship Mode':
            fig = px.pie(PostiveProfit, values='Profit', 
            names='Ship Mode', 
            title='Pie Chart of Postive Profit Ship Mode') 
    else:
        if feature == 'Sub-Category':
            fig = px.pie(NegativeProfit, values='Profit', 
            names='Sub-Category', 
            title='Pie Chart of Negative Profit Profit Sub-Category')
            return fig
        if feature == 'Category':
            fig = px.pie(NegativeProfit, values='Profit', 
            names='Category', 
            title='Pie Chart of Negative Profit Profit Category')
            return fig
        if feature == 'State':
            ByState = NegativeProfit.groupby('State').sum().sort_values('Profit' , ascending = False)
            ListOfStates = NegativeProfit.groupby('State').sum().sort_values('Profit' , ascending = False).index.values[0:5]
            fig = px.pie(ByState[0:5], values='Profit', 
            names=ListOfStates, 
            title='Pie Chart of Negative Profit Profit State')
            return fig
        if feature == 'Segment':
            fig = px.pie(NegativeProfit, values='Profit', 
            names='Sub-Category', 
            title='Pie Chart of Negative Profit Profit Segment')
            return fig
        if feature == 'Ship Mode':
            fig = px.pie(NegativeProfit, values='Profit', 
            names='Sub-Category', 
            title='Pie Chart of Negative Profit Profit Ship Mode')
            return fig
# TASK 4:
# Callback function for 4th Selector for Profit vs Order Date

@app.callback(Output(component_id='Order-Date-scatter-chart', component_property='figure'),
               Input(component_id='4thsSelecter', component_property='value'))

def scatterPolt(quarterValue):
    if quarterValue == '1/4':
        fig = px.scatter(DateSalesAndProfit.iloc[:onefour,:],x = 'Order Date',y= 'Profit')
        return fig
    if quarterValue == '2/4':
        fig = px.scatter(DateSalesAndProfit.iloc[onefour:twofour,:],x = 'Order Date',y= 'Profit')
        return fig
    if quarterValue == '3/4':
        fig = px.scatter(DateSalesAndProfit.iloc[twofour:threefour,:],x = 'Order Date',y= 'Profit')
        return fig
    if quarterValue == '4/4':
        fig = px.scatter(DateSalesAndProfit.iloc[threefour:fourfour,:],x = 'Order Date',y= 'Profit')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()