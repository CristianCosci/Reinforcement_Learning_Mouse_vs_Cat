# **Policies**

## Indice
- [Gatto Sentinella](#gatto-sentinella)
    - [Gatto Singolo](#gatto-singolo)
        - [Senza ostacoli](#senza-ostacoli)
        - [Con ostacoli](#con-ostacoli)
        - [Con parete diblocco](#con-parete-di-blocco)
        - [Confronto gamma](#confronto-gamma)
    - [Gatto Sentinella Doppio](#gatto-sentinella-doppio)
        - [Gatto doppio Verticale](#gatto-doppio-verticale)
        - [Gatto doppio Misto](#gatto-doppio-misto)
<hr>

# **Gatto Sentinella**

## **Gatto Singolo**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- Il gatto viene generato nella parte centrale della mappa e si muove lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle distanze di manatthan verso il gatto e il formaggio. In aggiunta c'è la visuale del topo che vede il muro a lui adiacente (e in un altro caso vede il muro una cella prima).

### Parametri di train
- Prova
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
    - Vittorie Gatto 544, 619    | 430 se reward ostacoli diverse (5)    | 504 se reward ostacoli diverse (10)  | 641 se vede i muri prima
    - Vittorie Topo 8942, 8930   | 9038 se reward ostacoli diverse (5)   | 9010 se reward ostacoli diverse (10) | 9073 se vede i muri prima
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 0, 0           | 0 se reward ostacoli diverse          | 0 se reward ostacoli diverse (10)    | 0 se vede i muri prima
    - Vittorie Topo 9193, 9622      | 9854 se reward ostacoli diverse (5)   | 9646 se reward ostacoli diverse (10) | 10000 se vede i muri prima
    - Muri toccati 4575, 3519       | 3938 se reward ostacoli diverse (5)   | 3092 se reward ostacoli diverse (10) | 98 se vede i muri prima

## **Con ostacoli** [3,0], [3,3], [3,6], [3,9], [5,1], [5,4], [5,7]
Il topo impara facilmente a battere il gatto non facendosi mai prendere e a mangiare il formaggio.
- **Risultati di train**:
    - Vittorie Gatto 1198
    - Vittorie Topo 7041
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 0
    - Vittorie Topo 9161
    - Muri toccati 151
    - Ostacoli toccati 394

## **Con parete di blocco** [3,2], [3,1], [3,0], [3,3], [3,4]
Il topo impara facilmente a battere il gatto non facendosi mai prendere e a mangiare il formaggio evitando anche la parete.
- **Risultati di train**:
    - Vittorie Gatto 601
    - Vittorie Topo 8352
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 0
    - Vittorie Topo 9029
    - Muri toccati 892
    - Ostacoli toccati 569

## **Confronto gamma** 
Viene utilizzato un gamma = 0.99. Anche in questo caso il topo apprende ma si hanno performance peggiori.
- **Risultati di train**:
    - Vittorie Gatto 625
    - Vittorie Topo 8251
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 62
    - Vittorie Topo 9233
    - Muri toccati 4389


### ***Note***
In tutti i casi il topo apprende come prendere il formaggio senza farsi catturare. Si hanno poche differenze cambiando i parametri, nonostante utilizzando un gamma di 0.85 si hanno le prestazioni mediamente migliori. Inoltre se il topo vede i muri in anticipo riesce ad evitarli sempre e si ottengono le prestazioni in assoluto migliori.

<hr>

# **Gatto Sentinella Doppio**
### Parametri di train
- Prova
    - 20k epoche
    - 100 steps
    - Gamma: gamma=0.85
    - Lr: alpha = 0.1
    - Eps: epsilon, eps_decay, eps_min = 1.0, 0.9994, 0.05
    - Note:
        Viene inoltre fornito un test di esempio con gamma = 0.99 dove si può notare come la policy costruita risulta peggiore.

## **Gatto Doppio Verticale**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- I due gatti vengono generati a 1/3 e 2/3 della mappa e si muovono lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle distanze di manatthan verso il gatto e il formaggio. Il topo vede il muro una cella prima.

- **Risultati di train**:
    - Vittorie Gatto 3803 con gamma = 1     | 3860 con gamma = 0.85
    - Vittorie Topo 14138 con gamma = 1     | 14476 con gamma = 0.85
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 172 con gamma = 1      | 133 con gamma = 0.85
    - Vittorie Topo 8519 con gamma = 1      | 8886 con gamma = 0.85
    - Muri toccati 1850 con gamme = 1       | 1963 con gamma = 0.85


## **Gatto Doppio Verticale (prova senza dare importanza al tocco dei muri)**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- I due gatti vengono generati a 1/3 e 2/3 della mappa e si muovono lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle 4 distanze (asse x e asse y) rispetto ai due gatti e dalle due distanze verso il formaggio.

- **Risultati di train**:
    - Vittorie Gatto 5039 con gamma = 1     |  con gamma = 0.85
    - Vittorie Topo  11617 con gamma = 1    |  con gamma = 0.85
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto 166 con gamma = 1      |  con gamma = 0.85
    - Vittorie Topo 8328 con gamma = 1      |  con gamma = 0.85
    - Muri toccati 39835                    |  con gamma = 0.85


## **Gatto Doppio Verticale (prova senza dare importanza al tocco dei muri ma 3 coopie)**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- I due gatti vengono generati a 1/3 e 2/3 della mappa e si muovono lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle 4 distanze (asse x e asse y) rispetto ai due gatti e dalle due distanze verso il formaggio.

- **Risultati di train**:
    - Vittorie Gatto 5956 con gamma = 1     |  con gamma = 0.85
    - Vittorie Topo 10613 con gamma = 1    |  con gamma = 0.85
    - Muri toccati N.D.



## **Gatto Doppio Verticale con ostacoli** [[2,2], [2,7], [7,2], [7,7], [4,5]]
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- I due gatti vengono generati a 1/3 e 2/3 della mappa e si muovono lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle distanze di manatthan verso il gatto e il formaggio. Il topo vede il muro una cella prima e gli ostacoli solo se li ha davanti.
- 30k epoche di train

- **Risultati di train**:
    - Vittorie Gatto  con gamma = 1    | 5507 con gamma = 0.85
    - Vittorie Topo  con gamma = 1     | 21620 con gamma = 0.85
    - Muri toccati N.D.
- **Risultati di test**:
    - Vittorie Gatto  con gamma = 1     | 19 con gamma = 0.85
    - Vittorie Topo  con gamma = 1      | 9287 con gamma = 0.85
    - Muri toccati  con gamme = 1       | 893 con gamma = 0.85
    - Ostacoli toccati                  | 1927 con gamma = 0.85 <br>
Il problema sta che vede i muri prima e gli ostacoli no.



## **Gatto Doppio Misto**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- I due gatti vengono generati a adfassjk e si muovono uno in orizzontale e uno in verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Lo stato tornato è dato dalle distanze di manatthan verso il gatto e il formaggio. In aggiunta c'è la distanza verso il muro più vicino.

<hr>