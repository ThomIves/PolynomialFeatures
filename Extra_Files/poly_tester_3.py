def poly(order=2,level=0,levels=2,powers=[0,0,0]):
    for pow in range(order+1):
        powers[level] = pow
        print('\t', level, pow, powers)
        if level < levels:
            poly(level=level+1,powers=powers)


poly()

