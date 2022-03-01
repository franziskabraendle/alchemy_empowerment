import empowermentexploration.utils.data_handle as dh
import pandas as pd

if __name__ == '__main__':
    game_version = "alchemy1"
    split_version = "data"
    vector_version = "crawl300"
    empowerment_info = pd.read_csv('empowermentexploration/resources/customgametree/data/{}EmpowermentTable-{}-{}.csv'.format(game_version, split_version, vector_version), dtype={'first': int, 'second': int, 'predResult': int, 'empComb': float, 'empChild': float, 'binComb': float, 'binChild': float})
