from itertools import repeat
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
pd.set_option('mode.chained_assignment', None)
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import mplcursors



# Loading and cleaning data
data = pd.read_csv('/Users/davidevaracalli/Downloads/dataset - PL.csv').dropna(subset=['Nationality', 'Age', 'Jersey Number'])
data[['Cross accuracy %', 'Shooting accuracy %', 'Tackle success %']] = data[['Cross accuracy %', 'Shooting accuracy %', 'Tackle success %']].replace('%', '', regex=True).astype(float)

# Filtering for players with at least 38 appearances
data_38app = data[data['Appearances'] >= 38]
positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
gk_38app, defenders_38app, midfielders_38app, forwards_38app = [data_38app[data_38app['Position'] == pos] for pos in positions]

# Per-game statistics
data_clean_appNonZero = data[data['Appearances'] > 0]
features_to_scale = data.columns.difference(['Age', 'Name', 'Appearances', 'Club', 'Nationality', 'Jersey Number', 'Cross accuracy %', 'Position', 'Goals per match', 'Passes per match', 'Tackle success %', 'Shooting accuracy %'])
data_clean_per_game = data_clean_appNonZero.copy()
data_clean_per_game[features_to_scale] = data_clean_per_game[features_to_scale].div(data_clean_per_game['Appearances'], axis=0)

# Filtering for positions with at least 38 appearances
all_players = data_clean_per_game[data_clean_per_game['Appearances'] >= 38]
gk_, defenders_, midfielders_, forwards_ = [all_players[all_players['Position'] == pos] for pos in positions]

# Top 5 nationalities by appearances and wins
for metric, colors, title in [('Appearances', ['#3BB143', '#D1E7DD', '#A3D5D1', '#4A9B8E', '#2C5F2D'], 'Top 5 Nationalities by Appearances'),
                              ('Wins', ['#007BFF', '#66B3FF', '#99CCFF', '#007BFF', '#0056b3'], 'Top 5 Nationalities by Wins')]:
    top_5_nationalities = data.groupby('Nationality')[metric].sum().nlargest(5).reset_index()
    plt.figure(figsize=(12, 8))
    plt.pie(top_5_nationalities[metric], labels=top_5_nationalities['Nationality'], autopct='%1.1f%%', colors=colors, wedgeprops={'edgecolor': 'white'})
    plt.title(title)
    plt.show()

# KDE plot of age
plt.figure(figsize=(12, 8))
sns.kdeplot(data=data['Age'], fill=True)
plt.title('KDE Plot of Age')
plt.show()

# BBoxplot of age by club with general average line
plt.figure(figsize=(12, 8))
sns.boxplot(x='Age', y='Club', data=data, color='coral')
plt.axvline(data['Age'].mean(), color='blue', linestyle='--', label=f'Media generale: {data["Age"].mean():.2f}')
plt.legend()
plt.subplots_adjust(left=0.2)
plt.gca().yaxis.set_tick_params(pad=5)
plt.title("Players Age Distribution by Club (avg. age dotted line)")
plt.xlabel("Age")
plt.ylabel("Club")
plt.show()

# GCharts for top 15 players by wins and losses
for metric, title, label, palette in [('Wins', 'Top 15 Players by Wins', 'Total Wins', sns.color_palette("coolwarm", 2)[0]),
                                      ('Losses', 'Top 15 Players by Losses', 'Total Losses', sns.color_palette("coolwarm", 2)[1])]:
    top_players = data.nlargest(15, metric)[['Name', metric]]
    plt.figure(figsize=(12, 8))
    sns.barplot(x=metric, y='Name', data=top_players, color=palette)
    plt.title(title)
    plt.xlabel(label)
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'{sel.target[0]:.0f}'))
    plt.show()

# Win and loss percentages per appearances
data_38app['perc_wins_apparences'] = data_38app['Wins'] / data_38app['Appearances']
data_38app['perc_losses_apparences'] = data_38app['Losses'] / data_38app['Appearances']

for metric, title, palette in [('perc_wins_apparences', 'Top 15 Players by Percentage of Wins', sns.color_palette("coolwarm", 2)[0]),
                               ('perc_losses_apparences', 'Top 15 Players by Percentage of Losses', sns.color_palette("coolwarm", 2)[1])]:
    top_players_perc = data_38app.nlargest(15, metric)[['Name', metric]]
    plt.figure(figsize=(12, 8))
    sns.barplot(x=metric, y='Name', data=top_players_perc, color=palette)
    plt.title(title)
    plt.xlabel(f'Percentage of {metric.split("_")[1].capitalize()}')
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'{sel.target[0]:.1%}' if 'wins' in metric else f'{sel.target[0]:.2%}'))
    plt.show()


# Function to create bar charts for a specific role
def create_stats_charts(data_overall, data_per_game, metrics, title):
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 16), facecolor='#F5F5F5')
    fig.subplots_adjust(hspace=0.8, wspace=0.7)  # Spaziatura tra i subplots
    fig.suptitle(title, fontsize=22, color='#333333', fontweight='bold')

    for i, (metric, color) in enumerate(metrics):
        # "Overall" chart
        axes[i, 0].barh(data_overall.sort_values(by=metric, ascending=False).head(5)["Name"], 
                        data_overall.sort_values(by=metric, ascending=False).head(5)[metric], 
                        color=color, edgecolor='black', alpha=0.7)
        axes[i, 0].set_title(f'{metric} (Overall)', fontsize=12, color='#333333')
        axes[i, 0].tick_params(axis='y', labelsize=12, color='#333333')
        axes[i, 0].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5, alpha=0.7)

        # "Per game" chart
        axes[i, 1].barh(data_per_game.sort_values(by=metric, ascending=False).head(5)["Name"], 
                        data_per_game.sort_values(by=metric, ascending=False).head(5)[metric], 
                        color=color, edgecolor='black', alpha=0.7)
        axes[i, 1].set_title(f'{metric} (Per Game)', fontsize=12, color='#333333')
        axes[i, 1].tick_params(axis='y', labelsize=12, color='#333333')
        axes[i, 1].grid(True, which='both', axis='x', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.subplots_adjust(left=0.15)  # Valore tra 0 e 1, maggiore aumenta lo spazio a sinistra
        plt.gca().yaxis.set_tick_params(pad=10)

    return fig

# Section 1: Goalkeeper Stats
gk_metrics = [
    ('Clean sheets', '#4682B4'),       # Steel
    ('Saves', '#FF7F50'),              # Coral
    ('High Claims', '#FFA07A'),        # Light Salmon
    ('Catches', '#9370DB'),            # Medium Purple
    ('Penalties saved', '#A9A9A9')     # Dark Gray
]

fig_gk = create_stats_charts(gk_38app, gk_, gk_metrics, 'Top Goalkeepers Stats Comparison: Overall Metrics vs Per Game')

# Section 2: Defender Stats
def_metrics_overall = [
    ('Blocked shots', '#FFA07A'),      # Light Salmon
    ('Interceptions', '#FF7F50'),      # Coral
    ('Clearances', '#4682B4'),         # Steel
    ('Headed Clearance', '#9370DB'),   # Medium Purple
    ('Clearances off line', '#A9A9A9') # Dark Gray
]

def_metrics_overall2 = [
    ('Last man tackles', '#D2691E'),   # Chocolate Brown
    ('Recoveries', '#CD5C5C'),         # Indian Red
    ('Duels won', '#2F4F4F'),          # Dark Slate Gray
    ('Successful 50/50s', '#8A2BE2'),  # Blue Violet
    ('Aerial battles won', '#778899')  # Light Slate Gray
]

fig_def_overall = create_stats_charts(defenders_38app, defenders_, def_metrics_overall, 'Top Defenders Stats Comparison: Overall Metrics vs Per Game')
fig_def_overall2 = create_stats_charts(defenders_38app, defenders_, def_metrics_overall2, 'Top Defenders Stats Comparison: Overall Metrics vs Per Game')

# Section 3: Defensive Midfielder Stats
mid_def_metrics_overall = [
    ('Blocked shots', '#FFA07A'),      # Light Salmon
    ('Interceptions', '#FF7F50'),      # Coral
    ('Tackle success %', '#4682B4'),   # Steel
    ('Headed Clearance', '#9370DB'),   # Medium Purple
    ('Recoveries', '#A9A9A9')          # Dark Gray
]

mid_def_metrics_overall2 = [
    ('Assists', '#DAA520'),            # Goldenrod
    ('Through balls', '#4682B4'),      # Steel
    ('Accurate long balls', '#9370DB'),# Medium Purple
    ('Duels won', '#B0C4DE'),          # Light Steel Blue
    ('Aerial battles won', '#2F4F4F')  # Dark Slate Gray
]

fig_mid_def_overall = create_stats_charts(midfielders_38app, midfielders_, mid_def_metrics_overall, 'Top Defensive Midfielders Stats Comparison: Overall Metrics vs Per Game')
fig_mid_def_overall2 = create_stats_charts(midfielders_38app, midfielders_, mid_def_metrics_overall2, 'Top Defensive Midfielders Stats Comparison: Overall Metrics vs Per Game')

# Section 4: Creative Midfielder Stats
mid_creative_metrics_overall = [
    ('Goals', '#4682B4'),              # Steel
    ('Headed goals', '#FF7F50'),       # Coral
    ('Penalties scored', '#FFA07A'),   # Light Salmon
    ('Freekicks scored', '#9370DB'),   # Medium Purple
    ('Shooting accuracy %', '#A9A9A9') # Dark Gray
]

mid_creative_metrics_overall2 = [
    ('Assists', '#DAA520'),            # Goldenrod
    ('Successful 50/50s', '#4682B4'),  # Steel
    ('Big chances created', '#8B008B'),# Dark Violet
    ('Cross accuracy %', '#6A5ACD'),   # Slate Blue
    ('Through balls', '#708090')       # Slate Gray
]

fig_mid_creative_overall = create_stats_charts(midfielders_38app, midfielders_, mid_creative_metrics_overall, 'Top Creative Midfielders Stats Comparison: Overall Metrics vs Per Game')
fig_mid_creative_overall2 = create_stats_charts(midfielders_38app, midfielders_, mid_creative_metrics_overall2, 'Top Creative Midfielders Stats Comparison: Overall Metrics vs Per Game')

# Section 5: Forward Stats
forward_metrics_overall = [
    ('Goals', '#4682B4'),              # Steel
    ('Headed goals', '#8B4513'),       # Saddle Brown
    ('Penalties scored', '#B8860B'),   # Dark Goldenrod
    ('Freekicks scored', '#2F4F4F'),   # Dark Slate Gray
    ('Shooting accuracy %', '#708090') # Slate Gray
]

forward_metrics_overall2 = [
    ('Assists', '#A0522D'),            # Sienna
    ('Big chances created', '#7B68EE'),# Medium Slate Blue
    ('Crosses', '#778899'),            # Light Slate Gray
    ('Goals with right foot', '#D2691E'), # Chocolate
    ('Goals with left foot', '#4169E1')   # Royal Blue
]

fig_forward_overall = create_stats_charts(forwards_38app, forwards_, forward_metrics_overall, 'Top Forwards Stats Comparison: Overall Metrics vs Per Game')
fig_forward_overall2 = create_stats_charts(forwards_38app, forwards_, forward_metrics_overall2, 'Top Forwards Stats Comparison: Overall Metrics vs Per Game')

# Enable hover cursor
mplcursors.cursor(hover=True)




############## GK WORST STATS SECTION #############
# Section 1: Worst Stats for Goalkeepers
gk_worst_metrics_overall = [
    ('Losses', '#FFA07A'),          # Light Salmon
    ('Clean sheets', '#FF7F50'),    # Coral
    ('Goals conceded', '#4682B4'),  # Steel
    ('Own goals', '#9370DB'),       # Medium Purple
    ('Red cards', '#FF0000')        # Red
]

fig_gk_overall = create_stats_charts(gk_38app, gk_, gk_worst_metrics_overall, 'Worst Goalkeeper Stats Comparison: Overall Metrics vs Per Game')
mplcursors.cursor(hover=True)  # Enable interactive cursor



############## DEF WORST STATS SECTION #############
# Section 2: Worst Stats for Defenders
def_worst_metrics_overall = [
    ('Losses', '#FF8C69'),           # Lighter Salmon Variant
    ('Own goals', '#FF6347'),        # Tomato Red
    ('Goals conceded', '#4169E1'),   # Royal Blue
    ('Duels lost', '#8A2BE2'),       # Blue Violet
    ('Aerial battles lost', '#696969') # Gray
]

def_worst_metrics_overall2 = [
    ('Errors leading to goal', '#8A2BE2'), # Blue Violet
    ('Yellow cards', '#FFD700'),           # Gold for yellow cards
    ('Red cards', '#FF0000'),              # Red 
    ('Fouls', '#A9A9A9'),                  # Dark Gray
    ('Tackle success %', '#32CD32')        # Lime Green
]

fig_def_overall = create_stats_charts(defenders_38app, defenders_, def_worst_metrics_overall, 'Worst Defender Stats Comparison: Overall Metrics vs Per Game')
fig_def_overall2 = create_stats_charts(defenders_38app, defenders_, def_worst_metrics_overall2, 'Worst Defender Stats Comparison: Overall Metrics vs Per Game')
mplcursors.cursor(hover=True)  # Enable interactive cursor



############## DEF MIDFIELDER WORST STATS SECTION #############
# Section 3: Worst Stats for Defensive Midfielders
def_mid__worst_metrics_overall = [
    ('Losses', '#FF8C69'),           # Light Salmon Variant
    ('Recoveries', '#4169E1'),       # Royal Blue
    ('Duels lost', '#9370DB'),       # Medium Purple
    ('Aerial battles lost', '#696969'), # Dark Gray
    ('Interceptions', '#FF4500')     # Orange Red
]

def_mid_worst_metrics_overall2 = [
    ('Errors leading to goal', '#8A2BE2'), 
    ('Yellow cards', '#FFD700'),  
    ('Red cards', '#FF0000'),        
    ('Fouls', '#A9A9A9'),
    ('Tackle success %', '#32CD32')
]

fig_def_mid_overall = create_stats_charts(midfielders_38app, midfielders_, def_mid__worst_metrics_overall, 'Worst Defensive Midfielders Stats Comparison: Overall Metrics vs Per Game')
fig_def_mid_overall2 = create_stats_charts(midfielders_38app, midfielders_, def_mid_worst_metrics_overall2, 'Worst Defensive Midfielders Stats Comparison: Overall Metrics vs Per Game')
mplcursors.cursor(hover=True)  # Enable interactive cursor



############## CREATIVE MIDFIELDER WORST STATS SECTION #############
# Section 4: Worst Stats for Creative Midfielders
creative_mid__worst_metrics_overall = [
    ('Losses', '#FF8C69'),          # Light Salmon Variant
    ('Big chances missed', '#4169E1'), 
    ('Offsides', '#9370DB'),
    ('Penalties scored', '#696969'), 
    ('Goals', '#4169E1')           # Coral
]    

fig_creative_mid_overall = create_stats_charts(midfielders_38app, midfielders_, creative_mid__worst_metrics_overall, 'Worst Creative Midfielders Stats Comparison: Overall Metrics vs Per Game')
mplcursors.cursor(hover=True)  # Enable interactive cursor



############## FORWARDS WORST STATS SECTION #############
# Section 5: Worst Stats for Forwards
forward__worst_metrics_overall = [
    ('Losses', '#FF8C69'),           # Lighter Salmon Variant
    ('Big chances missed', '#4682B4'),  
    ('Offsides', '#9370DB'),
    ('Penalties scored', '#A9A9A9'),
    ('Goals', '#4169E1')  # Warm and balanced Coral
]    

fig_forwards_overall = create_stats_charts(forwards_38app, forwards_, forward__worst_metrics_overall, 'Worst Forwards Stats Comparison: Overall Metrics vs Per Game')
mplcursors.cursor(hover=True)  # Enable interactive cursor

plt.show()
