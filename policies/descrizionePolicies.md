# **Policies**

## Indice
- [Gatto Sentinella](#gatto-sentinella)
    - [Gatto Singolo](#gatto-singolo)
        - [Senza ostacoli](#senza-ostacoli)
        - [Con ostacoli](#con-ostacoli)
        - [Con parete diblocco](#con-parete-di-blocco)
        - [Confronto gamma](#confronto-gamma)
<hr>

# **Gatto Sentinella**

## **Gatto Singolo**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- Il gatto viene generato nella parte centrale della mappa e si muove lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle distanze di manatthan verso il gatto e il formaggio. In aggiunta c'è la distanza verso il muro più vicino.

### Parametri di train
- Prova1
    - 10k epoche
    - 100 steps
    - Gamma: gamma=0.85
    - Lr: alpha = 0.1
    - Eps: epsilon, eps_decay, eps_min = 1.0, 0.9994, 0.05
    - Note:
        Viene inoltre fornito un test di esempio con gamma = 0.99 dove si può notare come la policy costruita risulta peggiore.

## **Senza ostacoli**
Il topo impara facilmente a battere il gatto non facendosi mai prendere e a mangiare il formaggio.
- **Risultati di train**:
    - Vittorie Gatto 544    | 430 se reward ostacoli diverse
    - Vittorie Topo 8942    | 9038 se reward ostacoli diverse
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 0      | 0 se reward ostacoli diverse
    - Vittorie Topo 9193    | 9854 se reward ostacoli diverse
    - Muri toccati 4575     | 3938 se reward ostacoli diverse

## **Con ostacoli**
Il topo impara facilmente a battere il gatto non facendosi mai prendere e a mangiare il formaggio.
- **Risultati di train**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati
- **Risultati di test**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati

## **Con parete di blocco**
Il topo impara facilmente a battere il gatto non facendosi mai prendere e a mangiare il formaggio evitando anche la parete.
- **Risultati di train**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati
- **Risultati di test**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati

## **Confronto gamma**
Viene utilizzato un gamma = 0.99. Anche in questo caso il topo apprende ma si hanno performance peggiori.
- **Risultati di train**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati
- **Risultati di test**:
    - Vittorie Gatto
    - Vittorie Topo
    - Muri toccati