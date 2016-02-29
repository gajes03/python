import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt
import StringIO
import numpy as np


root1 = ET.parse('pol_Country_en_xml_v2.xml').getroot()  # wczytanie i parsowanie pliku xml zawierajacego dane dla Polski
root2 = ET.parse('deu_Country_en_xml_v2.xml').getroot()  # wczytanie i parsowanie pliku xml zawierajacego dane dla Niemiec
root3 = ET.parse('ukr_Country_en_xml_v2.xml').getroot()  # wczytanie i parsowanie pliku xml zawierajacego dane dla Ukrainy
root4 = ET.parse('cze_Country_en_xml_v2.xml').getroot()  # wczytanie i parsowanie pliku xml zawierajacego dane dla Czech


def parse_xml(key, bottom_data, top_data):
    """Funkcja zbierajaca dane z plikow xml oraz tworzaca na ich podstawie wykresy."""

    """Argument key pozwala wczytywac dane dla konkretnego klucza- obszarow uprawnych, inwestycji zagranicznych,
    gestosci zaludnienia oraz ilosci turystow.
    Argumenty bottom_data oraz top_data to dolna i gorna granica lat, dla ktorych wczytujemy dane, tak aby byly
    one dostepne dla wszystkich krajow.
    """

    root_list = [root1, root2, root3, root4]  # stworzenie listy sparsowanych danych z plikow xml
    t = np.arange(int(bottom_data), int(top_data) + 1, 1)  # tablica argumentow wykresu
    legend_list = ["Pl", "Deu", "Ukr", "Cze"]  # lista zawierajaca dane do utworzenia legendy wykresu
    for root in root_list:
        values_list = []  # stworzenie pustej listy wartosci
        for child in root:
            for data in child:
                for record in data:
                    if record.attrib.values()[0] == 'Item':
                        if record.attrib.values()[1] == key:  # dla konkretnego klucza
                            if data[2].text >= bottom_data and data[2].text <= top_data:  # jesli dane mieszcza sie w przedziale czasowym
                                values_list.append((data[3]).text)  # dodanie konkretnych wartosci do listy
        plt.plot(t, values_list)  # stworzenie wykresu na podstawie listy wartosci
    leg = plt.legend((legend_list), loc='lower center', title='Kraje', ncol=4, prop={'size': 6})  # stworzenie legendy wykresu        
    leg.get_frame().set_alpha(0.2)  # ustawienie przezroczystosci legendy


def write_html():
    """Funkcja zapisujaca stworzone wczesniej wykresy do pliku 'statystyki.html'."""

    root = ET.Element("html")  # tworze szablon dokumentu
    head = ET.SubElement(root, "head")  # naglowek
    title = ET.SubElement(head, "title")  # tytul
    title.text = "Strona pierwsza"
    body = ET.SubElement(root, "body")
    paragraph = ET.SubElement(body, "p")
    paragraph.text = "Wykresy:"
    imgdata = StringIO.StringIO()  # bufor imitujacy obiekt pliku
    plt.savefig(imgdata, format="svg")
    svg_txt = imgdata.getvalue()  # pobieram dane z bufora
    imgdata.close()  # czyszcze bufor ("zamykam" wirtualny plik)
    ET.register_namespace("", "http://www.w3.org/2000/svg")  # informujemy biblioteke o nowej przestrzeni nazw
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    svg_tree_root = ET.fromstring(svg_txt)  # wczytuje dokument, funkcja fromstring zwraca korzen , czyli element svg
    paragraph = ET.SubElement(body, "p")
    paragraph.append(svg_tree_root)  # dodaje obrazek do dokumentu
    with open("statystyki.html", "w") as f:
        f.write(ET.tostring(root))  # zapisujemy wynik do pliku


def run():
    """Funkcja startowa programu wywolujaca funkcje parsujaca pliki xmlowe."""

    ax = plt.subplot(2, 2, 1)  # dzialamy na pierwszym wykresie
    ax.set_title("Obszary uprawne")  # nadanie tytulu pierwszemu wykresowi
    parse_xml('AG.LND.AGRI.ZS', "1993", "2012")  # wywolanie funkcji tworzacej wykres dla obszarow uprawnych
    ax = plt.subplot(2, 2, 2)  # dzialamy na drugim wykresie
    ax.set_title("Inwestycje zagraniczne")  # nadanie tytulu drugiemu wykresowi
    parse_xml('BM.KLT.DINV.GD.ZS', "2005", "2013")  # wywolanie funkcji tworzacej wykres dla inwestycji zagranicznych
    ax = plt.subplot(2, 2, 3)  # dzialamy na trzecim wykresie
    ax.set_title("Gestosc zaludnienia")  # nadanie tytulu trzeciemu wykresowi
    parse_xml('EN.POP.DNST', "1961", "2013")  # wywolanie funkcji tworzacej wykres dla gestosci zaludnienia
    ax = plt.subplot(2, 2, 4)  # dzialamy na czwartym wykresie
    ax.set_title("Ilosc turystow")  # nadanie tytulu czwartemu wykresowi
    parse_xml('ST.INT.ARVL', "2003", "2013")  # wywolanie funkcji tworzacej wykres dla ilosci turystow
    write_html()  # wywolanie funkcji zapisujacej dane do pliku 'statystyki.html'


run()
print'ok'
