import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#USERNAME_PASSWORD_PAIRS=[['guvi','guvi']]
app=dash.Dash(__name__)
#auth= dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server=app.server
df = pd.read_csv('https://raw.githubusercontent.com/srinathkr07/IPL-Data-Analysis/master/matches.csv')
df=df.drop(columns='id')
df=df.fillna(0)
mappings={'Rising Pune Supergiant':'Rising Pune Supergiants','Delhi Capitals':'Delhi Daredevils'}
df['team1']=df['team1'].replace(mappings)
df['team2']=df['team2'].replace(mappings)
df['winner']=df['winner'].replace(mappings)
df['toss_winner']=df['toss_winner'].replace(mappings)
#to create a new column 'Loser' 
loser=[]
for i in range(756):
  if (df.iloc[i,3])!=(df.iloc[i,9]):
    loser.append(df.iloc[i,3])
  elif (df.iloc[i,9])==0:
    loser.append(0)
  else:
    loser.append(df.iloc[i,4])
df['Loser']=loser
#to find the total matches played by each team over all the seasons
total={}
count=0
for i in df['team1'].unique():
  for m in range(756):
    if i==df.iloc[m,3]:
      count+=1
    else:
      if i==df.iloc[m,4]:
        count+=1
  total[i]=count
  count=0
#to create a new column of total matches played by the winner over all the seasons
match=[]
for i in df['winner']:
  for j,k in total.items():
    if i==j:
      match.append(k)
    elif i==0:
      match.append(0)
      break
df['Total_matches_played_by_winner']=match

app.layout=html.Div([html.Div([html.H1(children='IPL Data Analysis', style={'textAlign': 'center','color': 'darkblue', 'fontSize': 40,
'backgroundColor':'white'}),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br()],
style={'background-image':'url(https://styles.redditmedia.com/t5_2rnjo/styles/communityIcon_sn55eqgnhpw61.jpg?width=256&s=f3d9c42c8ab1f49848451012c87b276d6878b0e2)'}),
html.Br(),html.Div([dcc.Dropdown(['Best team based on Number of Wins',
                         'Best Player based on Player of the Match',
                         'Best team based on Win by Runs',
                         'Best Team based on Win by Wickets',
                         'Luckiest Venue for Each Team',
                         'Winning probability by Winning Toss'],'Best team based on Number of Wins',id='based-on',clearable=False,searchable=False,
                            style = dict(
                            width = '45%'                           
                            ))
  ]),html.Br(),
  html.Div([dcc.Dropdown(['All Seasons',2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,
                         2018,
                         2019],'All Seasons',id='year',clearable=False,searchable=False,
                            style = dict(width = '30%'))
  ]),html.Div([
  dcc.Graph(
       id='example-graph-1',
      )
  ])
])
@app.callback(
    Output('example-graph-1','figure'),
    [Input('based-on','value')],[Input('year','value')])
def update_graph(bvalue,yvalue):
  if bvalue== 'Best team based on Number of Wins':
    if yvalue=='All Seasons':
      pie=px.pie(data_frame=df,names='winner',title='Best team based on Number of Wins',hole=0.2,hover_data=['Total_matches_played_by_winner'])
      pie.update_traces(textinfo="label+value",textposition='inside')
      return pie
    else:
      df1 = df[df['season'] == yvalue]
      pie=px.pie(data_frame=df1,names='winner',title='Best team based on Number of Wins',hole=0.2)
      pie.update_traces(textinfo="label+value",textposition='inside')
      return pie

  elif bvalue== 'Best Player based on Player of the Match':
    if yvalue=='All Seasons':
      bar=px.bar(df,x='player_of_match',color='player_of_match',title='Best Player based on Player of the Match')
      bar.update_layout(xaxis={'categoryorder':'total descending'})
      return bar
    else:
      df1 = df[df['season'] == yvalue]
      bar=px.bar(df1,x='player_of_match',color='player_of_match',title='Best Player based on Player of the Match')
      bar.update_layout(xaxis={'categoryorder':'total descending'})
      return bar

  elif bvalue== 'Best team based on Win by Runs':
    if yvalue=='All Seasons':
      scat=px.scatter_3d(df,x='winner',y='Loser',z='win_by_runs',color='win_by_runs',size='win_by_runs',title='Best team based on Win by Runs')
      return scat
    else:  
      df1 = df[df['season'] == yvalue]
      scat=px.scatter_3d(df1,x='winner',y='Loser',z='win_by_runs',color='win_by_runs',size='win_by_runs',title='Best team based on Win by Runs')
      return scat

  elif bvalue== 'Best Team based on Win by Wickets':
    if yvalue=='All Seasons':
      df1=df.query("win_by_wickets>0")
      sun1= px.sunburst(df1, path=['winner', 'win_by_wickets'],title='Best Team based on Win by Wickets')
      sun1.update_layout(margin = dict(t=100, l=25, r=25, b=25))
      sun1.update_traces(textinfo="label+value",maxdepth=1)
      return sun1
    else:
      df1 = df[(df['season'] == yvalue) & (df["win_by_wickets"]>0)]
      sun1= px.sunburst(df1, path=['winner', 'win_by_wickets'],title='Best Team based on Win by Wickets')
      sun1.update_layout(margin = dict(t=100, l=25, r=25, b=25))
      sun1.update_traces(textinfo="label+value",maxdepth=1)
      return sun1

  elif bvalue== 'Luckiest Venue for Each Team':
    if yvalue=='All Seasons':
      fig=px.bar(df,x='venue',color='winner',title='Luckiest Venue for Each Team',animation_frame='winner',barmode='relative')
      fig.update_layout(margin=dict(l=100, r=20, t=100, b=200),paper_bgcolor="beige",title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
      fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
      fig['layout']['sliders'][0]['pad']=dict(r= 20, t= 200,)
      return fig
    else:
      df1 = df[df['season'] == yvalue]
      fig=px.bar(df1,x='venue',color='winner',title='Luckiest Venue for Each Team',animation_frame='winner',barmode='relative')
      fig.update_layout(margin=dict(l=100, r=20, t=100, b=200),paper_bgcolor="beige",title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
      fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
      fig['layout']['sliders'][0]['pad']=dict(r= 20, t= 200,)
      return fig

  elif bvalue== 'Winning probability by Winning Toss':
    if yvalue=='All Seasons':
      sun= px.sunburst(df, path=['toss_winner', 'winner'],title='Winning probability by Winning Toss')
      sun.update_layout(margin = dict(t=100, l=25, r=25, b=25))
      sun.update_traces(textinfo="label+percent parent+value")
      return sun
    else:
      df1 = df[df['season'] == yvalue]
      sun= px.sunburst(df1, path=['toss_winner', 'winner'],title='Winning probability by Winning Toss')
      sun.update_layout(margin = dict(t=100, l=25, r=25, b=25))
      sun.update_traces(textinfo="label+percent parent+value")
      return sun

if __name__ == '__main__':
   app.run_server(debug=True)
