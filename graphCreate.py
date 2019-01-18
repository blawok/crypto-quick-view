import plotly
import plotly.graph_objs as go
import json

def createBoxPlot(df, x, y, plotType):

    if plotType == 'bar':
        data = [
            go.Bar(
                x=df['{}'.format(x)],
                y=df['{}'.format(y)],
                marker = dict(
                              color = '#4cb576'
                         )
            )]
    elif plotType == 'scatter':
        data = [go.Scatter(
                x=df['{}'.format(x)],
                y=df['{}'.format(y)],
                mode = 'lines+markers',
                marker = dict(
                              color = '#ff4444'
    )
    )]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
