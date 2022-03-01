from empowermentexploration.resources.littlealchemy.empowerment import \
    Empowerment
from empowermentexploration.resources.littlealchemy.similarity import \
    Similarity
from empowermentexploration.resources.littlealchemy.gametrees import Gametrees
from empowermentexploration.resources.littlealchemy.tables import Tables
from empowermentexploration.resources.littlealchemy.vectors import Vectors

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: CHOOSE APPROPRIATE METHOD AND METHOD ARGUMENTS
    gametree = Gametrees()
    gametree.get_alchemy1_gametree()
    gametree.get_alchemy2_gametree()
    gametree.get_joined_gametree()
    gametree.get_tiny_gametree('alchemy')
    gametree.get_tiny_gametree('pixels')

    table = Tables()
    table.get_tables('combination','alchemy1', expand=True)
    table.get_tables('combination','alchemy2', expand=True)
    table.get_tables('combination','joined', expand=True)
    table.get_tables('combination','tinyalchemy', expand=True)
    table.get_tables('combination','tinypixels', expand=True)

    table.get_tables('parent','alchemy1')
    table.get_tables('parent','alchemy2')
    table.get_tables('parent','joined')
    table.get_tables('parent','tinyalchemy')
    table.get_tables('parent','tinypixels')

    table.get_tables('child','alchemy1')
    table.get_tables('child','alchemy2')
    table.get_tables('child','joined')
    table.get_tables('child','tinyalchemy')
    table.get_tables('child','tinypixels')

    vector = Vectors()
    vector.get_wordvectors('alchemy1', 'crawl', 300)
    vector.get_wordvectors('alchemy2', 'crawl', 300)
    vector.get_wordvectors('joined', 'crawl', 300)
    vector.get_wordvectors('tinyalchemy', 'crawl', 300)
    vector.get_wordvectors('tinypixels', 'crawl', 300)
    #vector.get_wordvectors('alchemy1', 'crawl', 100)
    #vector.get_wordvectors('alchemy2', 'crawl', 100)
    #vector.get_wordvectors('joined', 'crawl', 100)
    #vector.get_wordvectors('tinyalchemy', 'crawl', 100)
    #vector.get_wordvectors('tinypixels', 'crawl', 100)
    #vector.get_wordvectors('alchemy1', 'wiki', 300)
    #vector.get_wordvectors('alchemy2', 'wiki', 300)
    #vector.get_wordvectors('joined', 'wiki', 300)
    #vector.get_wordvectors('tinyalchemy', 'wiki', 300)
    #vector.get_wordvectors('tinypixels', 'wiki', 300)
    #vector.get_wordvectors('alchemy1', 'wiki', 100)
    #vector.get_wordvectors('alchemy2', 'wiki', 100)
    #vector.get_wordvectors('joined', 'wiki', 100)
    #vector.get_wordvectors('tinyalchemy', 'wiki', 100)
    #vector.get_wordvectors('tinypixels', 'wiki', 100)
    #vector.get_wordvectors('alchemy1', 'ccen', 300)
    #vector.get_wordvectors('alchemy2', 'ccen', 300)
    #vector.get_wordvectors('joined', 'ccen', 300)
    #vector.get_wordvectors('tinyalchemy', 'ccen', 300)
    #vector.get_wordvectors('tinypixels', 'ccen', 300)
    #vector.get_wordvectors('alchemy1', 'ccen', 100)
    #vector.get_wordvectors('alchemy2', 'ccen', 100)
    #vector.get_wordvectors('joined', 'ccen', 100)
    #vector.get_wordvectors('tinyalchemy', 'ccen', 100)
    #vector.get_wordvectors('tinypixels', 'ccen', 100)

    Similarity('alchemy1', 'crawl300')
    Similarity('alchemy2', 'crawl300')
    Similarity('tinyalchemy', 'crawl300')
    Similarity('tinypixels', 'crawl300')

    Empowerment('alchemy1', 'data', 'crawl300')
    Empowerment('alchemy2', 'data', 'crawl300')
    Empowerment('tinypixels', 'data', 'crawl300')
    Empowerment('tinyalchemy', 'data', 'crawl300')
    # YOUR ACTION IS NOT RECQUIRED ANYMORE
