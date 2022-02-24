## **policy_gattoStupido/OnlyRandomCheese/mouse**:
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte da (0,0)
    - Il gatto viene generato a metà griglia in alto
    - Info Training:
        - 10k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido
        - il topo sbatte sul muro, e impara nella parte finale leggermente

## **policy_gattoStupido/OnlyRandomMouse/mouse**:
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il topo viene generato in una posizione casuale nella parte sinistra della griglia
    - Il formaggio parte da (9,5)
    - Il gatto viene generato a metà griglia in alto
    - Info Training:
        - 10k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido
        - il topo impara a non sbattere sul muro (nella parte finale non sbatte quasi mai, max 1/2 volte)

## policy_gattoStupido/RandomCat&Cheese/mouse
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte da (0,0)
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale
     - Info Training:
        - 10k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido (ci mette qualche epoca in più delle due precedenti, circa 300)
        - il topo sbatte sul muro, e impara nella parte finale leggermente



## policy_gattoStupido/AllaRandom/mouse
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte nella parte sinistra della griglia in una posizione casuale
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale
    - Info Training:
        - 10k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido (ci mette qualche epoca in più delle due precedenti, circa 600   )
        - il topo sbatte sul muro, e impara nella parte finale leggermente

<hr>

## policy_gattoStupido/AllaRandom/evitaMuri/mouse
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte nella parte sinistra della griglia in una posizione casuale
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale
    - In più il topo come stato riceve in input anche le sue coordinate, come tentativo per vedere se riesce ad imparare ad evitare i muri.
        - Le coordinate sono date singolarmente e non come coppia.
    - Info Training:
        - 20k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido (ci mette qualche epoca in più delle due precedenti, circa 3000)
        - il topo sbatte sul muro, e impara nella parte finale leggermente

## policy_gattoStupido/AllaRandom/evitaMuri/mouse2
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte nella parte sinistra della griglia in una posizione casuale
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale
    - In più il topo come stato riceve in input anche le sue coordinate, come tentativo per vedere se riesce ad imparare ad evitare i muri.
        - Le coordinate sono date come coppia.
    - Info Training:
        - 20k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido (ci mette qualche epoca in più delle due precedenti, circa 3000)
        - il topo sbatte sul muro, e impara nella parte finale leggermente

## ***apparentemente questa tecnica non permette di evitare di andare a sbattere nel muro, anzi sembra aver peggiorato sia il training che il test***

<hr>

## policy_gattoStupido/AllaRandom/evitaMuri/mouse3
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte nella parte sinistra della griglia in una posizione casuale
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale
    - In più il topo come stato riceve in input anche la distanza più vicina da un muro, come tentativo per vedere se riesce ad imparare ad evitare i muri.
        - La distanza è calcolata da un'apposita funzione
    - Info Training:
        - 20k epochs
        - 100 steps
    - note:
        - il topo impara a battere facilmente il gatto stupido (ci mette qualche epoca in più delle due precedenti, circa 2000)
        - il topo sbatte sul muro inizialemente come sempre, e impara completamente nella parte finale 
