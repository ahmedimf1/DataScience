import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import datapane as dp
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import pandas_datareader.data as web
import datetime

# py.init_notebook_mode(connected=True)

import plotly.io as pio
pio.templates.default = "plotly_dark"

start = datetime.datetime(2019, 8, 1)
end = datetime.datetime.now()

zm = web.DataReader("ZM", 'yahoo', start, end).reset_index()
nflx = web.DataReader("NFLX", 'yahoo', start, end).reset_index()



trace0 = go.Scatter(x=nflx.Date, y=nflx.Close, name='nflx')
fig0 = go.Figure([trace0])
fig0.update_layout(
    title={
        'text': "Netflix Stock Price",
        'x':0.5,
        'xanchor': 'center'})



nflx['10-day MA'] = nflx['Close'].rolling(window=10).mean()
nflx['20-day MA'] = nflx['Close'].rolling(window=20).mean()
nflx['50-day MA'] = nflx['Close'].rolling(window=50).mean()

trace0 = go.Scatter(x=nflx.Date, y=nflx.Close, name='NFLX')
trace1 = go.Scatter(x=nflx.Date, y=nflx['10-day MA'], name='10-day MA')
trace2 = go.Scatter(x=nflx.Date, y=nflx['20-day MA'], name='20-day MA')
fig1 = go.Figure([trace0, trace1, trace2])
fig1.update_layout(
    title={
        'text': "Netflix Stock Price",
        'x':0.5,
        'xanchor': 'center'})


fig2 = go.Figure(go.Candlestick(x=nflx.Date, open=nflx.Open, high=nflx.High, low=nflx.Low, close=nflx.Close))
fig2.update_layout(
    title={
        'text': "Netflix Stock Price (Candle Stick)",
        'x':0.5,
        'xanchor': 'center'})



nflx['Daily return (%)'] = round(nflx['Close'].pct_change()*100, 2)

fig3 = px.bar(nflx, x="Date", y="Daily return (%)")
fig3.update_layout(
    title={
        'text': "Netflix Stock Daily Return",
        'x':0.5,
        'xanchor': 'center'})


trace0 = go.Scatter(x=nflx.Date, y=nflx.Close, name='NFLX', line=dict(color='lime'))
trace1 = go.Scatter(x=zm.Date, y=zm.Close, name='ZM', line=dict(color='red'))

fig4 = go.Figure([trace0, trace1])
fig4.update_layout(dict(
    title=dict({
        'text': "Netflix vs Zoom Stock Price",
        'x':0.5,
        'xanchor': 'center'}),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=3,
                     label='3m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=12,
                     label='12m',
                     step='month',
                     stepmode='backward')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date')))


trace0 = go.Scatterpolar(
      r = [nflx['Close'].mean(),nflx['Open'].min(), nflx['Low'].min(),nflx['High'].max()],
      theta = ['Close','Open','Low','High'], line =  dict(
            color = 'lime'), name='NFLX',
      fill = 'toself')

trace1 = go.Scatterpolar(
      r = [zm['Close'].mean(),zm['Open'].min(), zm['Low'].min(),zm['High'].max()],
      theta = ['Close','Open','Low','High'], line =  dict(
            color = 'red'), name='ZM',
      fill = 'toself'
    )

fig5 = go.Figure([trace0,trace1])
fig5.update_layout(go.Layout(
      polar = dict(
        radialaxis = dict(
          visible = True)),
            title=dict({
        'text': "Netflix vs Zoom Stock Price (Radar Chart)",
        'x':0.5,
        'xanchor': 'center'})))


df = web.DataReader(['BABA', 'FB', 'AAPL', 'SPOT'], 'yahoo', start, end)['Close']

trace0 = go.Box(y=df.BABA, name='BABA', line=dict(color='blue'))
trace1 = go.Box(y=df.FB, name='FB', line=dict(color='red'))
trace2 = go.Box(y=df.AAPL, name='AAPL', line=dict(color='green'))
trace3 = go.Box(y=df.SPOT, name='SPOT', line=dict(color='purple'))

fig6 = go.Figure([trace0, trace1, trace2, trace3])
fig6.update_layout(
    title={
        'text': "Stock Prices",
        'x':0.5,
        'xanchor': 'center'})


fig7 = px.area(df, facet_col="Symbols", facet_col_wrap=2)
fig7.update_layout(
    title={
        'text': "Stock Prices",
        'x':0.5,
        'xanchor': 'center'})



nflx = nflx[['Open','Close','Volume']]
nflx["index"] = np.arange(len(nflx))

fig8 = go.Figure(ff.create_scatterplotmatrix(nflx, diag='box', index='index',size=3,
                               height=600, width=1150, colormap='RdBu',
                                   title={
                                    'text': "Netflix Stock Price (Scatterplot Matrix)",
                                    'x':0.5,
                                    'xanchor': 'center'}))

dp.Report(
    dp.Group(
        dp.Plot(fig0), 
        dp.Plot(fig1), 
        dp.Plot(fig2), 
        dp.Plot(fig3), 
        dp.Plot(fig4), 
        dp.Plot(fig5), 
        dp.Plot(fig6), 
        dp.Plot(fig7), 
        columns=2,
        rows=4
    ), dp.Plot(fig8)
).publish(name='stock_report', open=True)
