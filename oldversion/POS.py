import re
from bs4 import BeautifulSoup
import requests
import os
import sys
import pickle

# Prend le  mot recherché et retourne la categorie gramaticale corespendante au mot, grace au  code html correspondant depuis http://www.jeuxdemots.org/rezo-dump et on prendant pour l'instant la relation r_pos telque son poid avec le noeud du mot recercher est maximale.

tableau_noeuds=[]
tableau_relations=[]

def extraction(word: str,cache:bool):
    html = requests.get('http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel=4')
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    noeuds=re.findall('[e];[0-9]*;.*', str(texte_brut))
    relations=re.findall('[r];[0-9]*;.*', str(texte_brut))
    if ((not noeuds) and (not relations)) :
        print("le mot "+word+" n'existe pas dans jeux de mots")
        return None

    #print(texte_brut)


    
    for noeud in noeuds:
        tableau_noeuds.append(noeud.split(';'))
    for relation in relations:
        tableau_relations.append(relation.split(';'))
        
    id=[]
    i=0
    while i<=len(tableau_relations)-1:
        if(int(tableau_relations[i][5])>=0):
            id.append(int(tableau_relations[i][3]))
        i+=1
            
    # on a remarqué que le maximum était en dernier (i.e les relations sont triés dans l'ordre croirssant) mais comme on n'est pas sur
    # on a preferer le calculé.
    categorie=[]
    for N in tableau_noeuds:
      
        if(int(N[1]) in id):
            categorie.append(N[2]);
    tableau_noeuds.clear()
    tableau_relations.clear()

    if cache:
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(chemin_absolu + '/cache'):
            try:
                os.mkdir(chemin_absolu + '/cache')
            except OSError:
                print('La création du dossier cache a échoué')

        fichier_cache = open(chemin_absolu + '/cache/' + word +'.pkl','wb')
        pickle.dump(categorie, fichier_cache)
        fichier_cache.close()
        
    return categorie


def extraction_cache(word:str,cache:bool):
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if not cache:
        return extraction(word,cache)
    elif cache and (not os.path.isdir(chemin_absolu + '/cache') or not os.path.isfile(chemin_absolu + '/cache/' +word+ '.pkl')):
        return extraction(word, cache)
    elif cache:
        fichier = open(chemin_absolu + '/cache/' + word + '.pkl', 'rb')
        categorie = pickle.load(fichier)
        fichier.close()
        return categorie
    
def analyse(phrase: str,cache:bool):
    words=phrase.split(" ");
    for word in words:
        if (word[len(word)-1] in ['.',',','!',':','?',';']):
            print(word[:-1]+"  :: ")
            print(extraction_cache(str(word[:-1]),cache))
            print(word[len(word)-1]+"  :: ")
            print(extraction_cache(str(word[len(word)-1]),cache))
        else:
            print(word+"  :: ")
            print(extraction_cache(str(word),cache));


phrase=input("Entrez la phrase: \n")
cache=input("voulez vous utiliser le cache ? ('T' or 'F'?) \n")
if(cache=='T'):
    analyse(phrase,True);
elif (cache=='F'):
    analyse(phrase,False);
else:
    print("only:  T for 'true' or F for 'false'");
    exit();
