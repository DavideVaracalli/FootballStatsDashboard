# FootballStatsDashboard
In-depth Analysis of the Premier League Dataset: Player Statistics and Trends


# Description
[PLPerformanceAnalysis](https://github.com/DavideVaracalli/FootballStatsDashboard) is a project that uses Python to conduct in-depth analyses of Premier League players and clubs, based on a comprehensive dataset containing detailed information on each player. The primary objective of this project is to create visualizations and statistical analyses that help users better understand individual and team performances throughout the seasons.

# 1. Overview of the Premier League
The Premier League is the highest level of the English football league system, featuring 20 clubs that compete annually in a league with a promotion and relegation system involving the English Football League (EFL). Each season runs from August to May, with each team playing 38 matches (playing against the other 19 teams both home and away).

# 2. The Dataset
The dataset used [PLDataset](./PLDataset.csv) contains data up to September 24, 2020, with a total of 571 rows and 59 columns. Each row represents a player currently active in the Premier League, and the columns describe player attributes and game statistics. Here are some of the included details:

Name: The player's name
Jersey Number: The number on the back of their shirt
Club: The club the player is currently playing for
Position: The playing position (Goalkeeper, Defender, Midfielder, Forward)
Nationality: The player's country of origin
Age: The player's age
Appearances: The number of games played (including substitute appearances)
Wins: The number of games won
Losses: The number of games lost
Goals: The number of goals scored in the EPL
Goals per match: Average goals scored per game

# 3. Analysis Objectives
The analysis aims to explore and visualize key statistics, including:

The number of appearances, wins, and losses per player and club.
Individual performances through metrics like goals per match and win/loss percentages.
The age distribution of players and its implications for performance.
Comparisons among different positions (goalkeepers, defenders, midfielders, and forwards).

# 4. Methodology
The analyses involve data cleaning and transformation techniques, alongside graphical visualizations using Python libraries such as matplotlib and seaborn. To avoid distortions in the results, per-game statistics are calculated by dividing total values by the number of player appearances. Only players with at least 38 appearances (equivalent to a full season) are considered for meaningful comparisons to prevent players with few matches from appearing as top performers.

# 5. Key Insights and Findings
The analysis identifies the most influential players and clubs with the highest number of wins and losses. Additionally, the visualizations help to understand how age and position affect performance, offering insights into the characteristics of the top Premier League players.
