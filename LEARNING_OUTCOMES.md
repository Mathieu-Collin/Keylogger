#  Keylogger — Points d’Apprentissage et Compétences Développées

##  Objectif du Projet

Ce projet a été réalisé dans un but **strictement éducatif et éthique**, dans le cadre d’un **portfolio en cybersécurité**.  
L’objectif principal était de comprendre **le fonctionnement interne d’un keylogger**, ses **mécanismes de capture des entrées clavier**, ainsi que les **mesures de défense** permettant de s’en prémunir.

---

##  Compétences Techniques Développées

###  Programmation et Architecture Logicielle
- Conception d’un programme capable d’interagir avec le système d’exploitation à bas niveau.  
- Manipulation des **API système Windows** (ex. : `GetAsyncKeyState`, `SetWindowsHookEx`) pour intercepter des événements clavier.  
- Gestion des fichiers et des logs (ou flux de sortie sécurisés).  
- Application de bonnes pratiques de structuration du code et d’isolation des responsabilités.

###  Sécurité Offensive (Ethical Hacking)
- Compréhension du **fonctionnement des keyloggers** utilisés dans les attaques réelles.  
- Étude des **techniques de persistance** et de **furtivité**, ainsi que des moyens de **détection** et de **prévention** (antivirus, EDR, sandboxing, monitoring des hooks système).  
- Mise en pratique dans un environnement de test isolé (machine virtuelle, sandbox).

###  Sécurité Défensive (Blue Team)
- Analyse comportementale d’un keylogger : indicateurs de compromission (IoC), processus suspects, modifications du registre, création de fichiers cachés, etc.  
- Identification des **signatures possibles** utilisées par les solutions de sécurité.  
- Élaboration de **contre-mesures** et stratégies de mitigation.

###  Conformité, Éthique et Légal
- Sensibilisation aux **limites légales** de l’expérimentation en cybersécurité.  
- Respect des principes du **Responsible Disclosure** et de l’usage **éthique** des outils d’analyse.  
- Documentation claire visant à **former et informer**, non à nuire.

---

##  Points Clés d’Apprentissage

1. **Comprendre pour mieux se défendre** : maîtriser la logique d’un keylogger permet de développer des outils et stratégies de détection plus efficaces.  
2. **Travailler en environnement contrôlé** : importance des machines virtuelles, des sandbox et de l’isolation réseau pour les tests de sécurité.  
3. **Analyser les comportements système** : observation des processus, gestion des événements clavier et interactions avec le système de fichiers.  
4. **Écrire un code responsable** : documenter, cloisonner et rendre les intentions du projet transparentes.

---

##  Environnement et Outils Utilisés

- **Langage** : Python (ou C/C++ selon ton implémentation)  
- **OS** : Windows (avec possibilité d’adaptation à Linux/macOS)
- **Gestion de version** : Git / GitHub  

---

##  Conclusion

Ce projet m’a permis de développer une compréhension approfondie des **techniques d’interception clavier**, mais surtout des **moyens de détection et de prévention** nécessaires pour s’en protéger.  
Il illustre une démarche d’apprentissage **responsable, analytique et défensive**, indispensable dans tout parcours en **cybersécurité**.

---

>  **Disclaimer :**  
> Ce code est destiné exclusivement à des fins éducatives et de recherche.  
> L’usage de ce type d’outil sur une machine ou un réseau sans consentement explicite est **illégal** et **puni par la loi**.
