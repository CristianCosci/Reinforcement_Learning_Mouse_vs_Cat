# TodoList

- [x] Ambiente
- [x] Agente
- [x] Cat 
- [x] Mouse
- [ ] Controllo che impara ad evitare i muri
- [ ] Controllo se impara ad evitare gli ostacoli
- [ ] Usare distanza di manatthan come distanza e non differenza tra gli assi singoliS
- [x] Posizionamento casuale topo
- [x] Posizionamento casuale gatto stupido
- [x] Posizionamento casuale formaggio
- [x] Posizionamento gatto (stupido) topo formaggio casuale
- [x] Train
- [x] Test
- [x] Definire gatto e topo come sottoclassi di agente (Non va bene)
- [x] Reward negativa se tocca i muri
- [ ] Provare con due gatti
- [ ] Provare varie strategia per vedere le diverse policies
    - [ ] Ad esempio vedere che succede se il gatto conosce anche la posizione del formaggio (in teoria dovrebbe aspettare li il topo)
- [ ] Eventuali plot

NOTE:
- Apparentemente non sembra apprendere che deve evitare i muri. Probabilmente è dovuto al fatto che l'agente non ha informazioni sulla posizione ma solo sulle distanze. Procavare a dare anche le coordinate come stato e vedere se impara ad evitare i muri (logicamente dovrebbe capire quali sono i bordi ed evitarli). 
- Se funziona fare stessa cosa per gli ostacoli (una volta introdotti nel sistema).
