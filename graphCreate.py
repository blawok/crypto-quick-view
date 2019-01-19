import plotly
import plotly.graph_objs as go
import json

def createPlot(df, x, y, plotType):
    """
    variables:
    df - dataframe from which the function creates the plot
    x - xaxis variable
    y - yaxis variable
    plotType - defines the plot type

    returns:
    plot depending on chosen plotType
    """
    if plotType == 'bar':
        data = [
            go.Bar(
                name = '{}'.format(y),
                x=df['{}'.format(x)],
                y=df['{}'.format(y)],
                marker = dict(color = '#a090b5')
            )]
        layout = dict(title = '{}'.format(y), yaxis=dict(
        title='{}'.format(y),
        titlefont=dict(
            family='Courier New, monospace',
            size=18
        )))
    elif plotType == 'scatter':
        data = [go.Scatter(
                name = '{}'.format(y),
                x=df['{}'.format(x)],
                y=df['{}'.format(y)],
                mode = 'lines+markers',
                marker = dict(color = '#ff4444'),

    )]
        layout = dict(title = '{}'.format(y), yaxis=dict(
        title='{}'.format(y),
        titlefont=dict(
            family='Courier New, monospace',
            size=18
        )))
    fig = dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def createPlotMultiple(df, x, y, y2, plotType):
    """
    variables:
    df - dataframe from which the function creates the plot
    x - xaxis variable
    y - first yaxis variable
    y2 - second yaxis variable
    plotType - defines the plot type

    returns:
    plot with multiple variables on yaxis, depending on chosen plotType
    """
    if plotType == 'scatter':
        plot1 = go.Scatter(
                name = '{}'.format(y),
                x=df['{}'.format(x)],
                y=df['{}'.format(y)],
                mode = 'lines+markers',
                marker = dict(color = '#42f450'),
                         )
        plot2 = go.Scatter(
                name = '{}'.format(y2),
                x=df['{}'.format(x)],
                y=df['{}'.format(y2)],
                mode = 'lines+markers',
                marker = dict(color = '#ff4444'),
                         )
        data = [plot1, plot2]
        layout = dict(title = '{}'.format(y), yaxis=dict(
        title='{}'.format(y),
        titlefont=dict(
            family='Courier New, monospace',
            size=18
        )))
    fig = dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
