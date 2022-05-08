from glob import glob
import re
import pygame as pg
import multiprocessing as mp
import time
import numpy as np

def my_function(i,param1,param2,param3):
    result = param1 **2 * param2 + param3
    time.sleep(2)
    return (i,result)


def get_result(result):
    global results
    results.append(result)


if __name__ == "__main__":
    params = np.random.random((10,3))*100
    results = []
    print('Number of cpus available: ',mp.cpu_count())
    ts = time.time()
    pool = mp.Pool(mp.cpu_count())
    for i in range(0,params.shape[0]):
        #get_result(my_function(i,params[i,0],params[i,1],params[i,2]))
        pool.apply_async(my_function,args=(i,params[i,0],params[i,1],params[i,2]),callback=get_result)

    pool.close()
    pool.join()
    #print('Time in serial: ',time.time()-ts)
    print('Time in parallel',time.time()-ts)
    print(results)
        




