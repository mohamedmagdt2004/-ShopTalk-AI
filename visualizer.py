import plotly.express as px

def create_chart(df, chart_type):

    x = df.columns[0]
    y = df.columns[1] if len(df.columns) > 1 else None

    if chart_type == "bar":
        return px.bar(df, x=x, y=y)

    elif chart_type == "line":
        return px.line(df, x=x, y=y)

    elif chart_type == "pie":
        return px.pie(df, names=x, values=y)

    elif chart_type == "scatter":
        return px.scatter(df, x=x, y=y)

    elif chart_type == "histogram":
        return px.histogram(df, x=x)

    return None  