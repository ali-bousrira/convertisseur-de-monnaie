import json
import sys
from forex_python.converter import CurrencyRates

c = CurrencyRates()

try :
    f = open ("nouv_devi.json", "r")
    f.close()
except:
    with open ("nouv_devi.json", "w") as f :
        json.dump({}, f)
    f.close()

#verification des types de saisie
def is_number(d):
    try:
        float(d)
        return True
    except ValueError:
        return False

#verification du saisie des nombre
def nb_input(x):
    n = input("{} : \n".format (x ))
    while  not is_number(n):
        n = input("{} : \n".format (x ))
    n = float(n)
    return n


#fonction pour crer une nouvel devise local
def crea_devi (devise):
    chois = input("vouler vous enregistre une nouvel devise pour {} : \n".format (devise))
    while not (chois == "oui" or chois == "non"):
        chois = input("vouler vous enregistre une nouvel devise pour {} : \n".format (devise))
    if chois == 'oui':
        taux = nb_input ("donner le taux de convertion de cette devise par raport au dollar americain")
        with open ("nouv_devi.json", "r") as f:
            devi_local = json.load (f)
        devi_local[devise] = taux
        with open ("nouv_devi.json", "w") as f:
            json.dump (devi_local, f)
    else:
        sys.exit ()

#sauvegarde des convertion
def sauv (val, devise1, result, devise2):
    chois = input ("voulez vous sauvegarder oui ou non : \n")
    while not (chois == "oui" or chois == "non"):
        chois = input ("voulez vous sauvegarder oui ou non : \n")
    if chois == "oui":
        with open ("historique.txt", "a") as f:
            f.write (str(val) + devise1 + " = " + str(result) + devise2)
            f.write("\n")

#fonction pour verifier est donner les valeur dune devise local
def verif (devise):
    result = False
    with open ("nouv_devi.json", "r") as f :
        verif = json.load(f)
    if devise in verif :
        result = True
    return result

#fonction de convertion de devise
def conv ():

    val = nb_input("donner la valeur a convertir")

    devise1 = input ("donner la devise a echanger : \n").upper()

    devise2 = input ("donner la deuxiem devise voulue : \n").upper()


    try :
        result = c.convert(devise1, devise2, val)

        print ( result)
        sauv (val, devise1, result, devise2)
    except:
        test_gl_1 = test_gl_2 = test_lc_1 = test_lc_2 = False
        try :
            c.get_rates(devise1)
            test_gl_1 = True
        except :
            if not verif (devise1):
                crea_devi (devise1)
            test_lc_1 = True
        try :
            c.get_rates(devise2)
            test_gl_2 = True
        except :
            if not verif (devise2) :
                crea_devi (devise2)
            test_lc_2 = True
        with open ("nouv_devi.json", "r") as f :
            val_lc = json.load (f)
            if (not test_gl_1) and (not test_lc_1) :
                crea_devi (devise1)
            if (not test_gl_2) and (not test_lc_2) :
                crea_devi (devise2)
            #si la desieme devise existe localement
            if test_lc_1 and test_gl_2:
                val_usd = val * val_lc [devise1]
                result = c.convert('USD', devise2, val_usd)
                print (result)
                sauv (val, devise1, result, devise2)
            if test_lc_2 and test_gl_1 :
                val_usd = c.convert(devise1,"USD",val)
                result = val_usd * val_lc [devise2]
                print (result)
                sauv (val, devise1, result, devise2)

            if test_lc_2 and test_lc_1 :
                val_usd = val * val_lc [devise1]
                result = val_usd * val_lc [devise2]
                print (result)
                sauv (val, devise1, result, devise2)


conv ()
