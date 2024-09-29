import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np


players = ["Tyjae Spears","Gabe Davis","Curtis Samuel","Sam LaPorta"]

def get_single_week_stats(week_number:int, predicted:bool):
    file_path = ""
    if predicted:
        file_path = f"Predicted_Data\Week {week_number}"
    else:
        file_path = f"Week Stats\Week {week_number}"
     
    files_names = os.listdir(file_path)
    frames = []
    for file in files_names:
            full_path = "{}\{}".format(file_path,file)
            frame = pd.read_csv(full_path)
            frames.append(frame)
    all_players = pd.concat(frames,axis=0,ignore_index=True)
    if not predicted:
        all_players['Player'] = all_players['Player'].apply(lambda x: re.sub(r'\(\w+\)','',x) if not isinstance(x, float) else x)
        all_players['Player'] = all_players['Player'].apply(lambda x : str(x).strip())
        all_players[all_players['Player'].isna()].dropna(inplace=True)
        all_players = all_players.fillna(0)
    all_players.to_csv('test.csv')
    player_dataframe = all_players[all_players['Player'].isin(players)]
    print(player_dataframe)
    player_stats = {}
    stat_columns = player_dataframe.columns[1:]  
    
    for player in players:
        player_data = player_dataframe[player_dataframe['Player'] == player][stat_columns].values.flatten().tolist()
        if len(player_data) > 0:
            player_data += player_data[:1]  
            player_stats[player] = player_data

    num_vars = len(stat_columns)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for player, stats in player_stats.items():
        ax.fill(angles, stats, alpha=0.25, label=player)
        ax.plot(angles, stats, linewidth=2, label=player)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stat_columns)

    plt.title(f'Player Attribute Comparison Radar Plot - Week {week_number}', size=15, color='darkblue')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    if predicted:
        plt.savefig(f'Player Predicted Charts/Game Stats/Week {week_number} Player Report Prediction.png')
    else:
        plt.savefig(f'Player Performance Charts/Game Stats/Week {week_number} Player Report Stats Per Game.png')


def get_progress(week:int,attribute:str,predicted:bool):
    """
    `week` is the latest amount of progress you want
    `attribute` see the progress of the corresponding attributes : REC , YDS, TDS, ATT, FPTS
    all attributes : ATT   YDS  YBCON  YACON  BRKTKL  TK LOSS  TK LOSS YDS  10+ YDS  ...  40+ YDS  50+ YDS  REC  TGT  RZ TGT  YACON.1   YBC   AIR   YAC  CATCHABLE  DROP
    """
    file_path = ""
    player_dict = {name: [] for name in players}
    for i in range(1,week+1):
        if predicted:
            file_path = f"Predicted_Data/Week {i}"
        else:
            file_path = f"Week Stats/Week {i}"
        files_names = os.listdir(file_path)
        frames = []
        for file in files_names:
            full_path = "{}\{}".format(file_path,file)
            frame = pd.read_csv(full_path)
            frames.append(frame)
        all_players = pd.concat(frames,axis=0,ignore_index=True)
        if not predicted:
            all_players['Player'] = all_players['Player'].apply(lambda x: re.sub(r'\(\w+\)','',x) if not isinstance(x, float) else x)
            all_players['Player'] = all_players['Player'].apply(lambda x : str(x).strip())
            all_players[all_players['Player'].isna()].dropna(inplace=True)
            all_players = all_players.fillna(0)
        all_players_dataframe = all_players[all_players['Player'].isin(players)]
        for key in player_dict.keys():
            player = all_players_dataframe[all_players_dataframe['Player'] == key]
            player_dict[key].append(*player[attribute].values)
    weeks = [i for i in range(1,week+1)]

    plt.figure(figsize=(10, 6))

    for player, scores in player_dict.items():
        plt.plot(weeks, scores, marker='o', label=player)

    plt.xlabel('Week')
    plt.ylabel(f'{attribute} Score')
    plt.title(f'Player {attribute} Progress Over {week} Weeks')
    plt.legend()
    plt.grid(True)
    print(player_dict)
    if predicted:
        plt.savefig(f'Player Predicted Charts/Player Trends/{attribute} week {week} Predicted Play Progress.png')    
    else:
        plt.savefig(f'Player Performance Charts/Player Trends/{attribute} week {week} Player Progress.png')  
if __name__ == "__main__":
    get_single_week_stats(3,True)

