# **Policies**

## Indice
- [Gatto Sentinella](#gatto-sentinella)
    - [Gatto Singolo](#gatto-singolo)
        - [Senza ostacoli](#senza-ostacoli)
        - [Con ostacoli](#con-ostacoli)
    - [Gatto Sentinella Doppio](#gatto-sentinella-doppio)
        - [Gatto doppio Verticale](#gatto-doppio-verticale)
        - [Gatto doppio Misto](#gatto-doppio-misto)
- [Gatto Intelligente](#)

<hr>

# **Gatto Sentinella**

## **Gatto singolo**
- Il topo viene generato nella parte sinistra della mappa in una posizione casuale.
- Il gatto viene generato nella parte centrale della mappa e si muove lungo l'asse verticale. La posizione è generata casualmente.
- Il formaggio viene generato nella parte destra della mappa in una posizione casuale.
- Il topo ha come input la distanza di Manhattan dal gatto, le informazioni relative agli ostacoli e la distanza di Manhatthan dal formaggio.
- Nel caso con gli ostacoli si sceglie un riempimento percentuale della mappa con gli ostacoli

### **Senza Ostacoli**
Parametri di train:
- epsilon, eps_decay, eps_min = 1.0, 0.9996, 0.05
- num_episodes = 10000

Risultati di train:
- Vittorie gatto: 725
- Vittorie topo: 8675
- Info sui muri e gli ostacoli: Il topo impara a evitare i muri. Non ci sono info sugli ostacoli.

Risultati di test su 10000 epoche:
- Vittorie gatto: 0
- Vittorie topo: 9970
- Info sui muri e gli ostacoli: Muro -> 4313 ; Ostacolo niente info

<hr>

### **Senza Ostacoli**
Parametri di train:
- epsilon, eps_decay, eps_min = 1.0, 0.9998, 0.05
- num_episodes = 20000
- Riempimento ostacoli 10%

Risultati di train:
- Vittorie gatto: 2144
- Vittorie topo: 14995
- Info sui muri e gli ostacoli: Il topo impara a evitare i muri. Non ci sono info sugli ostacoli.

Risultati di test su 10000 epoche:
- Vittorie gatto: 0
- Vittorie topo: 9970
- Info sui muri e gli ostacoli: Muro -> 4313 ; Ostacolo niente info

