!pip install yfinance;
!pip install datapane;
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

import plotly.figure_factory as ff
import datapane as dp
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import pandas_datareader.data as web
import datetime


import plotly.io as pio
pio.templates.default = "plotly_dark"
tickers = yf.Tickers('nflx msft AAPL goog GME')


nflx = tickers.tickers.NFLX.history(period="1y")
aapl = tickers.tickers.AAPL.history(period="1y")
gme = tickers.tickers.GME.history(period="1y")

nflx ['10-day MA'] =  nflx.iloc[:,3].rolling(window=10).mean()
nflx ['20-day MA'] =  nflx.iloc[:,3].rolling(window=20).mean()
nflx ['50-day MA'] =  nflx.iloc[:,3].rolling(window=50).mean()

trace0 = go.Scatter(x=nflx.index, y=nflx["Close"], name='nflx')
fig0 = go.Figure([trace0])
fig0.update_layout(
    title={
        'text': "Netflix Stock Price",
        'x':0.5,
        'xanchor': 'center'})

trace0 = go.Scatter(x=nflx.index, y=nflx.Close, name='NFLX')
trace1 = go.Scatter(x=nflx.index, y=nflx['10-day MA'], name='10-day MA')
trace2 = go.Scatter(x=nflx.index, y=nflx['20-day MA'], name='20-day MA')
fig1 = go.Figure([trace0, trace1, trace2])
fig1.update_layout(
    title={
        'text': "Netflix Stock Price",
        'x':0.5,
        'xanchor': 'center'})
        
fig2 = go.Figure(go.Candlestick(x=nflx.index, open=nflx["Open"], high=nflx["High"], low=nflx["Low"], close=nflx["Close"]))
fig2.update_layout(
    title={
        'text': "Netflix Stock Price (Candle Stick)",
        'x':0.5,
        'xanchor': 'center'})
fig2.show()

nflx['Daily return (%)'] = round(nflx['Close'].pct_change()*100, 2)

fig3 = px.bar(nflx, x=nflx.index, y="Daily return (%)")
fig3.update_layout(
    title={
        'text': "Netflix Stock Daily Return",
        'x':0.5,
        'xanchor': 'center'})
fig3.show()

trace1 = go.Scatter(x=aapl.index, y=aapl["Close"], name='AAPL', line=dict(color='red'))

fig4 = go.Figure([trace0, trace1])
fig4.update_layout(dict(
    title=dict({
        'text': "Netflix vs Apple Stock Price",
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
fig4.show()

trace0 = go.Scatterpolar(
      r = [nflx['Close'].mean(),nflx['Open'].min(), nflx['Low'].min(),nflx['High'].max()],
      theta = ['Close','Open','Low','High'], line =  dict(
            color = 'lime'), name='NFLX',
      fill = 'toself')

trace1 = go.Scatterpolar(
      r = [aapl['Close'].mean(),aapl['Open'].min(), aapl['Low'].min(),aapl['High'].max()],
      theta = ['Close','Open','Low','High'], line =  dict(
            color = 'red'), name='AAPL',
      fill = 'toself'
    )

fig5 = go.Figure([trace0,trace1])
fig5.update_layout(go.Layout(
      polar = dict(
        radialaxis = dict(
          visible = True)),
            title=dict({
        'text': "Netflix vs Apple Stock Price (Radar Chart)",
        'x':0.5,
        'xanchor': 'center'})))


end = datetime.datetime.now()
start = datetime.datetime(end.year-1,end.month,end.day)
df = web.DataReader(['NFLX', 'FB', 'AAPL', 'GME'], 'yahoo', start, end)['Close']

trace0 = go.Box(y=df.FB, name='FB', line=dict(color='blue'))
trace1 = go.Box(y=df.NFLX, name='NFLX', line=dict(color='red'))
trace2 = go.Box(y=df.AAPL, name='AAPL', line=dict(color='silver'))
trace3 = go.Box(y=df.GME, name='GME', line=dict(color='purple'))

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

