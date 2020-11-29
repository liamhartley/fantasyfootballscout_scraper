import re
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s', )
logger = logging.getLogger(__name__)


def create_lineup_dictionary(raw_data):
    '''

    :param raw_data:
    :return:
    '''

    lineup_dictionary = {}
    key = 0

    for team in raw_data:
        lineup_dictionary[key] = team.text.split('  ')[1:]
        assert len(lineup_dictionary[key]) == 11
        key += 1

    assert len(lineup_dictionary) == 20
    return lineup_dictionary


def create_team_mapper(raw_data):
    '''

    :param raw_data:
    :return:
    '''

    team_map = {}
    for team in range(2, 22):
        team_map[team-2] = raw_data[team].text.split('Next')[0]

    assert len(team_map) == 20
    return team_map


def create_final_dictionary(lineups_data, mapping_dictionary):
    '''
    This function uses the mapping dictionary to assign the team names to each predicted lineup.
    :param lineups_data:
    :param mapping_dictionary:
    :return:
    '''

    formatted_dictionary = {}
    for key in range(0, 20):
        formatted_dictionary[mapping_dictionary[key]] = lineups_data[key]

    assert len(formatted_dictionary) == 20

    return formatted_dictionary


def pull_fantasyfootballscout_lineups(url='https://www.fantasyfootballscout.co.uk/team-news/'):
    '''
    This function scrapes the latest predicted lineups from fantasyfootballscout.
    :param url: The url for where the predicted lineups are located.
    :return: A dictionary of the format {team1: [player1, player2... player11], ... team20: [...] }
    '''

    # Scrape the raw HTML and pass it into BeautifulSoup
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # Raw data related to the teams predicted lineup / formation
    lineups_raw = soup.find_all("div", {"class": re.compile('formation.*')})
    # Raw data which includes team names
    team_names_raw = soup.find_all('header')

    # Parse all of the raw data
    lineup_dictionary = create_lineup_dictionary(raw_data=lineups_raw)
    team_names_mapper = create_team_mapper(raw_data=team_names_raw)

    # Match the team lineups to their respective team names
    final_dictionary = create_final_dictionary(lineups_data=lineup_dictionary,
                                               mapping_dictionary=team_names_mapper)

    return final_dictionary


if __name__ == '__main__':
    logger.info('Pulling lineup predictions from Fantasy Football Scout')
    pull_fantasyfootballscout_lineups()


    # TODO split the functions out at the top to find indention error and add more docstrings