import re
import time
from unittest import case
from itertools import groupby
from operator import itemgetter

import iterutils as iterutils
from boltons import iterutils
import numpy
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import pytest
from pandas.tests.io.test_pickle import compare

tableau_noeuds = []
tableau_relations = []


import re
from bs4 import BeautifulSoup
import requests
import os
import sys
import pickle

# Prend le mot recherché et retourne la categorie gramaticale corespendante au mot, grace au  code html correspondant depuis http://www.jeuxdemots.org/rezo-dump et on prendant pour l'instant la relation r_pos telque son poid avec le noeud du mot recercher est maximale.

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
            id.append(tableau_relations[i])
        i += 1
    #print("id:::", id)

    # on a remarqué que le maximum était en dernier (i.e les relations sont triés dans l'ordre croirssant) mais comme on n'est pas sur
    # on a preferer le calculé.
    categorie = []
    for N in tableau_noeuds:

        if (int(N[1]) in id):
            categorie.append(N[2]);


    if cache:
        chemin_absolu = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(chemin_absolu + '/cache'):
            try:
                os.mkdir(chemin_absolu + '/cache')
            except OSError:
                print('La création du dossier cache a échoué')

        fichier_cache = open(chemin_absolu + '/cache/' + word + '.pkl', 'wb')
        pickle.dump([categorie,tableau_noeuds, id], fichier_cache)
        fichier_cache.close()
        pos_unique(id,tableau_noeuds)
        #print("cat : ",categorie)

    tableau_noeuds.clear()
    tableau_relations.clear()
    #return categorie
    return "############"



def extraction_cache(word: str, cache: bool):
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if not cache:
        return extraction(word, cache)
    elif cache and (not os.path.isdir(chemin_absolu + '/cache') or not os.path.isfile(
            chemin_absolu + '/cache/' + word + '.pkl')):
        return extraction(word, cache)
    elif cache:
        fichier = open(chemin_absolu + '/cache/' + word + '.pkl', 'rb')
        categorie = pickle.load(fichier)
        fichier.close()
        pos_unique(categorie[2], categorie[1])

       # mot = categorie[1][0][2].strip("''")
        #print(mot)  # affiche le mot dans le tableau categorie
        #return categorie
    return "##############"


def analyse(phrase: str, cache: bool):
    words = phrase.split(" ");
    for word in words:
        if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
            print(word[:-1] + "  :: ")
            print(extraction_cache(str(word[:-1]), cache))
            print(word[len(word) - 1] + "  :: ")
            print(extraction_cache(str(word[len(word) - 1]), cache))
        else:
            print(word + "  :: ")
            print(extraction_cache(str(word), cache));





def analysePOSunique(phrase: str):
    words = phrase.split(" ");
    for word in words:
        if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
            print(word[:-1] + "  :: " + extraction(str(word[:-1])))
            print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
        else:
            print(word + "  :: " + extraction(str(word)));
        # print(extraction(str(word)))


def pos_unique(tableau_relations,tableau_noeuds):


    tabPOS = ["146889", "171869", "150504", "147628", "171870", "146911", "147826", "212235"]
    #Ce tableau contient les eid pour adverbe 146889 / adjectif qualificatif 171869 / conjonction de coordination, conjonction de subordination 150504
    # déterminant, 147628
    # nom commun, nom propre, 171870
    # préposition, 146911
    #pronom, 147826
    # verbe. 212235
    #Cela va nous permettre de comparer les eid du tabPos et ceux du tableau_relation afin de déterminer si
    #c'est un pos unique (on ne rencontre qu'un seul elem du tabPOS ou multiple dans le cas contraire


    tableau_relations.sort(key=itemgetter(2)) #ici on tri le tableau_relation  de sorte à ne garder
    #que les relations liées à un même mot
    groups = groupby(tableau_relations, itemgetter(2)) #une fois séparée on les groupe par mot
    tb = [[item for item in data] for (key, data) in
          groups]  # sépare les différents id (chaque mot) pour avoir un tableau de pos par mot

    words = phrase.split(" ");

    tabmot = []
    tabmot_posmultiple=[]
    tabRes = []
    moment = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())
    myResFile = open("results/myresult"+moment+".txt", 'a')
    mot = tableau_noeuds[0][2].strip("''")  # recup le mot concerné
    for elem in range(len(tableau_noeuds)):  #cette boucle permet de garder seulement le tab de tab_noeud contenant le mot
        # print(tableau_noeuds[elem])
        found = re.search(r":", tableau_noeuds[elem][2])  # PERMET DE NE GARDER QUE LA LIGNE DE TABNOEUDS AVEC LE MOT
        if not found:
            tabmot.append(tableau_noeuds[elem])


    for elem in tb: #on va compter le nb de fois où on rencontre un elem de tb qui est dans tabPOS
        countPOS = 0
        for i in range(len(elem)):
            if elem[i][3] in tabPOS:  # On compte le nb de fois où un des elem de tabPOS est présent dans les eid des pos du mot
                countPOS += 1

        if countPOS == 1:
            str = "POS_UNIQUE  "

            #print(tableau_relations[len(tableau_relations)-1])#affiche le poids le plus haut du tab rel (le dernier sous tab)
            val_Poids_Rel_Haut = tableau_relations[len(tableau_relations) - 1][5] #poids le plus haut
            #print("poids le plus haut :",val_Poids_Rel_Haut)
            num_Tag_Poids_Haut = tableau_relations[len(tableau_relations) - 1][3]#Valeur du tag du poids le plus haut
            #print("ref tag :", num_Tag_Poids_Haut)

            for x in range(len(tableau_noeuds)):
                if tableau_noeuds[x][1] == num_Tag_Poids_Haut :
                    res_pos_mot = tableau_noeuds[x][2].strip("''")
                    print(res_pos_mot) #TAG du mot
            myResFile.write(mot +" :: "+ res_pos_mot + " ; ")


        if countPOS > 1:

            str = "POS_MULTIPLE "
            myResFile.write(mot +" :: "+ str + " ; ")

        print(str)

    myResFile.close()




def pos_multiple():

   # print("@@@@@@ myresult(moment).txt @@@@@@ fonction pos multiple")
    moment = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())
    openFile = open("results/myresult"+moment+".txt", "r")
    readFile = openFile.read()
    myFile = readFile.split(";")

    firtSublist = iterutils.chunked(myFile, 1)

    #print(len(firtSublist))
    final = []
    for i in range(len(firtSublist)):
        secondsublist = firtSublist[i][0].split("::")

        final.append(secondsublist)
   # print("final :", final)

   # print("myfile : ",myFile)
    #print(myFile[0].split(" ") + myFile[1].split(" ") )

    openFile.close()
    sequence_valide(final)

def sequence_valide(final):
    #print("------seqvalide()------")
   # print("final seq valide ",final)
    #print("final0:",final[0])
    openSeq = open("sequences/sequences_valides", "r")
    readSeq = openSeq.read()
    #readSeq.split('\n')
    #print("readseq:\n",readSeq)

    splitSeq =readSeq.split("\n")
    #print("split ", splitSeq)
    #print("split1 : ", splitSeq[0])
    #print(len(splitSeq))
    sublistSplitFinal = []
    for i in range(len(splitSeq)):
        sublistSplitFinal.append(splitSeq[i].split(";"))
    #print("sublistfinal : " ,sublistSplitFinal)


#### ON PASSE AU CHOSES SERIEUSES ####
## BOUCLE POUR COMPARER LE POS DE LA PHRASE ET CEUX DES SEQ VALIDES ##
    print("@@@@@@@@@@ RESULTAT FINAL @@@@@@@@@@")

    for x in range(len(final) - 1):

        for i in range(len(sublistSplitFinal)):

            if (final[x][1].strip(" ")) == sublistSplitFinal[i][x].strip(" "):  # on enleve les espaces pour etre sûr d'avoir que les caractère
                print("SEQUENCE OK : ", final[x][0].strip(" ") ,final[x][1].strip(" "), " ; ", sublistSplitFinal[i][x].strip(" "))
                break
            if final[x][1].strip(" ") == "POS_MULTIPLE":
                print("POSMULTIPLE : ", final[x][0].strip(" ") ,final[x][1].strip(" "))
                #ici il faudrait appeler la fonction qui recup le mot et retourne son POS
                propableTag(final[x][0].strip(" "))

                break



def propableTag(motposmultiple):

    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    readPkl = pd.read_pickle(chemin_absolu+'/cache/'+motposmultiple+'.pkl')
    #print(readPkl) #[0] = vide / [1] = tabnoeud / [2] = tabRel
    #print(readPkl[2])
    num_Tag_Poids_Haut = readPkl[2][len(readPkl[2]) - 1][3]  # Valeur du tag du poids le plus haut
    num_Tag_2ndPoids_Haut = readPkl[2][len(readPkl[2]) - 2][3]# valeur du 2nd tag de poids le plus haut

    #parfois le tag à n-2 de la fin du tab relation est plus précis
    #que le tag à n-1, (ex: à n-1 on à Nom: et à n-2 on a Nom:Fem+SG)
    #donc on va vérifier que c'est possible
    #d'attribuer le tag à n-2 si il est lié à celui du n-1 sinon on garde n-&

    for x in reversed(range(len(readPkl[1]))): #on reverse pour commencer du poids le plus haut

        if readPkl[1][x][1] == num_Tag_Poids_Haut:
            res_pos_mot1 = readPkl[1][x][2].strip("''")
           # print("1",res_pos_mot1)  # TAG du mot

        if readPkl[1][x][1] == num_Tag_2ndPoids_Haut:
            res_pos_mot2 = readPkl[1][x][2].strip("''")

             #print("2",res_pos_mot2)  # TAG du mot
            if res_pos_mot1 in res_pos_mot2 :
                print(res_pos_mot2)
            else:
                print(res_pos_mot1)







#####  MAIN  #####
phrase = input("Entrez la phrase: \n")
cache = input("voulez vous utiliser le cache ? ('T' or 'F'?) \n")
if (cache == 'T'):
    analyse(phrase, True);
elif (cache == 'F'):
    analyse(phrase, False);
else:
    print("only:  T for 'true' or F for 'false'");
    exit();
pos_multiple()
#pos_multiple()




