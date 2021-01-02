import os

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_daq as daq
import pandas as pd
import plotly.express as px

import utils

####################################### Mock up log-in ###########################################################
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'Alex': '1234'
# }
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server


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
                    html.Div(
                        [
                            html.A(
                                html.Button("View on Github",
                                            id="view-on-github"),
                                href="https://github.com/EckoTan0804/talent-worth",

                            )
                        ]

                    ),
                    # html.Img(id="logo", src=app.get_asset_url(
                    #     "talent-worth-logo.jpeg")),
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


@ app.callback(Output("app-content", "children"), [Input("app-tabs", "value")])
def render_tab_content(tab_switch):
    if tab_switch == "job-trend":
        return build_job_trend_tab()
    elif tab_switch == "match-skills":
        return build_match_skills_tab()
    return build_about_us_tab()


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


####################################### Job trend tab ###########################################################

def build_job_trend_tab():
    return html.Div(
        # id="status-container",
        className="status-container",
        children=[
            build_job_trend_control_panel(),
            html.Div(id="graphs-container", children=[
                build_job_trend_top_panel(),
                build_job_trend_chart_panel()
            ])
        ]
    )


def build_job_trend_control_panel():
    return html.Div(
        id="quick-stats-job-trend",
        className="row",
        children=[
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Job proportion"),
                    html.Br(),
                    dcc.Dropdown(
                        id="single-country-dropdown",
                        options=[{"label": country, "value": country}
                                 for country in utils.get_countries()],
                        value="China",
                        clearable=False,
                    ),
                    # html.Div(
                    #     id="utility-card-job-trend",
                    #     children=[
                    #         html.Button(
                    #             id="job-proportion-confirm-button",
                    #             className="confirm-button",
                    #             children="Confirm"
                    #         )
                    #     ]
                    # ),

                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Job proportion in different country"),
                    html.Br(),
                    dcc.Dropdown(
                        id="multi-country-dropdown",
                        options=[{"label": country, "value": country}
                                 for country in utils.get_countries()],
                        value=["China"],
                        multi=True,
                        clearable=False,
                    ),
                    # html.Div(
                    #     id="utility-card-job-trend",
                    #     children=[
                    #         html.Button(
                    #             id="job-proportion-different-country-confirm-button",
                    #             className="confirm-button",
                    #             children="Confirm"
                    #         )
                    #     ]
                    # ),
                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Job Titles"),
                    html.Br(),
                    dcc.Checklist(
                        id="job-titles-multi-select",
                        options=[{"label": job, "value": job}
                                 for job in utils.get_job_titles()],
                        value=["Data Scientist"]
                    ),
                    # html.Div(
                    #     id="utility-card-job-trend",
                    #     children=[
                    #         html.Button(
                    #             id="job-titles-confirm-button",
                    #             className="confirm-button",
                    #             children="Confirm"
                    #         )
                    #     ]
                    # ),
                ]
            ),

        ],
    )


def build_job_trend_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner(
                        "Job Proportion in Different Country"),
                    html.Div(
                        id="metric-div",
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id="job-proportion-differnet-countries-polar",
                                        figure=utils.get_job_proportion_polar_plot(
                                            ["China"]).get_figure()
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Job Proportion"),
                    dcc.Graph(
                        id="job-proportion-pie",
                        figure=utils.get_job_propotion_pie_chart("China")
                    )
                ],
            ),
        ],
    )


@app.callback(
    Output("multi-country-dropdown", "value"),
    Output("job-proportion-pie", "figure"),
    Input("single-country-dropdown", "value"),
    State("multi-country-dropdown", "value"),
)
def update_job_proportion_pie_chart(selected_country, current_selected_countries):
    if selected_country not in current_selected_countries:
        current_selected_countries.append(selected_country)
    return current_selected_countries, utils.get_job_propotion_pie_chart(selected_country)


@app.callback(
    Output("job-proportion-differnet-countries-polar", "figure"),
    Input("multi-country-dropdown", "value"),
)
def update_job_proportion_polar_plot(selected_countries):
    return utils.get_job_proportion_polar_plot(selected_countries).get_figure()


def build_job_trend_chart_panel():
    return html.Div(
        # id="control-chart-container",
        className="panel",
        children=[
            generate_section_banner("Salary"),
            dcc.Graph(id="salary-line-plot",
                      figure=utils.get_salary_line_plot().get_figure())
        ]
    )


@app.callback(
    Output("salary-line-plot", "figure"),
    Input("job-titles-multi-select", "value"),
)
def update_salary_line_plot(selected_job_titles):
    return utils.get_salary_line_plot(job_titles=selected_job_titles).get_figure()


####################################### Match skills tab ##########################################################


def build_match_skills_tab():
    return html.Div(
        className="status-container",
        children=[
            build_match_skills_control_panel(),
            html.Div(
                id="graphs-container",
                children=[
                    build_match_skills_top_panel(),
                    build_match_skills_chart_panel()
                ])
        ]
    )


def build_match_skills_control_panel():
    return html.Div(
        id="quick-stats-match-skills",
        className="row",
        children=[
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Skills in Job Description"),
                    html.Br(),
                    dcc.Checklist(
                        options=[{"label": job, "value": job}
                                 for job in utils.get_programming_language()],
                        value=["Python"]
                    ),
                    html.Div(
                        id="utility-card-job-trend",
                        children=[daq.StopButton(id="stop-button",
                                                 children="Confirm")]
                    ),
                ]
            ),
            html.Div(
                id="metric-select-menu",
                className='ten columns',
                children=[
                    html.H5("Time writing codes"),
                    html.Br(),
                    dcc.Checklist(
                        options=[{"label": job, "value": job}
                                 for job in utils.get_time_writing_code()],
                        value=["Python"]
                    ),
                    html.Div(
                        id="utility-card-job-trend",
                        children=[daq.StopButton(id="stop-button",
                                                 children="Confirm")]
                    ),
                ]
            ),

        ],
    )


def build_match_skills_top_panel():
    return html.Div(
        id="top-section-container-match-skills",
        className="row",
        children=[
            html.Div(
                className="panel",
                children=[
                    generate_section_banner(
                        "Skills in Job Description"),
                    dcc.Graph(
                        id="job-skills-desc-polar",
                        figure=utils.get_job_skills_polar_plot().get_figure()
                    )
                ]
            )
        ],
    )


def build_match_skills_chart_panel():
    return html.Div(
        # id="control-chart-container",
        className="panel",
        children=[
            generate_section_banner("Salary"),
            dcc.Graph(id="conrol-chart-live",
                      figure=utils.get_prog_language_line_plot().get_figure())
        ]
    )


####################################### About us tab ##############################################################

def build_about_us_tab():
    pass


################################################################################################################
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
