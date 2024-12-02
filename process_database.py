import random
import numpy
import tqdm


def scale_points(points,N0,N1):
    maxN0 = 0 
    maxN1 = 0

    new_points = []

    for i,j in points:
        maxN0 = max(i,maxN0)
        maxN1 = max(j,maxN1)


    for i,j in points:
        new_i = int(max(1, i*N0/maxN0))
        new_j = int(max(1,j*N1/maxN1))
        new_points.append((new_i,new_j))
    return new_points



def make_database_from_points(points):
    newN0 = 0 
    newN1 = 0
    new_points = []

    map_to_original = {}
    for point in points:
        i,j = point
        search_token = random.randrange(10000000)
        while search_token in map_to_original:
            search_token = random.randrange(10000000)
        map_to_original[search_token] = (i,j)
        new_points.append(search_token)
        newN0 = max(i,newN0)
        newN1 = max(j,newN1)
    return new_points, map_to_original, newN0+1,newN1+1



def make_database_from_points_3D(points):
    newN0 = 0 
    newN1 = 0
    newN2 = 0
    new_points = []

    map_to_original = {}
    for point in points:
        i,j,k = point
        search_token = random.randrange(10000000)
        while search_token in map_to_original:
            search_token = random.randrange(10000000)
        map_to_original[search_token] = (i,j,k)
        new_points.append(search_token)
        newN0 = max(i,newN0)
        newN1 = max(j,newN1)
        newN2 = max(k,newN2)
    return new_points, map_to_original, newN0+1,newN1+1,newN2+1


def get_random_database(N0,N1, max_points, plaintext=False):
    map_to_original = {}
    points = []
    for i in range(1,N0):
        for j in range(1,N1):
            repeats = int(1+(max_points-1)*random.random())
            for num in range(repeats):
                if plaintext:
                    search_token = (i,j)
                else:
                    search_token = random.randrange(10000000)
                map_to_original[search_token] = (i,j)
                points.append(search_token)

    return points, map_to_original


def get_random_database_3D(N0,N1,N2, max_points):
    map_to_original = {}
    points = []
    for i in range(1,N0):
        for j in range(1,N1):
            for z in range(1,N2):
                repeats = int(1+(max_points-1)*random.random())
                for num in range(repeats):
                    search_token = random.randrange(10000000)
                    map_to_original[search_token] = (i,j,z)
                    points.append(search_token)

    return points, map_to_original



def get_responses(points,map_points_to_coordinates, N0, N1):
    resps = []
    for min0 in tqdm.tqdm(range(1,N0)):
        for min1 in range(1,N1):
            for max0 in range(min0,N0):
                for max1 in range(min1,N1):
                    r = []
                    for p in points:
                        if map_points_to_coordinates[p][0] <= max0 and map_points_to_coordinates[p][0] >= min0 and map_points_to_coordinates[p][1] <= max1 and map_points_to_coordinates[p][1] >= min1:
                            r.append(p)
                    resps.append(set(r))

    return resps

def get_responses_no_vals(points,map_points_to_coordinates, N0, N1):
    resps = []
    for min0 in tqdm.tqdm(range(1,N0)):
        for min1 in range(1,N1):
            for max0 in range(min0,N0):
                for max1 in range(min1,N1):
                    # r = []
                    # for p in points:
                    #     if map_points_to_coordinates[p][0] <= max0 and map_points_to_coordinates[p][0] >= min0 and map_points_to_coordinates[p][1] <= max1 and map_points_to_coordinates[p][1] >= min1:
                    #         r.append(p)
                    resps.append((min0,max0,min1,max1))

    return resps


def get_actual_resps_after_sampling(resps,points,map_points_to_coordinates):
    actual = []

    unique_rs = set()

    for min0,max0,min1,max1 in tqdm.tqdm(resps):
        r = []
        for p in points:
            if map_points_to_coordinates[p][0] <= max0 and map_points_to_coordinates[p][0] >= min0 and map_points_to_coordinates[p][1] <= max1 and map_points_to_coordinates[p][1] >= min1:
                r.append(p)
                unique_rs.add(map_points_to_coordinates[p])
        actual.append(set(r))
    return actual,unique_rs


def get_responses_3D(points,d, N0, N1,N2):
    resps = []
    i = 0
    for min0 in tqdm.tqdm(range(1,N0)):
        for min1 in range(1,N1):
            for min2 in range(1,N2):
                for max0 in range(min0,N0):
                    for max1 in range(min1,N1):
                        for max2 in range(min2,N2):
                            r = []
                            for p in points:
                                if d[p][0] <= max0 and d[p][0] >= min0 and d[p][1] <= max1 and d[p][1] >= min1 and d[p][2] <= max2 and d[p][2] >= min2:
                                    r.append(p)
                            resps.append(set(r))
                            i+=1
    return resps

def get_responses_no_vals_3D(points,d, N0, N1,N2):
    resps = []
    for min0 in tqdm.tqdm(range(1,N0)):
        for min1 in range(1,N1):
            for min2 in range(1,N2):
                for max0 in range(min0,N0):
                    for max1 in range(min1,N1):
                        for max2 in range(min2,N2):
                            #r = []
                            #for p in points:
                            #    if d[p][0] <= max0 and d[p][0] >= min0 and d[p][1] <= max1 and d[p][1] >= min1 and d[p][2] <= max2 and d[p][2] >= min2:
                            #        r.append(p)
                            resps.append((min0,max0,min1,max1,min2,max2))
    return resps


def get_actual_resps_after_sampling_3D(resps,points,map_points_to_coordinates):
    actual = []

    unique_rs = set()

    for min0,max0,min1,max1,min2,max2 in tqdm.tqdm(resps):
        r = []
        for p in points:
            if map_points_to_coordinates[p][0] <= max0 and map_points_to_coordinates[p][0] >= min0 and map_points_to_coordinates[p][1] <= max1 and map_points_to_coordinates[p][1] >= min1 and map_points_to_coordinates[p][2] <= max2 and map_points_to_coordinates[p][2] >= min2:
                r.append(p)
                unique_rs.add(map_points_to_coordinates[p])
        actual.append(set(r))
    return actual,unique_rs






def sample_gaussian(resps, needed):
    to_return = []
    while len(to_return) < needed:
        index =int(random.gauss(len(resps)/2,len(resps)/5))
        if index >= 0 and index < len(resps)-1:
            to_return.append(resps[index])
    return to_return


def sample_beta(resps, needed):
    to_return = []
    for i in range(needed):
        index =int(random.betavariate(2, 1)*(len(resps)-1))
        index = min(index, len(resps)-1)
        index = max(index,0)
        to_return.append(resps[index])
    return to_return

def sample_uniform(resps, needed):
    return random.sample(resps, needed)



