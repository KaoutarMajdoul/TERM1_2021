import re
from unittest import case
from itertools import groupby
from operator import itemgetter
from bs4 import BeautifulSoup
import requests


tableau_noeuds = []
tableau_relations = []


def extraction(word: str):
    html = requests.get('http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel=4')
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    noeuds = re.findall('[e];[0-9]*;.*', str(texte_brut))
    relations = re.findall('[r];[0-9]*;.*', str(texte_brut))
    if ((not noeuds) and (not relations)):
        print("le mot " + word + " n'existe pas dans jeux de mots")
        return None
    #print(texte_brut) #affiche la sortie de chaque mot
    for noeud in noeuds:
        tableau_noeuds.append(noeud.split(';'))
    for relation in relations:
        tableau_relations.append(relation.split(';'))
    max = int(tableau_relations[0][5])
    id = int(tableau_relations[0][3])
    i = 0
    while i < len(tableau_relations) - 1:
        i += 1
        if (int(tableau_relations[i][5]) > max):
            id = int(tableau_relations[i][3])
            max = int(tableau_relations[i][5])

    for N in tableau_noeuds:

        if (int(N[1]) == id):
            categorie = N[2];
    #print(tableau_noeuds)
    #print(tableau_relations)
    #tableau_noeuds.clear()
    pos_unique(tableau_relations)
    tableau_relations.clear()
    return categorie


def analyse(phrase: str):
    words = phrase.split(" ");
    for word in words:
        if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
           # print(word[:-1] + "  :: " + extraction(str(word[:-1])))
           extraction(str(word[:-1]));
            #print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
           extraction(str(word[len(word) - 1]))
        else:
           # print(word + "  :: " + extraction(str(word)));
            extraction(str(word))
        #print(extraction(str(word)))

def analysePOSunique(phrase: str):
    words = phrase.split(" ");
    for word in words:
        if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
           print(word[:-1] + "  :: " + extraction(str(word[:-1])))
           print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
        else:
           print(word + "  :: " + extraction(str(word)));
        print(extraction(str(word)))



def pos_unique(tableau_relations):

    tabPOS = ["146889","171869","150504","147628","171870","146911","147826","212235"]
    #print(len(tableau_noeuds))
    #analysePOSunique(phrase)
    tableau_relations.sort(key = itemgetter(2))
    groups = groupby(tableau_relations, itemgetter(2))

    tb =[[item for item in data] for (key, data) in groups] #sépare les différents id (chaque mot) pour avoir un tableau de pos par mot
    #///////// ATTENTION :::::: CE GROUPEMENT N'AFFICHE QU'UNE FOIS LE RESULTAT MM SI LE MOT APPARAIT PLUSIEUR FOIS DANS LA PHRASE
    #////////   ex: La montagne et la rivière. : le mot "la" n'est traité qu'une fois \\\\\\\

    words = phrase.split(" ");

    print("tabnoeud", tableau_noeuds)
    #found = re.search(r":", tableau_noeuds)
    tabmot = []
    for elem in range(len(tableau_noeuds)):
        #print(tableau_noeuds[elem])
        found = re.search(r":",tableau_noeuds[elem][2]) #PERMET DE NE GARDER QUE LA LIGNE DE TABNOEUDS AVEC LE MOT
        if not found :
            #print("ok not found")
            print("tabnoeud mot: ",tableau_noeuds[elem])
            print("mot: ",tableau_noeuds[elem][2].strip("''"))
            tabmot.append(tableau_noeuds[elem])

    #print(tableau_noeuds[elem][2]) AFFICHE LE POS DU DERNIER MOT

    print(words)
   # for i in range(len(words)):
    #    analysePOSunique(words[i])
    for elem in tb :
        countPOS = 0
        #print("elem : ", elem)
        print("elem[2] : ", elem[0][2])
        #print("tabmot : ", tabmot)

        #for x in range(len(tabmot)):
            #print(tabmot[x])
            #print(tabmot[x][1])

            #if tabmot[x][1] == elem[x][2]:
             #   print("elem x OK : ", elem[x], tabmot[x])
              #  print("LE MOT EST : ", tabmot[x][2])
       # if elem[0][2] in tabmot[1].strip("''") :
            #print("OK")

        for i in range(len(elem)) :

            #print(words[i])
            if elem[i][3] in tabPOS :
                countPOS +=1
                #print(countPOS)
       # for x in range(len(words)):
            if countPOS == 1 :
                str = "POS UNIQUE "
                #print("LE MOT POS UNIQUE : ", tabmot[x][2].strip("''"))
                #param = tabmot[x][2].strip("''")


                #analysePOSunique(str(tabmot[x][2]))

            elif countPOS > 1:
                str = "POS MULTIPLE"

        print(str)
        #print("essayer d'afficher le mot")




phrase = input("Entrez la phrase: \n")
analysePOSunique(phrase);
#pos_unique(tableau_relations);





###############V2##################


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
            #categorie.append()
    #print(categorie)
    #print(tableau_relations)
    #tableau_noeuds.clear()
    #tableau_relations.clear()

    if cache:
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(chemin_absolu + '/cache'):
            try:
                os.mkdir(chemin_absolu + '/cache')
            except OSError:
                print('La création du dossier cache a échoué')

        fichier_cache = open(chemin_absolu + '/cache/' + word + '.pkl', 'wb')

        pickle.dump([categorie,c ], fichier_cache)
        #pickle.dump(c,fichier_cache)
        #print(tableau_relations)
        #pickle.load(categorie,fichier_cache)
        fichier_cache.close()

    return categorie, c


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
        pos_unique(categorie[1])
        return categorie[0]


# def analyse(phrase: str):
#     words = phrase.split(" ");
#     for word in words:
#         if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
#            print(word[:-1] + "  :: " + extraction(str(word[:-1])))
#            extraction(str(word[:-1]));
#            print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
#            extraction(str(word[len(word) - 1]))
#         else:
#             print(word + "  :: " + extraction(str(word)));
#             extraction(str(word))
#         #print(extraction(str(word)))


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
    #print(len(tableau_noeuds))
    #analysePOSunique(phrase)
    tableau_relations.sort(key = itemgetter(2))
    groups = groupby(tableau_relations, itemgetter(2))

    tb =[[item for item in data] for (key, data) in groups] #sépare les différents id (chaque mot) pour avoir un tableau de pos par mot


    words = phrase.split(" ");

    #print("tabnoeud", tableau_noeuds)
    #found = re.search(r":", tableau_noeuds)
    tabmot = []
    for elem in range(len(tableau_noeuds)):
        #print(tableau_noeuds[elem])
        found = re.search(r":",tableau_noeuds[elem][2]) #PERMET DE NE GARDER QUE LA LIGNE DE TABNOEUDS AVEC LE MOT
        if not found :
            #print("ok not found")
            #print("tabnoeud mot: ",tableau_noeuds[elem])
            #print("mot: ",tableau_noeuds[elem][2].strip("''"))
            tabmot.append(tableau_noeuds[elem])


    #print(words)

    for elem in tb :
        countPOS = 0
        #print("elem : ", elem)
        #print("elem[2] : ", elem[0][2])
        for i in range(len(elem)) :

            #print(words[i])
            if elem[i][3] in tabPOS : #On compte le nb de fois où un des elem de tabPOS est présent dans les eid des pos du mot
                countPOS +=1
                #print(countPOS)
        #for x in range(len(words)):
            if countPOS == 1 :
                str = "POS UNIQUE : "
                #print("LE MOT POS UNIQUE : ", tabmot[x][2].strip("''"))
                #param = tabmot[x][2].strip("''")
                #analysePOSunique(tabmot[x][2])

            elif countPOS > 1:
                str = "POS MULTIPLE :"

        print(str)
        #print("essayer d'afficher le mot")


phrase = input("Entrez la phrase: \n")
analyse(phrase,True);

#pos_unique(tableau_relations);





