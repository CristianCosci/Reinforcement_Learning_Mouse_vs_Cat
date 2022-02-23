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
        -  il topo sbatte sul muro, e impara nella parte finale leggermente



- policy_gattoStupido/AllaRandom/mouse
    - Prova con gatto guardiano del formaggio in modo stupido (solo su e giù in verticale)
    - Il formaggio viene generato in una posizione casuale nella parte protetta dal gatto guardiano
    - Il topo parte nella parte sinistra della griglia in una posizione casuale
    - Il gatto viene generato a metà griglia in una posizione di altezza casuale