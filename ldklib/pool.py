from multiprocessing.dummy import Pool as threading_pool

def pool(nums=10):
    pool = threading_pool(10)
    return pool.map
