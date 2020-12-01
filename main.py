import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s', )
logger = logging.getLogger(__name__)


def create_lineup_dictionary(raw_data) -> Dict[int, str]:
    '''
    Pull the lineup data and put it into an unformatted dictionary.
    :param raw_data: Extracts of HTML from fantasyfootballscout that contain the lineup information.
    :return: A dictionary of the format {0: [player1, player2... player11], ... 20: [...] }
    '''

    logger.info('---- Creating lineup dictionary (unformatted) ----')

    lineup_dictionary = {}
    key = 0

    for team in raw_data:
        lineup_dictionary[key] = team.text.split('  ')[1:]
        logger.info(f'Lineup {key}: {lineup_dictionary[key]}')
        assert len(lineup_dictionary[key]) == 11
        key += 1

    logger.info(f'Final unformatted lineups: {lineup_dictionary}')
    assert len(lineup_dictionary) == 20

    logger.info('---- Created lineup dictionary (unformatted) successfully ---- \n')
    return lineup_dictionary


def create_team_mapper(raw_data) -> Dict[int, str]:
    '''
    Create a dictionary which maps the unformatted lineup data to their respective team names.
    :param raw_data: Extracts of HTML from fantasyfootballscout that contain the team names.
    :return: A dictionary of the format {0: team1, 1: team2, ... 19: team20 }
    '''

    logger.info('---- Creating mapping function ----')

    team_map = {}
    for team in range(2, 22):
        team_map[team-2] = raw_data[team].text.split('Next')[0]
        logger.info(f'{team_map[team-2]} mapped to {team-2}')

    logger.info(f'Final mapping function: {team_map}')
    assert len(team_map) == 20

    logger.info('---- Created mapping function successfully ---- \n')
    return team_map


def create_final_dictionary(lineups_data: Dict[int, str], mapping_dictionary: Dict[int, str]) -> Dict[str, str]:
    '''
    This function uses the mapping dictionary to assign the team names to each predicted lineup.
    :param lineups_data: A dictionary with keys that match mapping_dictionary to obtain the respective team names.
    :param mapping_dictionary: A dictionary with keys that match the lineups_data to map team names to these values.
    :return: A dictionary of the format {team1: [player1, player2... player11], ... team20: [...] }
    '''

    logger.info('---- Creating final formatted lineup dictionary ----')

    formatted_dictionary = {}
    for key in range(0, 20):
        formatted_dictionary[mapping_dictionary[key]] = lineups_data[key]
        logger.info(f'Team: {mapping_dictionary[key]}')
        logger.info(f'Lineup: {formatted_dictionary[mapping_dictionary[key]]}')

    logger.info(f'Final formatted lineups {formatted_dictionary}')
    assert len(formatted_dictionary) == 20

    logger.info('---- Created final formatted lineup dictionary successfully ---- \n')
    return formatted_dictionary


def pull_fantasyfootballscout_lineups(url='https://www.fantasyfootballscout.co.uk/team-news/') -> Dict[str, str]:
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
    logger.info('---- Pulling lineup predictions from Fantasy Football Scout ---- \n')
    pull_fantasyfootballscout_lineups()
    logger.info('---- Lineup predictions successfully pulled from Fantasy Football Scout ---- \n')

