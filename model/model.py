import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._grafo = nx.DiGraph()
        self._edges = []
        self._anno = None
        self._idMapPosizione = {}
        self._races = []
        self._idMapVittorie = {}
        pass


    def getAnni(self):
        return DAO.getAnni()

    def creaGrafo(self, a):
        self._grafo.clear_edges()
        self._grafo.clear()
        self._anno = a
        self._nodes = DAO.getDrivers(a)
        self._races = DAO.getRaces(a)
        drp = DAO.getCose(a)
        for i in drp:
            driver = i[0]
            race = i[1]
            position = i[2]

            self._idMapPosizione[(driver,race)] = position
        for ra in self._races:
            #archi = []
            sconfitti = []
            primo = None
            posizioni = dict(sorted(self._idMapPosizione.items(), key=lambda x: x[1]))
            nodi = []
            for d , r in posizioni.keys() :
                if ra == r:
                    #print(posizioni[d, ra])
                    nodi.append(d)
            n = 0

            while n != len(nodi)-1 :
                for dr in nodi:
                    if nodi.index(dr)> n:
                        if (nodi[n], dr)  in self._idMapVittorie.keys() :
                            self._idMapVittorie[(nodi[n], dr)] += 1
                        else:
                            self._idMapVittorie[(nodi[n], dr)] = 1


                        if self._grafo.has_edge(nodi[n], dr) == True:
                            ind = self._edges.index((nodi[n], dr))
                            self._edges[ind] = (nodi[n], dr, {'weight': self._idMapVittorie[(nodi[n], dr)]})
                        else:
                            self._edges.append((nodi[n], dr, {'weight': self._idMapVittorie[(nodi[n], dr)]}))

                n += 1


        self._grafo.add_nodes_from(self._nodes)
        self._grafo.add_edges_from(self._edges)




    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)


    def getBest(self):
        self._best = 0
        self._bestP = None

        for p in self._nodes:

            peso_uscenti = sum(data["weight"] for _, _, data in self._grafo.out_edges(p, data=True))
            peso_entranti = sum(data["weight"] for _, _, data in self._grafo.in_edges(p, data=True))
            risultato = peso_uscenti - peso_entranti
            if risultato > self._best:
                self._best = risultato
                self._bestP = p

        return self._bestP, self._best

    def cercaDreamTeam(self, k):
        self._best_team = []
        self._min_defeats = float('inf')


        self._ricorsione([], 0, 0, k)

        return self._best_team, self._min_defeats

    def _ricorsione(self, parziale, livello, start, k):
        if livello == k:
            sconfitte = self._calcolaSconfitte(parziale)
            if sconfitte < self._min_defeats:
                self._min_defeats = sconfitte
                self._best_team = parziale.copy()
            return

        for i in range(start, len(self._nodes)):
            parziale.append(self._nodes[i])
            self._ricorsione(parziale, livello + 1, i + 1, k)
            parziale.pop()

    def _calcolaSconfitte(self, team):
        team_set = set(team)
        sconfitte = 0
        for u, v in self._grafo.edges():
            if u not in team_set and v in team_set:
                sconfitte += 1
        return sconfitte



