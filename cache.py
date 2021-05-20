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

# Prend le  mot recherché et retourne la categorie gramaticale corespendante au mot, grace au  code html correspondant depuis http://www.jeuxdemots.org/rezo-dump et on prendant pour l'instant la relation r_pos telque son poid avec le noeud du mot recercher est maximale.

tableau_noeuds = []
tableau_relations = []


def extraction(word: str, cache: bool):

    html = requests.get('http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel=4')
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    #print("txt ", texte_brut)


    noeuds = re.findall('[e];[0-9]*;.*', str(texte_brut))
    #print(" noeuds " ,noeuds)

    relations = re.findall('[r];[0-9]*;.*', str(texte_brut))
    # print("rel " , relations)
    # print("word " ,word)
    if ((not noeuds) and (not relations)) :
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
    print("id:::", id)

    # on a remarqué que le maximum était en dernier (i.e les relations sont triés dans l'ordre croirssant) mais comme on n'est pas sur
    # on a preferer le calculé.
    categorie = []
    for N in tableau_noeuds:

        if (int(N[1]) in id):
            categorie.append(N[2]);

    print("word", word)
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
        if (word[len(word) - 1] in ['.', '!', ':', '?', ';']):
            print(word[:-1] + "  :: ")

            print(extraction_cache(str(word[:-1]), cache))
            print(word[len(word) - 1] + "  :: ")
            print(extraction_cache(str(word[len(word) - 1]), cache))
        else:
            print(word + "  :: ")
            print(extraction_cache(str(word), cache));



#
#
# def analysePOSunique(phrase: str):
#     words = phrase.split(" ");
#     for word in words:
#         if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
#
#             print(word[:-1] + "  :: " + extraction(str(word[:-1])))
#             print(word[len(word) - 1] + "  :: " + extraction(str(word[len(word) - 1])))
#         else:
#             print(word + "  :: " + extraction(str(word)));
#         # print(extraction(str(word)))


def pos_unique(tableau_relations,tableau_noeuds):


    tabPOS = ["146889", "171869", "150504", "147628", "171870", "146911", "147826", "212235", "2354314"]
    #Ce tableau contient les eid pour adverbe 146889 / adjectif qualificatif 171869 / conjonction de coordination, conjonction de subordination 150504
    # déterminant, 147628
    # nom commun, nom propre, 171870
    # préposition, 146911
    #pronom, 147826
    # verbe. 212235
    # ponctuation : 2354314
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

    res_pos_mot= []
    for elem in tb: #on va compter le nb de fois où on rencontre un elem de tb qui est dans tabPOS
        countPOS = 0
        for i in range(len(elem)):
            if elem[i][3] in tabPOS:  # On compte le nb de fois où un des elem de tabPOS est présent dans les eid des pos du mot
                countPOS += 1


        if countPOS == 1:
            str = "POS_UNIQUE  "
            for x in range(len(tableau_noeuds)):
                res_pos_mot.append(tableau_noeuds[x][2].strip("''"))
            print(res_pos_mot) #TAG du mot



            myResFile.write(res_pos_mot[0] + " :: ")
            for i in range(1,len(res_pos_mot)):
                myResFile.write(res_pos_mot[i] + " , ")
            myResFile.write(" ; \n")




        if countPOS > 1:

            str = "POS_MULTIPLE "
            #myResFile.write(mot +" :: "+ str + " ; ")
           # myResFile.write("\n")
            for x in range(len(tableau_noeuds)):

                res_pos_mot.append(tableau_noeuds[x][2].strip("''"))
            print(res_pos_mot) #TAG du mot
            #print(res_pos_mot[1])# affiche le premier pos car 0 = le mot
            #for mot in res_pos_mot:
            #myResFile.write(mot + " ::")
            myResFile.write(res_pos_mot[0] + " :: " )
            for i in range(1,len(res_pos_mot)):
                myResFile.write(res_pos_mot[i] + " , ")
            myResFile.write(" ; \n")

        print(str)
    myResFile.close()


def save_tags_mot():

   # print("@@@@@@ myresult(moment).txt @@@@@@ fonction pos multiple")
    moment = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())
    openFile = open("results/myresult"+moment+".txt", "r")
    readFile = openFile.read()
    myFile = readFile.split(";")
    print("myfile  : ", myFile[0])


    final = []
    firtSublist = iterutils.chunked(myFile, 1)
    print("frist", firtSublist)
    print(firtSublist[0][0])

    for i in range(len(firtSublist)):
        if "Punct:" in firtSublist[i][0]:
            print("il y a une ponct")
            print("here", firtSublist[i][0])
            #essayer de concatener , et Punct
            ts = firtSublist[i][0].split("::")
            print("ts", ts[1].split(","))
            fint = ts[1].split(",")
            print(fint[(len(fint) - 2)].strip(" "))
            final.append(fint[(len(fint) - 2)].strip(" "))

        else:
            secondsublist = firtSublist[i][0].split("::")
            final.append(secondsublist)



    print("SC :",final)

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

    print("@@@@@@@@@@ MES TABLEAUX @@@@@@@@@@")

    for i in range(len(sublistSplitFinal)):
        print(sublistSplitFinal[i])

    # test=[]
    # print(final)
    # print(final[0][0])
    # print(final[0][1].split(","))
    # test.append(final[0][0])
    # test.append(final[0][1].split(","))
    # print("test : ", test)
    # print(test[0])
    # print(test[1])

    wordAndTags = [] #variable qui va permette de stocker un mot et ensuite une liste de ses tag
    for x in range(len(final)-1): #boucle pour peupler la varible comme ceci : [mot1 , [listTagMot1] , mot2, [listTagMot2]...]
        wordAndTags.append(final[x][0])
        wordAndTags.append(final[x][1].split(","))
    sublistWord_tags = iterutils.chunked(wordAndTags, 2) #on découpe la liste pour avoir des sous liste contenant [mot, [listTag]]..
    # for x in range(len(sublistWord_tags)):
    #     for y in range(len(sublistWord_tags[x][1])):
    #         sb = sublistWord_tags[x][1][y].strip(" ")
    # print("sb : " ,sb)
    print("sublistWord_tags : ", sublistWord_tags)
    #print(mysplit[0])

    print("seq sublistSplitFinal : ",sublistSplitFinal) #liste des sequences du fichier seq valide

    #print(sublistWord_tags[0][1])
    #print(sublistSplitFinal[2][0])
    #print(sublistWord_tags[0][1][7].strip(" "))
    #print(len(sublistWord_tags[0][1]))
    print("\n @@@@@ RESULTAT FINAL @@@@@\n ")
    idxSeq = 0
    idxTag = 0
    incrTag = 0
    myListTags = []

    #print("len phrase : ", len(sublistWord_tags))
    for i in range(len(sublistSplitFinal)):
        for z in range(len(sublistWord_tags)):
            if len(sublistWord_tags) == (len(sublistSplitFinal[i])): #pour ne pas avoir d'erreur index out of range on ne traite que les seq de meme longeur que la phrase

                #check_valide(sublistSplitFinal, i, idxSeq+z, sublistWord_tags, idxTag+z, z)
                check_valide(sublistSplitFinal, i, idxSeq+z, sublistWord_tags, idxTag+z, z)
                #myListTags.append(ts[1])
                # print("z ", z)
                # print("idxSeq", idxSeq+z)
                # print("idxTag", idxTag+z)
                #check_valide(sublistSplitFinal, i, idxSeq+z, sublistWord_tags, idxTag+z, z  )

        #print("\n")



def check_valide(sublistSplitFinal, i , idxSeq,  sublistWord_tags,idxTag , z):
    myListTags = []
    isOK = False
    for x in range(len(sublistWord_tags[idxTag][1])):


        if sublistSplitFinal[i][idxSeq].strip(" ") == sublistWord_tags[idxTag][1][x].strip(" "):
            #print("OK", "seq " , z , " : ", sublistSplitFinal[i][idxSeq].strip(" "), " tag mot : ",
             #     sublistWord_tags[idxTag][1][x].strip(" "))
            #print(sublistSplitFinal[i])
            isOK = True

            if isOK == True and z == (len(sublistWord_tags)-1) and idxTag == (len(sublistWord_tags)-1) and idxSeq == (len(sublistWord_tags)-1) :
                print("Sequence valide : ")
                #print(sublistSplitFinal[i])
                myListTags.append(sublistSplitFinal[i])
                print(myListTags)

        #print(isOK)

            #myListTags.append(sublistWord_tags[idxTag][1][x].strip(" "))

    #print(" myListTags : ",myListTags)
    #return(sublistSplitFinal[i], myListTags)



# def propableTag(motposmultiple, place, seq):
#
#     chemin_absolu = os.path.dirname(os.path.abspath(__file__))
#     readPkl = pd.read_pickle(chemin_absolu+'/cache/'+motposmultiple+'.pkl')
#     #print(readPkl) #[0] = vide / [1] = tabnoeud / [2] = tabRel
#     #print(readPkl[2])
#     #num_Tag_Poids_Haut = readPkl[2][len(readPkl[2]) - 1][3]  # Valeur du tag du poids le plus haut
#     #num_Tag_2ndPoids_Haut = readPkl[2][len(readPkl[2]) - 2][3]# valeur du 2nd tag de poids le plus haut
#
#     #maintenant on doit parcourir le tableau de relation avec tous le pos positif
#     #afin de garder celui qui correspond à celui dans la sequence valide
#     #for i in (range(len(readPkl[2]))):
#     print("readpkl :", readPkl)
#     print(readPkl[1])
#     print(readPkl[2])
#     print(seq)
#     print(place)
#     estDansSeq = 0
#     for x in range(len(readPkl[1])):
#         for i in range(len(readPkl[2])):
#             #print("e :" ,readPkl[1][x][1].strip("''"))
#             #print(" r :",readPkl[2][i][3].strip("''"))
#             if readPkl[1][x][1].strip("''") == readPkl[2][i][3].strip("''"):
#
#                 #print("on est bon",readPkl[1][x][2].strip("''") )
#                 for z in range(len(seq)):
#                     #print("z",seq[z][place])
#                     if readPkl[1][x][2].strip("''") == seq[z][place].strip(" "):
#                         estDansSeq=1
#                         print("sequence ok",readPkl[1][x][2].strip("''"),seq[z][place] )
#
#             #     if estDansSeq == 0 and z == (len(seq)-1):
#             #         print("pas de sequence valide pour cette phrase")
#             #         break
#             #     break
#             # break
#




#####  MAIN  #####
phrase = input("Entrez la phrase: \n")

analyse(phrase, True);


save_tags_mot()
#pos_multiple()




