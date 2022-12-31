import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

import warnings

warnings.filterwarnings("ignore")
sns.set_style('whitegrid')
plt.style.use("seaborn-notebook")

##  MAIN PAGE  ##

st.markdown("# World Happiness Report 2021 - An Analysis")
st.image('download.jpg')
st.markdown("*Data source: Kaggle*")
st.write("Welcome to the World Happiness Report Dashboard for 2021!")
st.write(
  "The World Happiness Report is an annual publication that ranks 156 countries by their happiness levels. The report is based on the global happiness index, which is calculated using factors such as income, social support, healthy life expectancy, freedom to make life choices, trust, and generosity."
)

# Add a sidebar to the left of the page
st.sidebar.header('Choose:')


def transformer(Variable):

  pop = pd.read_csv('world-population-19602018/population_total_long.csv')
  df2021 = pd.read_csv('world-happiness-report-2021/world-happiness-report-2021.csv')
  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')
  
  country_continent = {}
  for i in range(len(df2021)):
      country_continent[df2021["Country name"][i]] = df2021["Regional indicator"][i]
  all_countries = df["Country name"].value_counts().reset_index()["index"].tolist()
  all_countries_2021 = df2021["Country name"].value_counts().reset_index()["index"].tolist()

  region = []
  for i in range(len(df)):
      if df['Country name'][i] == 'Angola':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'Belize':
          region.append("Latin America and Caribbean")
      elif df['Country name'][i] == 'Congo (Kinshasa)':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'Syria':
          region.append("Middle East and North Africa")
      elif df['Country name'][i] == 'Trinidad and Tobago':
          region.append("Latin America and Caribbean")
      elif df['Country name'][i] == 'Cuba':
          region.append("Latin America and Caribbean")
      elif df['Country name'][i] == 'Qatar':
          region.append("Middle East and North Africa")
      elif df['Country name'][i] == 'Sudan':
          region.append("Middle East and North Africa")
      elif df['Country name'][i] == 'Central African Republic':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'Djibouti':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'Somaliland region':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'South Sudan':
          region.append("Middle East and North Africa")
      elif df['Country name'][i] == 'Somalia':
          region.append("Sub-Saharan Africa")
      elif df['Country name'][i] == 'Oman':
          region.append("Middle East and North Africa")
      elif df['Country name'][i] == 'Guyana':
          region.append("Latin America and Caribbean")
      elif df['Country name'][i] == 'Guyana':
          region.append("Latin America and Caribbean")
      elif df['Country name'][i] == 'Bhutan':
          region.append("South Asia")
      elif df['Country name'][i] == 'Suriname':
          region.append("Latin America and Caribbean")
      else:
          region.append(country_continent[df['Country name'][i]])
          
  df["region"] = region

  all_countries = df["Country name"].value_counts().reset_index()["index"].tolist()
  all_countries_pop = pop["Country Name"].value_counts().reset_index()["index"].tolist()
  
  del_cou = []
  for x in all_countries:
      if x not in all_countries_pop:
          del_cou.append(x)

  pop_df = df[['Log GDP per capita', 'Life Ladder', 'Country name', 'year', 'Social support', 'Healthy life expectancy at birth',
         'Freedom to make life choices', 'Generosity',"region",'Perceptions of corruption']].copy()

  pop_df = pop_df[~pop_df["Country name"].isin(del_cou)]
  pop_df = pop_df[~pop_df.year.isin([2006,2005,2007,2018,2019,2020,2021])]
  pop_dict = {x:{} for x in range(2008,2018)}
  for i in range(len(pop)):
      if(pop["Year"][i] in range(2008,2018)):
          pop_dict[pop["Year"][i]][pop["Country Name"][i]] = pop["Count"][i]

  population = []
  for i in pop_df.index:
      population.append(pop_dict[pop_df["year"][i]][pop_df["Country name"][i]])
  pop_df["population"] = population

  if Variable == 'Corruption':
      fig = px.scatter(pop_df, 
                       x = "Perceptions of corruption",
                       y = "Life Ladder",
                       animation_frame = "year",
                       animation_group = "Country name",
                       size = "population",
                       color = "region", 
                       hover_name = "Country name", 
                       size_max = 60)
      fig.update_layout(title = "Life Ladder and Corruption Comparison by Countries via Regions for each Year")

      st.plotly_chart(fig)

  if Variable == 'Freedom':
      fig = px.scatter(pop_df, 
                       x = "Freedom to make life choices",
                       y = "Life Ladder",
                       animation_frame = "year",
                       animation_group = "Country name",
                       size = "population",
                       template = "plotly_dark",
                       color = "region", 
                       hover_name = "Country name", 
                       size_max = 60)
      fig.update_layout(title = "Life Ladder and Freedom Comparison by Countries via Regions for each Year")
    
      st.plotly_chart(fig)

  if Variable == 'Income':
      fig = px.scatter(pop_df, 
                       x = "Log GDP per capita",
                       y = "Life Ladder",
                       animation_frame = "year",
                       animation_group = "Country name",
                       size = "population",
                       template = "plotly_white",
                       color = "region", 
                       hover_name = "Country name", 
                       size_max = 60)
      fig.update_layout(title = "Life Ladder and Log GDP per capita Comparison by Countries via Regions for each Year")

      st.plotly_chart(fig)


# PAGE 1
if st.sidebar.button("REGIONAL COUNTPLOT"):

  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')

  # Regional countplot
  sns.catplot(x='Regional indicator', kind='count', data=df2021)
  plt.xticks(rotation=90)
  plt.title('Regional countplot')

  # Display the chart in the main content area of the page
  st.pyplot()

# PAGE 2
if st.sidebar.button("FEATURE DISTRIBUTION - SET 1"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  list_features = [
    "Social support", "Freedom to make life choices", "Generosity",
    "Perceptions of corruption"
  ]
  sns.boxplot(data=df2021.loc[:, list_features],
              orient="v",
              palette="Set1",
              showmeans=True)
  plt.xticks(rotation=60)
  plt.title('Feature distribution')

  st.pyplot()

# PAGE 3
if st.sidebar.button("FEATURE DISTRIBUTION - SET 2"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  list_features = ["Ladder score", "Logged GDP per capita"]
  sns.boxplot(data=df2021.loc[:, list_features],
              orient="v",
              palette="Set1",
              showmeans=True)
  plt.title('Feature distribution')

  st.pyplot()

# PAGE 4
if st.sidebar.button("HEALTHY LIFE EXPECTANCY"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  list_features = ["Healthy life expectancy"]
  sns.boxplot(data=df2021.loc[:, list_features],
              orient="v",
              palette="Set1",
              showmeans=True)

  st.pyplot()

# PAGE 5
if st.sidebar.button("HAPPIEST AND UNHAPPIEST COUNTRIES IN 2021"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  df2021_happiest_unhappiest = df2021[(df2021.loc[:, "Ladder score"] > 7.0) |
                                      (df2021.loc[:, "Ladder score"] < 4.0)]
  sns.barplot(x="Ladder score",
              y="Country name",
              data=df2021_happiest_unhappiest,
              palette="coolwarm")
  plt.title("Happiest and Unhappiest Countries in 2021")

  st.pyplot()

# PAGE 6
if st.sidebar.button("LADDER SCORE DISTRIBUTION BY REGIONAL INDICATOR"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  plt.figure(figsize=(15, 8))
  sns.kdeplot(x=df2021["Ladder score"],
              fill=True,
              linewidth=2,
              hue=df2021["Regional indicator"])
  plt.axvline(df2021["Ladder score"].mean(), c="black")
  plt.title("Ladder Score Distribution by Regional Indicator")
  plt.legend(df2021['Regional indicator'].unique())

  st.pyplot()

# PAGE 7
if st.sidebar.button("FREEDOM COMPARISON BY COUNTRIES"):
  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')

  fig = px.choropleth(df.sort_values("year"),
                      locations="Country name",
                      color="Freedom to make life choices",
                      locationmode="country names",
                      animation_frame="year")
  fig.update_layout(title="Freedom Comparison by Countries")

  st.plotly_chart(fig)

# PAGE 8
if st.sidebar.button("LIFE LADDER COMPARISON"):
  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')

  fig = px.choropleth(df.sort_values("year"),
                      locations="Country name",
                      color="Life Ladder",
                      locationmode="country names",
                      animation_frame="year")
  fig.update_layout(title="Life Ladder Comparison by Countries")

  st.plotly_chart(fig)

# PAGE 9
if st.sidebar.button("MOST GENEROUS AND UNGENEROUS COUNTRIES"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')
  df2021_g = df2021[(df2021.loc[:, "Generosity"] > 0.3) |
                    (df2021.loc[:, "Generosity"] < -0.2)]
  sns.barplot(x="Generosity", y="Country name", data=df2021_g, palette="dark")
  plt.title("Most Generous and Most Ungenerous Countries in 2021")

  st.pyplot()

  fig = px.choropleth(df.sort_values("year"),
                      locations="Country name",
                      color="Generosity",
                      locationmode="country names",
                      animation_frame="year")
  fig.update_layout(title="Generosity Comparison by Countries")

  st.plotly_chart(fig)

# PAGE 10
if st.sidebar.button("GENEROSITY DISTRIBUTION BY REGION"):
  df2021 = pd.read_csv(
    'world-happiness-report-2021/world-happiness-report-2021.csv')
  plt.figure(figsize=(10, 13))
  sns.swarmplot(x="Regional indicator", y="Generosity", data=df2021, hue="Regional indicator")
  plt.xticks(rotation=60)
  plt.title("Generosity Distribution by Region.")

  st.pyplot()

# PAGE 11
if st.sidebar.button("RELATIONSHIP BETWEEN INCOME AND HAPPINESS"):
  transformer('Income')

if st.sidebar.button("RELATIONSHIP BETWEEN HAPPINESS AND CORRUPTION"):
  transformer("Corruption")

if st.sidebar.button("RELATIONSHIP BETWEEN HAPPINESS AND FREEDOM"):
  transformer("Freedom")
  
# PAGE 12
if st.sidebar.button("RELATIONSHIP BETWEEN FEATURES"):
  df = pd.read_csv('world-happiness-report-2021/world-happiness-report.csv')
  sns.heatmap(df.corr(), annot = True, fmt = ".2f", linewidth = .7)
  plt.title("Relationship Between Features ")

  st.pyplot()

  sns.clustermap(df.corr(), center = 0, cmap = "vlag", dendrogram_ratio = (0.1, 0.2), annot = True, linewidths = .7, figsize=(10,10))

  st.pyplot()

# FINAL PAGE
if st.sidebar.button("CONCLUSION"):
  st.write(
    "From the exploratory data analysis conducted, we can conclude that the life ladder has a positive correlation with general income, social support, healthy life expectancy and freedom to make life choices."
  )
  st.write(
    "Furthermore, we found that perceptions of corruption was negatively correlated with the life ladder.")