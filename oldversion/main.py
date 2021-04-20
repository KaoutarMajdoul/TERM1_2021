import re
from unittest import case
from itertools import groupby
from operator import itemgetter
from bs4 import BeautifulSoup
import requests
import pickle
import os


tableau_noeuds = []
tableau_relations = []


def extraction(word: str, cache: bool):
    html = requests.get('http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel=4')
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    noeuds = re.findall('[e];[0-9]*;.*', str(texte_brut))
    relations = re.findall('[r];[0-9]*;.*', str(texte_brut))
    if ((not noeuds) and (not relations)):
        print("le mot " + word + " n'existe pas dans jeux de mots")
        return None

    # print(texte_brut)

    for noeud in noeuds:
        tableau_noeuds.append(noeud.split(';'))
    for relation in relations:
        tableau_relations.append(relation.split(';'))

    id = []
    i = 0
    while i <= len(tableau_relations) - 1:
        if (int(tableau_relations[i][5]) >= 0):
            id.append(int(tableau_relations[i][3]))
        i += 1

    # on a remarqué que le maximum était en dernier (i.e les relations sont triés dans l'ordre croirssant) mais comme on n'est pas sur
    # on a preferé le calculer.
    categorie = []
    cat = []
    c=[]
    for N in tableau_noeuds:

        if (int(N[1]) in id):
            cat+=N[2];

    categorie+=tableau_noeuds
    c+=tableau_relations


    if cache:
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(chemin_absolu + '/cache'):
            try:
                os.mkdir(chemin_absolu + '/cache')
            except OSError:
                print('La création du dossier cache a échoué')

        fichier_cache = open(chemin_absolu + '/cache/' + word + '.pkl', 'wb')

        pickle.dump([categorie,c ], fichier_cache)
        fichier_cache.close()
    print("tabnoeu : ", tableau_noeuds)
    print("tabrel : ", tableau_relations)
    #print("ici categorie : ", categorie)
    #print("ici c : ", c)
    tableau_relations.clear()
    return categorie, c
    categorie.clear()
    c.clear()



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
        #pos_unique(categorie[1])

        print("tab rel : ", categorie[1])
        print("id mot : ", categorie[0][0][1])

        #print("tabnocategorie.clear()eu : ", tableau_noeuds)
        #print("tabrel : ", tableau_relations)

        return categorie
        categorie.clear()

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

def analysePOSunique(phrase: str):
    words = phrase.split(" ");
    for word in words:
        if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
           print(word[:-1] + "  :: " + extraction(str(word[:-1])))
           print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
        else:
           print(word + "  :: " + extraction(str(word)));
        #print(extraction(str(word)))



def pos_unique(tableau_relations):

    tabPOS = ["146889","171869","150504","147628","171870","146911","147826","212235"]
    tableau_relations.sort(key = itemgetter(2))
    groups = groupby(tableau_relations, itemgetter(2))

    tb =[[item for item in data] for (key, data) in groups] #sépare les différents id (chaque mot) pour avoir un tableau de pos par mot
    words = phrase.split(" ");

    tabmot = []
    for elem in range(len(tableau_noeuds)):
        #print(tableau_noeuds[elem])
        found = re.search(r":",tableau_noeuds[elem][2]) #PERMET DE NE GARDER QUE LA LIGNE DE TABNOEUDS AVEC LE MOT
        if not found :

            tabmot.append(tableau_noeuds[elem])


    for elem in tb :
        countPOS = 0
        for i in range(len(elem)) :

            #print(words[i])
            if elem[i][3] in tabPOS : #On compte le nb de fois où un des elem de tabPOS est présent dans les eid des pos du mot
                countPOS +=1
                #print(countPOS)
        #for x in range(len(words)):
            if countPOS == 1 :
                str = "POS UNIQUE : "

            elif countPOS > 1:
                str = "POS MULTIPLE :"

        print(str)
        #print("essayer d'afficher le mot")


phrase = input("Entrez la phrase: \n")
analyse(phrase,True);

#pos_unique(tableau_relations);





