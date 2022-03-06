# **Policies**

## Indice
- [Gatto Sentinella](#gatto-sentinella)
    - [Gatto Singolo](#gatto-singolo)
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