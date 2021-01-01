from plotly.graph_objs import Layout
import plotly.graph_objects as go
import pandas as pd
import numpy as np

GRID_COLOR = "#595959"


class PolarPlot():

    def __init__(self):
        self.figure = go.Figure()  # instatiates plotly figure
        self.range = (0, 0)  # define the initial range of polar plots
        self.theta = ['Business Analyst', 'Data Analyst', 'Data Scientist', 'Data Engineer/DBA',
                      'Software Engineer', 'Statistician/Research Scientist', 'Business Analyst']  # Those are the Theta values for our plot

    def update_common_layout(self):
        """
        Updates general layout characteristics
        """
        self.figure.update_layout(
            showlegend=True,
            legend_itemclick='toggleothers',
            legend_itemdoubleclick='toggle',
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            autosize=True,
            font_color="white",
            uirevision=True,
            height=600,
        )

    def update_commom_polar_layout(self):
        """
        Updates polar layout characteristics
        """
        self.figure.update_layout(
            polar_bgcolor='rgba(0, 0, 0, 0)',

            polar_radialaxis_visible=True,
            polar_radialaxis_showticklabels=True,
            polar_radialaxis_tickfont_color='darkgrey',
            polar_radialaxis_showline=False,
            polar_radialaxis_layer='below traces',
            polar_radialaxis_gridcolor='gray',
            polar_radialaxis_range=self.range,

            polar_angularaxis_color='gray',
            polar_angularaxis_showline=True,
        )

    def add_data(self, data, country, hover_template='%{r:0.0f}%'):
        """
        Adds a trace to the figure following the same standard for each trace
        """
        data.append(
            data[0])  # add the first element to the end of the list, this will "close" the polar chart
        self.figure.add_trace(
            go.Scatterpolar(
                r=data,
                theta=self.theta,
                mode='lines',
                name=country,
                hoverinfo='name+r',
                hovertemplate=hover_template,
                showlegend=True,
                line_shape='spline',
                line_smoothing=0.8,
                line_width=3
            )
        )
        # Calls the method that will update the max range
        self.update_range(data)

    def update_range(self, data):
        """
        Updates the range to be 110% of maximum value of all traces
        """
        max_range = max(data) * 1.1
        # updates the range attribute
        self.range = (
            0, max_range) if max_range > self.range[1] else self.range

    def get_figure(self):
        """
        Update layouts and shows the figure
        """
        self.update_common_layout()
        self.update_commom_polar_layout()
        return self.figure

##############################################################################################


class LinePlot():

    def __init__(self):
        self.figure = go.Figure()
        self.range = (0, 100)

    def update_axis_title(self, x, y):
        self.figure.update_layout(
            xaxis_title_text=x,
            yaxis_title_text=y,
        )

    def update_layout(self):
        """
        Creates a clean layout for ploting, adjusting multiple settings
        """
        self.figure.update_layout(
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            showlegend=True,
            legend_font_color='gray',
            legend_itemclick='toggleothers',
            legend_itemdoubleclick='toggle',
            xaxis={
                "visible": True,
                "showgrid": False,
                "gridwidth": 0.8,
                # "color": "white",
            },
            yaxis={
                "showgrid": True,
                "gridcolor": GRID_COLOR,
                "gridwidth": 0.5,
            },
            font_color='white'
        )

    def add_data(self, x_names, y_data, trace_name, hover_template):
        """
        Adds a trace to the figure following the same standard for each trace
        """
        self.figure.add_trace(
            go.Scatter(
                x=x_names,
                y=y_data,
                mode='lines',
                name=trace_name,
                hoverinfo='name+y',
                hovertemplate=hover_template,
                line_shape='spline',
                line_smoothing=0.8,
                line_width=2
            )
        )

    def get_figure(self):
        self.update_layout()
        return self.figure


###############################################################################################

def set_fig_layout(fig):
    layout = Layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        autosize=True,
        font_color="white",
        uirevision=True,
        height=400,
        # margin=dict(l=0, r=0, t=4, b=4),

    )
    return fig.update_layout(layout)


# This function will be used to create different aggegations for plotting
def plot_lines(line_plot, data, traces, x_names, agg_column, group_column, trace_column, hover_template):
    """
    Creates aggregation to plot
    """
    for trace_name in traces:
        data_filtered = data[data[trace_column] == trace_name]
        plot_data = data_filtered.groupby([group_column], as_index=False).agg({
            agg_column: ['mean', 'count']})
        plot_data = plot_data[agg_column]['mean'].tolist()
        line_plot.add_data(x_names, plot_data, trace_name,
                           hover_template=hover_template)


job_proportion_polar_plot = PolarPlot()
time_of_coding_line_plot = LinePlot()
salary_line_plot = LinePlot()
job_skills_polar_plot = PolarPlot()

####################################################################################################
kaggle_csv_link = "https://gist.githubusercontent.com/EckoTan0804/7ba61515d185c6558f77504044b485bb/raw/4caac4c296138e0d40aa22c90ae38d712ba0531d/multiple_choice_responses_preprocessed.csv"
kaggle = pd.read_csv(kaggle_csv_link)


def get_salary_line_plot():
    traces = [
        'Business Analyst',
        'Data Analyst',
        'Data Scientist',
        'Data Engineer/DBA',
        'Software Engineer',
        'Statistician/Research Scientist'
    ]
    x_names = [
        '0-49 employees',
        '50-249 employees',
        '250-999 employees',
        '1000-9,999 employees',
        '> 10,000 employees'
    ]
    plot_lines(
        salary_line_plot,
        data=kaggle,
        traces=traces,
        x_names=x_names,
        agg_column='Salary',
        group_column='CompanySize',
        trace_column='JobTitle',
        hover_template='U$%{y:,.2r}'
    )

    xaxis_title = 'Company size'
    yaxis_title = 'Average Salary (USD per Year)'
    salary_line_plot.update_axis_title(xaxis_title, yaxis_title)
    return salary_line_plot
