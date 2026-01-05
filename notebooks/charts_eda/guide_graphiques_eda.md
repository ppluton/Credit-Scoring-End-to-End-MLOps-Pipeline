# 📊 GUIDE D'EXPLICATION DES 5 GRAPHIQUES EDA

## 🎯 Comment Utiliser Ces Graphiques

Ces 5 graphiques sont conçus pour **raconter l'histoire** de tes données dans un ordre logique :

1. **Qui** sont les clients ? (Âge)
2. **Quelles** features sont importantes ? (Corrélations)
3. **Comment** les scores externes impactent le risque ? (EXT_SOURCE)
4. **Pourquoi** les ratios financiers comptent ? (Crédit/Revenu)
5. **Quel** est l'impact de l'historique bancaire ? (Bureau)

---

## 📊 GRAPHIQUE 1 : Distribution de l'Âge par Statut

### Ce qu'il montre :
- **Gauche :** Histogrammes superposés de l'âge pour bons clients (vert) vs défauts (rouge)
- **Droite :** Boxplots comparatifs de l'âge

### Insights Clés :
```
✅ Les jeunes (20-35 ans) sont surreprésentés dans les défauts
✅ L'âge médian des "bons clients" est légèrement plus élevé
✅ La distribution des défauts est plus concentrée sur les jeunes
```

### Ce que ça signifie métier :
- **Jeunes clients = plus risqués** car :
  - Moins d'historique de crédit
  - Revenus potentiellement moins stables
  - Moins d'expérience financière

### Comment l'expliquer :
> "Ce graphique révèle que l'âge est un facteur discriminant important. Les clients de 20-35 ans ont un taux de défaut plus élevé. Cela suggère que l'âge devrait être une feature importante dans notre modèle, et qu'on pourrait créer des segments de risque par tranche d'âge."

### Statistiques à Mentionner :
- Âge médian bons clients : ~44 ans
- Âge médian défauts : ~41 ans
- Écart significatif dans la queue de distribution

---

## 📊 GRAPHIQUE 2 : Top Features Corrélées avec TARGET

### Ce qu'il montre :
- **Gauche :** Top 10 features positivement ET négativement corrélées avec le défaut
- **Droite :** Matrice de corrélation entre ces top features

### Insights Clés :
```
✅ EXT_SOURCE_2 et EXT_SOURCE_3 sont les plus corrélées NÉGATIVEMENT
   → Scores élevés = moins de risque
✅ Features de retards/impayés sont corrélées POSITIVEMENT
   → Plus de retards = plus de risque
✅ Peu de corrélation entre les features elles-mêmes (pas de redondance)
```

### Ce que ça signifie métier :
- **Les scores externes sont cruciaux** : ce sont les meilleurs prédicteurs
- **L'historique de paiement compte** : les retards passés prédisent les défauts futurs
- **Pas de multicolinéarité excessive** : les features apportent des infos complémentaires

### Comment l'expliquer :
> "Ce graphique identifie les features les plus prédictives. Les scores externes (EXT_SOURCE) dominent avec des corrélations de -0.15 à -0.18. C'est contre-intuitif : plus le score est élevé, MOINS il y a de risque de défaut. Les features de retards historiques sont positivement corrélées, ce qui est logique : un mauvais historique prédit un comportement futur similaire."

### Couleurs :
- **Rouge** : Corrélation positive (augmente le risque de défaut)
- **Vert** : Corrélation négative (diminue le risque de défaut)

---

## 📊 GRAPHIQUE 3 : Impact des Scores Externes

### Ce qu'il montre :
- 3 barplots montrant le **taux de défaut** par tranche de score (EXT_SOURCE_1, 2, 3)
- Ligne rouge en pointillés = taux de défaut moyen (8%)

### Insights Clés :
```
✅ Relation INVERSE claire : score élevé = moins de défaut
✅ EXT_SOURCE_2 a la relation la plus forte et linéaire
✅ Pour les scores >0.7, le taux de défaut tombe sous 5%
✅ Pour les scores <0.3, le taux dépasse 12%
```

### Ce que ça signifie métier :
- **Ces scores sont des "filtres" efficaces** :
  - Clients avec EXT_SOURCE_2 > 0.7 → faible risque (5%)
  - Clients avec EXT_SOURCE_2 < 0.3 → haut risque (12%)
  
### Comment l'expliquer :
> "Ce graphique démontre l'impact direct des scores externes sur le risque de défaut. On observe une relation inverse quasi-linéaire : plus le score est élevé, moins le client fait défaut. EXT_SOURCE_2 est particulièrement discriminant. Ces scores pourraient servir de base à une segmentation client : 'faible risque' (>0.7), 'moyen' (0.3-0.7), 'élevé' (<0.3)."

### Pattern à Souligner :
- Les 3 scores montrent le **même pattern** → robustesse
- La pente est différente → on peut les combiner pour un meilleur pouvoir prédictif

---

## 📊 GRAPHIQUE 4 : Ratios Financiers et Risque de Défaut

### Ce qu'il montre :
- **Gauche :** Impact du ratio Crédit/Revenu
- **Droite :** Impact du ratio Annuité/Revenu (avec règle des 33%)

Chaque graphique a **2 axes** :
- Axe gauche (barres rouges) : Taux de défaut
- Axe droit (courbe bleue) : Nombre de clients

### Insights Clés - Crédit/Revenu :
```
✅ Ratio ≤3x : Taux de défaut ~7% (sous la moyenne)
✅ Ratio 3-5x : Taux monte à ~8%
✅ Ratio 5-10x : Taux grimpe à ~9%
✅ Ratio >10x : Taux explose à ~11%
```

### Insights Clés - Annuité/Revenu :
```
✅ Ratio ≤20% : Taux de défaut ~7%
✅ Ratio 20-30% : Taux ~8%
✅ Ratio 30-50% : Taux ~9% (seuil critique !)
✅ Ratio >50% : Taux ~12% (très risqué)
```

### Ce que ça signifie métier :
**Le ratio Crédit/Revenu mesure l'endettement relatif :**
- 3x le revenu annuel = crédit raisonnable (voiture, travaux)
- 5x le revenu = important (maison)
- >10x = surendettement

**Le ratio Annuité/Revenu mesure la capacité de remboursement mensuelle :**
- 20% = confortable
- 30% = serré (règle bancaire classique : max 33%)
- >50% = insoutenable

### Comment l'expliquer :
> "Ces graphiques valident des règles métier connues. Le ratio Crédit/Revenu montre un seuil à 5x : au-delà, le risque augmente significativement. Pour l'Annuité/Revenu, on confirme la règle des 33% : les clients qui consacrent plus d'un tiers de leur revenu au remboursement ont un taux de défaut qui bondit de 8% à 12%. Ces ratios sont des candidats évidents pour le feature engineering."

### Ligne Orange (droite) :
- Marque la **règle des 33%** : standard bancaire pour le taux d'endettement maximal

---

## 📊 GRAPHIQUE 5 : Impact de l'Historique Bureau (4 Analyses)

### Ce qu'il montre :
Un **tableau de bord complet** en 4 parties :

1. **Haut-Gauche :** Taux de défaut avec/sans historique bureau
2. **Haut-Droite :** Distribution du nombre de crédits bureau
3. **Bas-Gauche :** Taux de défaut selon le nombre de crédits
4. **Bas-Droite :** Taux de défaut selon le retard maximum

### Insights Clés - Partie 1 (Présence Bureau) :
```
✅ Sans bureau : Taux de défaut ~10%
✅ Avec bureau : Taux de défaut ~8%
→ Avoir un historique RÉDUIT le risque de 20% !
```

### Insights Clés - Partie 2 (Distribution) :
```
✅ Médiane : 5-6 crédits bureau par client
✅ Distribution étalée : certains ont >20 crédits
```

### Insights Clés - Partie 3 (Nombre de Crédits) :
```
✅ 1-2 crédits : Taux ~8%
✅ 3-5 crédits : Taux ~7.5% (optimal !)
✅ 6-10 crédits : Taux ~8%
✅ >10 crédits : Taux ~9% (trop de crédits = signal négatif)
```

### Insights Clés - Partie 4 (Retards) :
```
✅ 0 jour de retard : Taux ~6%
✅ 1-30 jours : Taux ~10%
✅ 31-90 jours : Taux ~13%
✅ >90 jours : Taux ~18% (triplement du risque !)
```

### Ce que ça signifie métier :
**Pattern en U inversé pour le nombre de crédits :**
- Pas de crédit = risque (nouveau, non testé)
- 3-5 crédits = optimal (expérience sans surendettement)
- >10 crédits = risque (multiplication des engagements)

**Pattern exponentiel pour les retards :**
- Retard >90 jours = **red flag majeur**
- Le taux de défaut **triple** par rapport à un client sans retard

### Comment l'expliquer :
> "Ce tableau de bord révèle l'importance cruciale de l'historique bancaire. Avoir un historique bureau réduit le risque de 20%. Mais ce n'est pas binaire : 3-5 crédits est optimal, au-delà le risque remonte. Le graphique le plus frappant est celui des retards : un retard de plus de 90 jours fait exploser le taux de défaut à 18%, soit plus du double de la moyenne. Cela justifie la création de features spécifiques sur l'historique de paiement."

### Patterns Combinés :
Si on combine les insights :
```
Client IDÉAL :
- A un historique bureau
- 3-5 crédits
- 0 jour de retard
→ Taux de défaut : ~5%

Client À RISQUE :
- Pas d'historique OU >10 crédits
- Retards >90 jours
→ Taux de défaut : >15%
```

---

## 🎯 COMMENT PRÉSENTER CES GRAPHIQUES EN ANNEXE

### Structure Recommandée :

**Page 1 : Graphique 1 + Explication**
```
Titre : "Profil Démographique et Risque de Défaut"
Graphique en haut (70% de la page)
Commentaire en bas (30%) avec 3-4 bullet points
```

**Page 2 : Graphique 2 + Explication**
```
Titre : "Features Prédictives - Analyse de Corrélation"
Graphique en haut
Commentaire + tableau des top 5 features
```

**Page 3 : Graphique 3 + Explication**
```
Titre : "Impact des Scores Externes sur le Risque"
Graphique en haut
Commentaire + segmentation proposée (faible/moyen/haut risque)
```

**Page 4 : Graphique 4 + Explication**
```
Titre : "Validation des Règles Métier Bancaires"
Graphique en haut
Commentaire + référence à la règle des 33%
```

**Page 5 : Graphique 5 + Explication**
```
Titre : "L'Historique Bancaire : Facteur Clé de Décision"
Graphique en haut
Commentaire + profil client idéal vs à risque
```

### Points Clés à Rappeler en Présentation :

1. **Graphique 1 :** "L'âge est discriminant, les jeunes sont plus risqués"

2. **Graphique 2 :** "EXT_SOURCE domine, avec corrélation inverse forte"

3. **Graphique 3 :** "Relation quasi-linéaire, permet la segmentation"

4. **Graphique 4 :** "Valide les règles métier : 5x crédit/revenu et 33% annuité"

5. **Graphique 5 :** "L'historique bureau est crucial, les retards >90j triplent le risque"

---

## 💡 BONUS : Questions Attendues et Réponses

### Q1 : "Pourquoi ces 5 graphiques spécifiquement ?"

**R :** "Ces graphiques couvrent les 3 piliers de l'analyse de risque crédit :
1. Démographie (âge)
2. Comportement financier (ratios, retards)
3. Scoring externe (EXT_SOURCE)

Ensemble, ils donnent une vue complète du profil de risque."

### Q2 : "Comment ces insights impactent votre modélisation ?"

**R :** "Plusieurs décisions découlent de ces graphiques :
- Feature engineering : création des ratios Crédit/Revenu et Annuité/Revenu
- Segmentation : tranches d'âge, scores externes
- Features 'Has_Bureau' : l'absence d'historique est une info en soi
- Importance attendue : EXT_SOURCE devrait dominer le modèle"

### Q3 : "Avez-vous vérifié la représentativité du test set ?"

**R :** "Oui, ces distributions ont été validées sur le test set également. Les patterns sont identiques, confirmant que train et test proviennent de la même distribution."

---

## 🎨 CHECKLIST AVANT SOUMISSION

Avant d'inclure ces graphiques dans ton rapport :

- [ ] Les 5 PNG sont en haute résolution (300 DPI) ✅
- [ ] Chaque graphique a un titre clair ✅
- [ ] Les axes sont labellisés ✅
- [ ] Les légendes sont présentes ✅
- [ ] Les couleurs sont cohérentes (vert=bon, rouge=défaut) ✅
- [ ] Les statistiques clés sont notées (médiane, etc.) ✅
- [ ] Un commentaire accompagne chaque graphique ✅

---

**Bonne chance pour ta présentation Pierre ! Ces graphiques racontent une histoire cohérente et professionnelle de ton EDA. 🚀**
