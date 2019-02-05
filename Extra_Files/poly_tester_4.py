def poly(order=2,level=1,levels=3,powers=[0,0,0],memo={}):
    # if powers in memo:
    #     return memo
    # memo[tuple(powers)] = powers

    for pow in range(order+1):
        powers[level-1] = pow
        if sum(powers) <= order:
            memo[tuple(powers)] = 'done'
        # print('\t', level, pow, powers)
        if level < levels:
            poly(level=level+1,powers=powers,memo=memo)

    return memo

my_ans = poly()

print(len(my_ans))
print(my_ans.keys())