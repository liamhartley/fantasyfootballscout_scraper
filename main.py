import re
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s', )
logger = logging.getLogger(__name__)


def pull_fantasyfootballscout_lineups(url):
    lineup_dictionary = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    raw_data = soup.find_all("div", {"class": re.compile('formation.*')})

    team_id = 0
    for team in raw_data:
        lineup_dictionary[team_id] = decode_data(team.text)
        # for team_name in epl_teams:
        #     lineup_dictionary[team_name] = (team.text).split()
        team_id += 1

    # fantasy_football_lineup_mapping = fatasy_football_lineup_mapper()
    # for team_numeric in range(0, 20):
    #     lineup_dictionary[fantasy_football_lineup_mapping[team_numeric]] = lineup_dictionary[team_numeric]
    #     del lineup_dictionary[team_numeric]

    return lineup_dictionary


def decode_data(match):
    """Returns data in the match's first group decoded to JSON."""
    trans_data = match.split()
    return trans_data

#######

def predict_lineups():
    logger.info('############# Pulling lineup predictions from Fantasy Football Scout #############')

    url = 'https://www.fantasyfootballscout.co.uk/team-news/'
    lineup_data = pull_fantasyfootballscout_lineups(url)

    # predicted_lineups_id = epl_teams_fantasyfootballscout()
    # lineup_dictionary = lineup_database()
    #
    # # TODO make this into its own function which outputs predited_lineups_id
    # # For every team
    # for team in predicted_lineups_id.keys():
    #     lineup = lineup_data[team]
    #     previous_player = ''
    #     # For every player in that team
    #     for player_id in lineup:
    #         player = str(player_id)
    #         if f'{team}_{player}' in lineup_dictionary:
    #             predicted_lineups_id[team].append(lineup_dictionary[f'{team}_{player}'])
    #         elif f'{team}_{previous_player} {player}' in lineup_dictionary:
    #             predicted_lineups_id[team].append(lineup_dictionary[f'{team}_{previous_player} {player}'])
    #         else:
    #             previous_player = player
    #
    # # # Add team names to the dictionary
    # # team_names = epl_teams_list()
    # # for team in range(0, 20):
    # #     replace_names = predicted_lineups_id[team]
    # #     predicted_lineups_id[team_names[team]] = replace_names
    # # for team in range(0, 20):
    # #     del predicted_lineups_id[team]
    #
    # # Check all players were pulled
    # for team in predicted_lineups_id:
    #     if len(predicted_lineups_id[team]) <= 10:
    #         logger.warning(f'Team: {team} only has {len(predicted_lineups_id[team])} players.')
    #         logger.warning(f'Please edit the lineup_database to amend this.')
    #
    # logger.info(f'Predicted lineups id returned: {predicted_lineups_id}')
    #
    # predicted_lineups = {}
    # inverse_lineups = inverse_lineup_database()
    # for team in predicted_lineups_id.keys():
    #     logger.info(f'Team: {team}')
    #     player_list = []
    #     for player in predicted_lineups_id[team]:
    #         if player in predicted_lineups_id[team]:
    #             player_list.append(inverse_lineups[player])
    #         else:
    #             raise ValueError('Missing player from inverse database!')
    #     predicted_lineups[team] = player_list
    #     logger.info(f'Players: {player_list}')
    #
    # return predicted_lineups_id


if __name__ == '__main__':
    predict_lineups()

# def fatasy_football_lineup_mapper():
#     teams = {0: 'Arsenal',
#              1: 'Aston Villa',
#              2: 'Brighton',
#              3: 'Burnley',
#              4: 'Chelsea',
#              5: 'Crystal Palace',
#              6: 'Everton',
#              7: 'Fulham',
#              8: 'Leeds United',
#              9: 'Leicester City',
#              10: 'Liverpool',
#              11: 'Manchester City',
#              12: 'Manchester United',
#              13: 'Newcastle United',
#              14: 'Sheffield United',
#              15: 'Southampton',
#              16: 'Tottenham Hotspur',
#              17: 'West Bromwich Albion',
#              18: 'West Ham',
#              19: 'Wolverhampton'}
#     return teams
#