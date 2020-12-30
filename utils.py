from plotly.graph_objs import Layout


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
