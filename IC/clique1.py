import networkx as nx
def find_cliques(G1):
    # Cache nbrs and find first pivot (highest degree)
    maxconn=-1
    nnbrs={}
    pivotnbrs=set() # handle empty graph
    for n,nbrs in G1.adjacency():
        nbrs=set(nbrs)
        nbrs.discard(n)
        conn = len(nbrs)
        if conn > maxconn:
            nnbrs[n] = pivotnbrs = nbrs
            maxconn = conn
        else:
            nnbrs[n] = nbrs
    # Initial setup
    cand=set(nnbrs)
    smallcand = set(cand - pivotnbrs)
    done=set()
    stack=[]
    clique_so_far=[]
    # Start main loop
    while smallcand or stack:
        try:
            # Any nodes left to check?
            n=smallcand.pop()
        except KeyError:
            # back out clique_so_far
            cand,done,smallcand = stack.pop()
            clique_so_far.pop()
            continue
        # Add next node to clique
        clique_so_far.append(n)
        cand.remove(n)
        done.add(n)
        nn=nnbrs[n]
        new_cand = cand & nn
        new_done = done & nn
        # check if we have more to search
        if not new_cand:
            if not new_done:
                # Found a clique!
                yield clique_so_far[:]
            clique_so_far.pop()
            continue
        # Shortcut--only one node left!
        if not new_done and len(new_cand)==1:
            yield clique_so_far + list(new_cand)
            clique_so_far.pop()
            continue
        # find pivot node (max connected in cand)
        # look in done nodes first
        numb_cand=len(new_cand)
        maxconndone=-1
        for n in new_done:
            cn = new_cand & nnbrs[n]
            conn=len(cn)
            if conn > maxconndone:
                pivotdonenbrs=cn
                maxconndone=conn
                if maxconndone==numb_cand:
                    break
        # Shortcut--this part of tree already searched
        if maxconndone == numb_cand:
            clique_so_far.pop()
            continue
        # still finding pivot node
        # look in cand nodes second
        maxconn=-1
        for n in new_cand:
            cn = new_cand & nnbrs[n]
            conn=len(cn)
            if conn > maxconn:
                pivotnbrs=cn
                maxconn=conn
                if maxconn == numb_cand-1:
                    break
        # pivot node is max connected in cand from done or cand
        if maxconndone > maxconn:
            pivotnbrs = pivotdonenbrs
        # save search status for later backout
        stack.append( (cand, done, smallcand) )
        cand=new_cand
        done=new_done
        smallcand = cand - pivotnbrs
        
        
def graph_number_of_cliques(H,cliques=None):
   
    if cliques is None:
        cliques=list(find_cliques(H))
    return  len(cliques)
def find_k_cliques(net,k,p):
    cliques = list(find_cliques(net))
    cliques = sorted(cliques,key = len,reverse = True)
    cli_deg = []
    for i in range(len(cliques)):
        cli_deg.append([])
        for j in range(len(cliques[i])):
            cli_deg[i].append({'node':cliques[i][j],'deg':net.degree(cliques[i][j])})
    for i in range(len(cliques)):
        cli_deg[i] = sorted(cli_deg[i], key = lambda k:k['deg'])
        cliques[i] = [d['node'] for d in cli_deg[i]]
    del cli_deg
    result = []
    seed_count = k
    turn = 1
    while True:
        take = int(k/len(cliques))
        upto = k%len(cliques)
        for i in range(len(cliques)):
            if turn ==1:
                if i < upto:
                    t = take + 1
                else:
                    t = take
                turn+=1    
            else:
                t = 1
            p = 0
            while p < t:
                 if p < len(cliques[i]):
                    if cliques[i][p] not in result:
                        result.append(cliques[i][p])
                        #print(result)
                        if len(result) == seed_count:
                            break
                    else:
                        t+=1
                    p+=1
                    
                 else:
                    break
            if len(result) == seed_count:
                break
        if len(result) == seed_count:
            break
        else:
            k = seed_count - len(result)
    return result
