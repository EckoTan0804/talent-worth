import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly

from app import app

VALID_USERNAME_PASSWORD_PAIRS = {
    'Alex': '1234'
}

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


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
                    html.H5(
                        f"Hello, {list(VALID_USERNAME_PASSWORD_PAIRS.keys())[0]}"),
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
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
