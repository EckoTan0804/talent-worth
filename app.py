import os

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_daq as daq
import pandas as pd
import plotly.express as px

from utils import set_fig_layout

####################################### Mock up log-in ###########################################################
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'Alex': '1234'
# }
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country", size_max=60)
fig = set_fig_layout(fig)

df2 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
fig2 = px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")
fig2 = set_fig_layout(fig2)


def init_value_setter_store():
    # Initialize store data
    state_dict = {"a": 1}
    return state_dict


####################################### Layout elements ###########################################################
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4("TalentWorth"),
                    html.H6("Make your skills with future trend"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    # html.H5(f"Hello, {list(VALID_USERNAME_PASSWORD_PAIRS.keys())[0]}"),
                    html.Button(id="log-out-button",
                                children="LOG OUT", n_clicks=0),
                    html.Img(id="logo", src=app.get_asset_url(
                        "logo2.png"), style={'height':'20%', 'width':'20%'}),

                ],

            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="job-trend",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        # id="Specs-tab",
                        label="Job Trend",
                        value="job-trend",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        # id="Control-chart-tab",
                        label="Match Skills",
                        value="match-skills",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        # id="Control-chart-tab",
                        label="About Us",
                        value="about-us",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


####################################### Job trend tab ###########################################################

def build_job_trend_tab():
    return html.Div(
        id="status-container",
        children=[
            build_quick_stats_panel(),
            html.Div(id="graphs-container", children=[
                build_top_panel(),
                build_chart_panel()
            ])
        ]
    )


def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(id="utility-card",
                     children=[daq.StopButton(id="stop-button", size=160, n_clicks=0, children="Click")],),
        ],
    )


def build_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Chart 1"),
                    html.Div(children=[
                        dcc.Graph(
                            id="control-chart-live",
                            figure=fig2,
                        ),
                    ]),
                ]
            )
        ]
    )


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Chart 2"),
            dcc.Graph(id="conrol-chart-live", figure=fig)
        ]
    )

####################################### Match skills tab ##########################################################


def build_match_skills_tab():
    pass


####################################### About us tab ##############################################################

def build_about_us_tab():
   
   
    return html.Div(children=[
        html.H3('Group Members: ',
            style = {
                'textAlign' : 'center',
                'color' : '#FFFFFF'
            }
        ),
        html.H6(children = 'Linh',
            style = {
                'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),
        html.H6(children = 'Haobin',
            style = {
                'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),

        html.H6(children = 'Vinu',
            style = {
               'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40,
            }
        ),
        html.H6(children = 'Kathi',
            style = {
                'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),
        html.H6(children = 'Grace',
            style = {
               'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),
        html.Br(),
        html.H3('Sources: ',
            style = {
                'textAlign' : 'center',
                'color' : '#FFFFFF'
            }
        ),
        html.H6(['Source 1: ', html.A('link', href = 'https://www.onetcenter.org/database.html#individual-files')],
            style = {
               'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),
        html.H6(['Source 2: ', html.A('link', href = 'https://www.peopledatalabs.com/related-title-dataset?utm_source=kaggle&Utm_medium=social&utm_campaign=related-title-dataset')],
            style = {
               'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),
        html.H6(['Source 3: ', html.A('link', href = 'https://www.kaggle.com/maneeshdisodia/employment-skills')],
            style = {
               'textAlign' : 'left',
                'color' : '#FFFFFF',
                'marginLeft': 40
            }
        ),

        dcc.Dropdown(
            id = "data-sources",
            options=[
                {'label': 'Source 1', 'value': 'link1'},
                {'label': 'Source 2', 'value': 'link2'},
                {'label': 'Source 3', 'value': 'link3'},
            ]
        )
    ])
         
     
        

   

####################################### Callbacks ##############################################################


@app.callback(Output("app-content", "children"), [Input("app-tabs", "value")])
def render_tab_content(tab_switch):
    if tab_switch == "job-trend":
        return build_job_trend_tab()
    elif tab_switch == "match-skills":
        return build_match_skills_tab()
    return build_about_us_tab()


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
