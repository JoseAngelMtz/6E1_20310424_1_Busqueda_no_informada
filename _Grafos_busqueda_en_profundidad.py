
import networkx as nx
import matplotlib.pyplot as plt

class Accion:
    def __init__(self,nombre):
        self.nombre=nombre
        
    def __str__(self):
        return self.nombre


#%%Estado
class Estado:
    def __init__(self,nombre,acciones):
        self.nombre=nombre
        self.acciones=acciones
        
    def __str__(self):
        return self.nombre


#%%Problema
class Problema:
    def __init__(self,estado_inicial,estados_objetivos,acciones,
                 costes=None,heuristicas=None):
        self.estado_inicial=estado_inicial
        self.estados_objetivos=estados_objetivos
        self.acciones=acciones
        self.costes=costes
        self.heuristicas=heuristicas
        self.infinito=99999
        if not self.costes:
            self.costes={}
            for estado in self.acciones.keys():
                self.costes[estado]={}
                for accion in self.acciones[estado].keys():
                    self.costes[estado][accion]=1
        if not self.heuristicas:
            self.heuristicas={}
            for estado in self.acciones.keys():
                self.heuristicas[estado]={}
                for objetivo in self.estados_objetivos:
                    self.heuristicas[estado][objetivo]=self.infinito

    def __str__(self):
        msg="Estado Inicial: {0} -> Objetivos: {1}"
        return msg.format(self.estado_inicial.nombre,
                          self.estados_objetivos)
    
    def es_objetivo(self,estado):
        return estado in self.estados_objetivos
    
    def resultado(self,estado,accion):
        if estado.nombre not in self.acciones.keys():
            return None
        acciones_estado=self.acciones[estado.nombre]
        if accion.nombre not in self.acciones[estado.nombre]:
            return None
        return acciones_estado[accion.nombre]
    
    def coste_accion(self,estado,accion):
        if estado.nombre not in self.costes.keys():
            return self.infinito
        costes_estado=self.costes[estado.nombre]
        if accion.nombre not in costes_estado.keys():
            return self.infinito
        return costes_estado[accion.nombre]
    
    def coste_camino(self,nodo):
        total=0
        while nodo.padre:
            total+=self.coste_accion(nodo.padre.estado, nodo.accion)
            nodo=nodo.padre
        return total


#%%Nodo
class Nodo:
    def __init__(self,estado,accion=None,acciones=None,padre=None):
        self.estado=estado
        self.accion=accion
        self.acciones=acciones
        self.padre=padre
        self.hijos=[]
        self.coste=0
        self.heuristicas={}
        self.valores={}
        self.alfa=0
        self.beta=0
        
    def __str__(self):
        return self.estado.nombre
    
    def expandir(self,problema):
        self.hijos= []
        if not self.acciones:
            if self.estado.nmbre not in problema.acciones.keys():
                return self.hijos
            self.acciones=problema.acciones[self.estado.nombre]
        for accion in self.acciones.keys():
            accion_hijo=Accion(accion)
            nuevo_estado=problema.resultado(self.estado,accion_hijo)
            acciones_nuevo={}
            if nuevo_estado.nobre in problema.acciones.keys():
                acciones_nuevo=problema.acciones[nuevo_estado.nombre]
            hijo=Nodo(nuevo_estado,accion_hijo,acciones_nuevo,self)
            coste=self.padre.coste if self.padre else 0
            coste+=problema.coste_accion(self.estado,accion_hijo)
            hijo.coste=coste
            hijo.heuristicas=problema.heuristicas[hijo.estado.nombre]
            hijo.valores={estado:heuristica+hijo.coste
                          for estado,heuristica
                          in hijo.heuristicas.items()}
            self.hijos.append(hijo)
        return self.hijos
    
    def hijo_mejor(self,problema,metrica='valor',criterio='menor'):
        if not self.hijos:
            return None
        mejor=self.hijos[0]
        for hijo in self.hijos:
            for objetivo in problema.estados_objetivos:
                if metrica=='valor':
                    valor_hijo=hijo.valores[objetivo.nombre]
                    valor_mejor=mejor.valores[objetivo.nombre]
                    if(criterio=='menor' and
                       valor_hijo<valor_mejor):
                        mejor=hijo
                    elif(criterio=='mayor' and
                         valor_hijo>valor_mejor):
                        mejor=hijo
                elif metrica=='heuristica':
                    heuristica_hijo=hijo.heuristicas[objetivo.nombre]
                    heuristica_mejor=mejor.heuristicas[objetivo.nombre]
                    if(criterio=='menor' and
                       heuristica_hijo<heuristica_mejor):
                        mejor=hijo
                    elif(criterio=='mayor' and
                         heuristica_hijo>heuristica_mejor):
                        mejor=hijo
                elif metrica=='coste':
                    coste_camino_hijo=problema.coste_camino(hijo)
                    coste_camino_mejor=problema.coste_camino(mejor)
                    if(criterio=='menor' and
                       coste_camino_hijo<coste_camino_mejor):
                        mejor=hijo
                    elif(criterio=='mayor' and
                       coste_camino_hijo>coste_camino_mejor):
                        mejor=hijo
                    elif metrica=='alfa':
                        if(criterio=='menor' and
                           hijo.alfa<mejor.alfa):
                            mejor=hijo
                        elif(criterio=='mayor' and
                             hijo.alfa>mejor.alfa):
                            mejor=hijo
                    elif metrica=='beta':
                        if(criterio=='menor' and
                           hijo.beta<mejor.beta):
                            mejor=hijo
                        elif(criterio=='mayor' and
                             hijo.beta>mejor.beta):
                            mejor=hijo
        return mejor

#%%
def Profundidad(problema):
 # Crea un nodo raíz
    raiz=crea_nodo_raiz(problema)
    # Verifica si el estado del nodo raíz es el objetivo
    if problema.es_objetivo(raiz.estado):
        return raiz
    # Agrega el nodo raíz a la frontera
    frontera=[raiz,]
    # Crea un conjunto vacío para los nodos explorados
    explorados=set()
    # Comienza un ciclo while que se ejecuta hasta que se encuentra el objetivo o la frontera está vacía
    while True:
        # Imprime los nodos en la frontera
        print("frontera: ",[nodo.estado.nombre for nodo in frontera])
        # Imprime los nodos explorados
        print("explorados: ",[estado.nombre for estado in explorados])
        # Si la frontera está vacía, devuelve None
        if not frontera:
            return None
        # Elimina un nodo de la frontera y lo agrega a los explorados
        nodo=frontera.pop()
        print("escoge: ",nodo.estado.nombre)
        print("-------")
        explorados.add(nodo.estado)
        # Si el nodo no tiene acciones, continúa con la siguiente iteración del ciclo while
        if not nodo.acciones:
            continue
        # Crea un hijo para cada acción y verifica si el estado del hijo ya está en los explorados o en la frontera
        for nombre_accion in nodo.acciones.keys():
            accion=Accion(nombre_accion)
            hijo=crea_nodo_hijo(problema,nodo,accion)
            estados_frontera=[nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and
               hijo.estado not in estados_frontera):
                # Si el estado del hijo es el objetivo, devuelve el hijo
                if problema.es_objetivo(hijo.estado):
                    return hijo
                # Agrega el hijo a la frontera
                frontera.append(hijo)
        continue

    # Crea un hijo para cada acción y verifica si el estado del hijo ya está en los explorados o en la frontera
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion)
        estados_frontera = [nodo.estado for nodo in frontera]

        if hijo.estado not in explorados and hijo.estado not in estados_frontera:
            # Si el estado del hijo es el objetivo, devuelve el hijo
            if problema.es_objetivo(hijo.estado):
                return hijo

            # Agrega el hijo al grafo y a la frontera
            frontera.append(hijo)


#%%
def crea_nodo_raiz(problema):
    # Obtiene el estado inicial del problema
    estado_raiz=problema.estado_inicial
    # Crea un diccionario vacío para las acciones de la raíz
    acciones_raiz={}
    # Si el nombre del estado raíz está en las acciones del problema, agrega las acciones al diccionario
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz=problema.acciones[estado_raiz.nombre]
    # Crea un nodo raíz con el estado raíz, sin padre, con las acciones de la raíz y sin acción
    raiz=Nodo(estado_raiz,None,acciones_raiz,None)
    # Devuelve el nodo raíz
    return raiz
#%%
def crea_nodo_hijo(problema,padre,accion):
    # Obtiene el nuevo estado a partir del estado del padre y la acción
    nuevo_estado=problema.resultado(padre.estado,accion)
    # Crea un diccionario vacío para las acciones del nuevo estado
    acciones_nuevo={}
    # Si el nombre del nuevo estado está en las acciones del problema, agrega las acciones al diccionario
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo=problema.acciones[nuevo_estado.nombre]
    # Crea un nodo hijo con el nuevo estado, la acción, las acciones del nuevo estado y el padre
    hijo=Nodo(nuevo_estado,accion,acciones_nuevo,padre)
    # Agrega el nodo hijo a la lista de hijos del padre
    padre.hijos.append(hijo)
    # Devuelve el nodo hijo
    return hijo
#%%
def muestra_solucion(objetivo=None):
    if not objetivo:
        print("no hay solución")
        return
    nodo=objetivo
    while nodo:
        msg="Estado: {0}"
        print(msg.format(nodo.estado.nombre))
        if nodo.accion:
            msg="<--- {0} ---"
            print(msg.format(nodo.accion.nombre))
        nodo=nodo.padre
            

#%%Definiciones
if __name__=='__main__':
    accN=Accion('Norte')
    accS=Accion('Sur')
    accE=Accion('Este')
    accO=Accion('Oeste')
   
    
    
    lanoi=Estado('lanoi', [accN,accO])
    nohoi=Estado('nohoi', [accN,accS,accE,accO])
    ruun=Estado('ruun', [accN,accS,accO])
    milos=Estado('milos', [accN,accE])
    ghiido=Estado('ghiido', [accN,accS,accO])
    kuart=Estado('kuart', [accS,accE])
    boomon=Estado('boomon', [accS,accO])
    goorum=Estado('goorum', [accN,accE])
    shiphos=Estado('shiphos', [accS,accE])
    
    viajes={'lanoi':{'norte':ruun,
                        'oeste':milos},
            'nohoi':{'norte':shiphos,
                          'sur':milos,
                          'este':ruun,
                          'oeste':goorum},
            'ruun':{'norte':ghiido,
                       'sur':lanoi,
                       'oeste':nohoi},
            'milos':{'norte':nohoi,
                         'este':lanoi},
            'ghiido':{'norte':boomon,
                       'sur':ruun,
                       'oeste':shiphos},
            'kuart':{'sur':goorum,
                          'este':boomon},
            'boomon':{'sur':ghiido,
                       'oeste':kuart},
            'goorum':{'norte':kuart,
                         'este':nohoi},
            'shiphos':{'sur':nohoi,
                         'este':ghiido}}
    
   
    G=nx.DiGraph()
    for e in viajes.keys():
        G.add_node(e)
    for origen in viajes.keys():
        for destino in viajes[origen].keys():
            G.add_edge(origen,viajes[origen][destino].nombre)

    pos=nx.spring_layout(G)
    nx.draw(G,pos,with_labels=True,font_weight='bold')
    plt.show()
    
    objetivo_1=[boomon]
    problema_1=Problema(lanoi,objetivo_1,viajes)
    
   
    
    problema_resolver=problema_1
    
    solucion=Profundidad(problema_resolver)
    muestra_solucion(solucion)
