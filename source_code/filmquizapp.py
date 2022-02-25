import pickle
import sys
import regex
from random import choice, shuffle
from menudownload import *
import requests
from bs4 import BeautifulSoup
from einfuehrung import *
from CLASS_SUPERDICT2 import *






def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))


def read_pkl(filename):
    with open(filename, 'rb') as f:
        data_pickle = pickle.load(f)
    return data_pickle


def flatten_iter(iterable):
    def iter_flatten(iterable):
        it = iter(iterable)
        for e in it:
            if isinstance(e, list):
                for f in iter_flatten(e):
                    yield f
            else:
                yield e

    a = [i if not isinstance(i, (str, int, float)) else [i] for i in iter_flatten(iterable)]
    a = [i for i in iter_flatten(a)]
    return a


def delete_duplicates_from_nested_list(nestedlist):
    tempstringlist = {}
    for ergi in nestedlist:
        tempstringlist[str(ergi)] = ergi
    endliste = [tempstringlist[key] for key in tempstringlist.keys()]
    return endliste.copy()


def convert_dict(tup, di):
    di = dict(tup)
    return di


def richtig(leerzeichen=5):
    global userpunkte
    global gesamtpunkte
    gesamtpunkte = gesamtpunkte + 1
    userpunkte = userpunkte + 1
    print(drucker.f.black.brightgreen.bold(
        f'\nDeine Antwort ist richtig!\nErreichte Punkte:\t\t{userpunkte}\nMaximale Punktanzahl:\t\t{gesamtpunkte}\n'))
    print('\n' * leerzeichen)


def falsch(richtigeantwort, leerzeichen=5):
    global userpunkte
    global gesamtpunkte
    gesamtpunkte = gesamtpunkte + 1
    print(drucker.f.black.brightred.bold(f'\nDeine Antwort ist falsch! Die richtige Antwort ist: {richtigeantwort}\nErreichte Punkte:\t\t') +   drucker.f.black.brightred.negative(
        f'  {userpunkte}  ') + drucker.f.black.brightred.bold(f'\nMaximale Punktanzahl:\t\t') + drucker.f.black.brightred.negative(
        f'  {gesamtpunkte}  ') + drucker.f.black.brightred.bold(f'\n'))
    print('\n' * leerzeichen)


def bildspeichern(url, speichern):

    try:
        endung = url.split('.')[-1]
        speichern = speichern + '.' + endung
    except:
        pass
    with open(speichern, "wb") as f:
        f.write(requests.get(url).content)
    return speichern

def bildspeichern_neu(url):

    linkrequests = requests.get(url)
    suppe = BeautifulSoup(linkrequests.content, 'html.parser')
    for ini,img in enumerate(suppe.find_all('img')):
        bild = bildspeichern(url=img.__dict__['attrs']['src'], speichern='tempxxxbildxxx')
        print(drucker.p_picture_to_ascii_art(bild, letter_for_ascii_art='█',desired_width=50, rgb8_16_256=256))
        if ini==0:
            return True
    #
    # with open(speichern, "wb") as f:
    #     f.write(requests.get(url).content)
    # return speichern

def get_number_from_user(satzdrucken, farbe="brightyellow"):
    anfang = ""
    while not isinstance(anfang, int):
        try:
            anfang = input(drucker.f.black[farbe].italic(satzdrucken))
            anfang = int(anfang)
        except:
            print(
                drucker.f.black.brightred.italic(
                    "\nEingabe konnte nicht verstanden werden!\n"
                )
            )
    return anfang
datenbank = read_pkl(get_file_path(datei='dictallefilme.pkl')[0])
shuffle(datenbank)
gesamtpunkte = 0
userpunkte = 0
einfuehrung('Kinoquiz')
anzahlaufgaben = get_number_from_user(
    satzdrucken="\nWie viele Aufgaben sollen erstellt werden?\n",
    farbe="brightgreen",
)
for key, item in datenbank.items():

    try:
        deutschewoerter = delete_duplicates_from_nested_list(flatten_iter(item['de']))
        linkimdb = delete_duplicates_from_nested_list(flatten_iter(item['link']))[0]
        deutschertitel = delete_duplicates_from_nested_list(flatten_iter(item['de_titel']))[0]
        portugiesischertitel = delete_duplicates_from_nested_list(flatten_iter(item['pt_titel']))[0]
        dictionary = {}
        alsdict = convert_dict(deutschewoerter, dictionary)
        falschertitel0 = deutschertitel
        falschertitel1 = deutschertitel
        falschertitel2 = deutschertitel
        falschertitel3 = deutschertitel
        allefalschenantworten = []
        varianten = regex.findall(r'\b\w+\b', deutschertitel)
        for ini, vari in enumerate(varianten):
            try:
                suchwoerter = choice(alsdict[vari])
                if ini == 0:
                    falschertitel0 = falschertitel0.replace(vari, suchwoerter)
                    allefalschenantworten.append(falschertitel0)
                if ini == 1:
                    falschertitel1 = falschertitel1.replace(vari, suchwoerter)
                    allefalschenantworten.append(falschertitel1)
                if ini == 2:
                    falschertitel2 = falschertitel2.replace(vari, suchwoerter)
                    allefalschenantworten.append(falschertitel2)
                if ini == 3:
                    falschertitel3 = falschertitel3.replace(vari, suchwoerter)
                    allefalschenantworten.append(falschertitel3)
            except:
                pass
        allefalschenantworten = delete_duplicates_from_nested_list(allefalschenantworten)
        allefalschenantworten = [x for x in allefalschenantworten if x != deutschertitel]
        allefalschenantworten = [('f', x) for x in allefalschenantworten if len(x) > 1]
        if not any(allefalschenantworten):
            continue
        allefalschenantworten.append(('r', deutschertitel))
        shuffle(allefalschenantworten)
        try:
            bildspeichern_neu(url=linkimdb)
        except Exception as Fehler:
            print(Fehler)
            pass
        print(drucker.f.green.brightyellow.bold(f'\n{portugiesischertitel}\n'))
        optionendrucker = [x[1] for x in allefalschenantworten]

        ant1 = auswahlmenu_erstellen(optionen=optionendrucker, uberschrift='\nWie heißt der Film auf Deutsch?\n',
                                     color='brightyellow', unterdemtext='Deine Antwort: ')
        if allefalschenantworten[int(ant1)-1][0] == 'r':
            richtig()
        elif allefalschenantworten[int(ant1)-1][0] == 'f':
            falsch(richtigeantwort=deutschertitel)
        if gesamtpunkte == anzahlaufgaben:
            break
        print(10*'\n')


    except Exception as Fehler:
        print(Fehler)
        continue

print(
    drucker.f.black.brightyellow.italic("\nDu hast ")
    + drucker.f.brightyellow.black.italic(f"     {userpunkte}     ")
    + drucker.f.black.brightyellow.italic(" von insgesamt ")
    + drucker.f.brightyellow.black.italic(f"     {gesamtpunkte}     ")
    + drucker.f.black.brightyellow.italic(" erreicht\n")
)