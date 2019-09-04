import os
import json
import pdfkit
import pandas
from datetime import datetime


class Program:
    def __init__(self):
        self.ime = "program"
        self.doloci_poti()
        self.dimenzije = self.preberi_dimenzije('dimenzije.txt')
        self.urejene_dimenzije = self.uredi_dimenzije(self.dimenzije)
        self.tvorjene_dimenzije = [self.tvori_dimenzijo(dimenzija[0],dimenzija[1],dimenzija[2],dimenzija[3]) for dimenzija in self.dimenzije]
        self.zaloga = Zaloga()
        self.nalozi_stranke()
        self.nalozi_slovar()
        self.nalozi_cenik()
        self.preberi_aktivne_baze()
        self.delovna_baza = None
        self.ponastavi_velikosti()
        self.design = Design()

############################################################################################################

    def nalozi_slovar(self):
        os.chdir(self.path)
        with open('program.json') as dat:
            slovar = json.load(dat)
        self.slovar = slovar

    def shrani_slovar(self):
        os.chdir(self.path)
        with open('program.json',"w") as dat:
            json.dump(self.slovar,dat)


    def nastavi_naslednjo_fakturo(self,razlika = 1, leto = "2019"):
        self.nalozi_slovar()
        trenutna_faktura = self.slovar["naslednja_faktura"]
        stevilo_fakture = int(trenutna_faktura.split("/")[0])
        naslednjo_stevilo = stevilo_fakture + razlika
        if naslednjo_stevilo < 10:
            naslednja_faktura = '00' + str(naslednjo_stevilo) + '\2019'
        elif naslednjo_stevilo < 100:
            naslednja_faktura = '0' + str(naslednjo_stevilo) + '\2019'
        else:
            naslednja_faktura = str(naslednjo_stevilo) + '\2019'
        self.slovar["naslednja_faktura"] = naslednja_faktura
        self.shrani_slovar()

    def preberi_excel(self,filename,tip_tabele=0):
        seznam = []
        if tip_tabele == 0:
            data = pandas.read_excel(filename, use_cols = [1,2,3])
            seznam = data.values.tolist()
        elif tip_tabele == 1:
            data = pandas.read_excel(filename, use_cols = [1,2], header=None)
            seznam = data.values.tolist()
            seznam.remove(seznam[-1])
        return seznam

    def ustvari_lepo_datoteko_iz_excela(self,filename,tip_tabele = 0):
        data = self.preberi_excel(filename,tip_tabele)
        text_file = filename.replace(".xlsx",".txt")
        with open(text_file,"w") as dat:
            for seznam in data:
                dat.write(str(seznam[0]) + ";" + str(seznam[1]) + "\n")
        self.iz_grde_v_lepo_datoteko(text_file)

    def ustvari_pdf(self):
        pdfkit.from_url('http://bozojoel.pythonanywhere.com/pregled_zaloge_meni/pdf_table/', 'out2.pdf')

    def nalozi_cenik(self):
        os.chdir(self.path)
        with open('cenik.json') as dat:
            slovar = json.load(dat)
        self.cenik = slovar

    def shrani_cenik(self):
        os.chdir(self.path)
        with open('cenik.json',"w") as dat:
            json.dump(self.cenik,dat, indent=4)

    def spremeni_ceno(self,tip_prodaje,dimenzija,tip_dimenzije,nova_cena):
        self.nalozi_cenik()
        if tip_dimenzije in ["yellow", "Yellow", "Y", "y", 0]:
            self.cenik[dimenzija][tip_prodaje][0] = nova_cena
        elif tip_dimenzije in ["white", "White", "W", "w", 1]:
            self.cenik[dimenzija][tip_prodaje][1] = nova_cena
        self.shrani_cenik()

    def ustvari_cenik(self):
        cenik = {}
        for dimenzija in self.tvorjene_dimenzije:
            slovar = {
                dimenzija: {
                    "dnevna_prodaja": [0,0],
                    "vele_prodaja": [0,0]
                }
            }
            cenik.update(slovar)
        with open("cenik.json","w") as dat:
            json.dump(cenik,dat, indent = 4)


    def vrni_danes(self):
        danes = datetime.today()
        return danes.strftime("%Y-%m-%d")
        
    def iz_grde_v_lepo_datoteko(self,ime_datoteke):
        slovar_dimenzij = {dimenzija: [0,0] for dimenzija in self.tvorjene_dimenzije} 
        with open(ime_datoteke) as dat:
            for vrstica in dat:
                seznam = vrstica.replace("\n","").split(";")
                dimenzija = seznam[0]
                if "-B" in dimenzija:
                    slovar_dimenzij[dimenzija.replace("-B","")][1] += int(seznam[1])
                else:
                    slovar_dimenzij[dimenzija][0] += int(seznam[1])
        with open(ime_datoteke,"w") as dat:
            for dimenzija in slovar_dimenzij:
                yellow = str(slovar_dimenzij[dimenzija][0])
                white = str(slovar_dimenzij[dimenzija][1])
                dat.write(dimenzija + ";" + yellow +  ";" + white + "\n")
                    
        
    def doloci_poti(self):
        self.path = os.getcwd()
        self.prevzemi_path = os.path.join('arhiv','prevzemi')
        self.inventure_path = os.path.join('arhiv','inventure')
        self.vele_prodaje_path = os.path.join('arhiv','vele_prodaje')
        self.dnevne_prodaje_path = os.path.join('arhiv','dnevne_prodaje')
        self.odpisi_path = os.path.join('arhiv','odpisi')

    def vrni_path_arhiva(self, tip_baze):
        if tip_baze == "prevzem":
            return self.prevzemi_path
        elif tip_baze == "inventura":
            return self.inventure_path
        elif tip_baze == "vele_prodaja":
            return self.vele_prodaje_path
        elif tip_baze == "dnevna_prodaja":
            return self.dnevne_prodaje_path
        elif tip_baze == "odpis":
            return self.odpisi_path

##############################################################################################################

    def preberi_dimenzije(self,file):
        dimenzije = []
        dat = open(file)
        for vrstica in dat:
            vrstica = vrstica.replace("\n","")
            seznam_dimenzije = vrstica.split(";")
            if seznam_dimenzije[3] == "FALSE":
                seznam_dimenzije[3] = False
            elif seznam_dimenzije[3] == "TRUE":
                seznam_dimenzije[3] = True
            dimenzije.append(seznam_dimenzije)
        dat.close()
        return dimenzije

    def uredi_dimenzije(self,dimenzije):
        slovar_dimenzij = {}
        for dimenzija in dimenzije:
            radius = dimenzija[0]
            height = dimenzija[1]
            width = dimenzija[2]
            special = dimenzija[3]
            if radius in slovar_dimenzij:
                if height in slovar_dimenzij[radius]:
                    if special:
                        if not width + "C" in slovar_dimenzij[radius][height]:
                            slovar_dimenzij[radius][height].append(width + "C")
                    elif width == "R":
                        if not width + radius in slovar_dimenzij[radius][height]:
                            slovar_dimenzij[radius][height].append(width + radius)
                    else:
                        if not width in slovar_dimenzij[radius][height]:
                            slovar_dimenzij[radius][height].append(width)
                else:
                    if special:
                        slovar_dimenzij[radius].update({height:[width + "C"]})
                    elif width == "R":
                        slovar_dimenzij[radius].update({height:[width + radius]})
                    else:
                        slovar_dimenzij[radius].update({height:[width]})
            else:
                if special:
                    slovar_dimenzij.update({radius:{height:[width + "C"]}})
                elif width == "R":
                    slovar_dimenzij.update({radius:{height:[width + radius]}})
                else:
                    slovar_dimenzij.update({radius:{height:[width]}})
        return slovar_dimenzij
            
    def tvori_dimenzijo(self,radius,height,width,special = False):
        radius = str(radius)
        height = str(height)
        width = str(width)
        if special or width[-1] == "C":
            return height + "/" + width.replace("C","") + "/R" + radius.replace("R","") + "C"
        elif width[0] == "R":
            return height + "/" + width[0] + radius
        elif radius[0] == "R":
            return height + "/" + width + "/" + radius
        else:
            return height + "/" + width + "/R" + radius
    
    def razcleni_dimenzijo(self,dimenzija):
        razclenjena = dimenzija.split("/")
        if len(razclenjena) == 2:
            seznam_dimenzije = [razclenjena[1].replace("R",""),razclenjena[0],razclenjena[1][0],"FALSE"]
        else:
            if dimenzija[-1] == "C":
                seznam_dimenzije = [razclenjena[2].replace("R","").replace("C",""),razclenjena[0],razclenjena[1],"TRUE"]
            else:
                seznam_dimenzije = [razclenjena[2].replace("R",""),razclenjena[0],razclenjena[1],"FALSE"]
        return seznam_dimenzije
    
    def vrni_tvorjene_dimenzije_dolocenega_radiusa(self,radius):
        seznam_dimenzij = []
        for dimenzija in self.dimenzije:
            if int(dimenzija[0]) == int(radius):
                seznam_dimenzij.append(self.tvori_dimenzijo(dimenzija[0],dimenzija[1],dimenzija[2],dimenzija[3]))
        return seznam_dimenzij

    def vrni_tvorjene_dimenzije_dolocenega_heighta(self,radius,height):
        seznam_dimenzij = []
        for dimenzija in self.dimenzije:
            if dimenzija[0] == radius and dimenzija[1] == height:
                seznam_dimenzij.append(self.tvori_dimenzijo(dimenzija[0],dimenzija[1],dimenzija[2],dimenzija[3]))
        return seznam_dimenzij

    def vrni_tvorjene_dimenzije_dolocenega_widtha(self,radius,height,width):
        seznam_dimenzij = []
        for dimenzija in self.dimenzije:
            if dimenzija[0] == radius and dimenzija[1] == height and dimenzija[2] == width:
                seznam_dimenzij.append(self.tvori_dimenzijo(dimenzija[0],dimenzija[1],dimenzija[2],dimenzija[3]))
        return seznam_dimenzij

    def filtrirane_dimenzije(self,radius="all",height="all",width="all"):
        if radius == "all":
            return self.tvorjene_dimenzije
        else:
            if height == "all":
                return self.vrni_tvorjene_dimenzije_dolocenega_radiusa(radius)
            else:
                if width == "all":
                    return self.vrni_tvorjene_dimenzije_dolocenega_heighta(radius,height)
                else:
                    return self.vrni_tvorjene_dimenzije_dolocenega_widtha(radius,height,width)

    def vrni_vse_radiuse(self):
        radiusi = []
        for dimenzija in self.dimenzije:
            if not dimenzija[0] in radiusi:
                radiusi.append(dimenzija[0])
        return radiusi

    def vrni_vse_heighte(self):
        heighti = []
        for dimenzija in self.dimenzije:
            if not dimenzija[1] in heighti:
                heighti.append(dimenzija[1])
        return heighti

    def vrni_vse_widthe(self):
        widthi = []
        for dimenzija in self.dimenzije:
            if not dimenzija[2] in widthi:
                widthi.append(dimenzija[2])
        return widthi

############################################################################################################      
    
    def vrni_bazo(self,path,ime):
        return Baza(self.path,path,ime)

    def dodaj_bazo_vele_prodaje(self,stranka,datum):
        os.chdir('aktivne_baze')
        ime = self.slovar["naslednja_faktura"]
        slovar = {
                    "osnovni_path": self.path,
                    "moj_path": 'aktivne_baze',
                    "ime_datoteke": ime + '.json',
                    "ime": ime,
                    "tip": "vele_prodaja",
                    "stranka": stranka,
                    "datum": datum,
                    "cas_zakljucka":"",
                    "dimenzije":{dimenzija : [0,0] for dimenzija in self.tvorjene_dimenzije},
                    "vnosi":[]
                    } 
        with open(ime + '.json','w') as dat:
            json.dump(slovar, dat, indent = 4)
        os.chdir(self.path)
        self.preberi_aktivne_baze()

    def dodaj_bazo_dnevne_prodaje(self,datum):
        os.chdir('aktivne_baze')
        ime = datum
        slovar = {
                    "osnovni_path": self.path,
                    "moj_path": 'aktivne_baze',
                    "ime_datoteke": ime + '.json',
                    "ime": ime,
                    "tip": "dnevna_prodaja",
                    "datum": datum,
                    "cas_zakljucka":"",
                    "dimenzije":{dimenzija : [0,0] for dimenzija in self.tvorjene_dimenzije},
                    "vnosi":[]
                    } 
        with open(ime + '.json','w') as dat:
            json.dump(slovar, dat, indent = 4)
        os.chdir(self.path)
        self.preberi_aktivne_baze()
     
    def dodaj_bazo(self,ime,datum,tip):
        os.chdir('aktivne_baze')
        slovar = {
                    "osnovni_path": self.path,
                    "moj_path": 'aktivne_baze',
                    "ime_datoteke": ime + '.json',
                    "ime": ime,
                    "tip": tip,
                    "datum": datum,
                    "cas_zakljucka":"",
                    "dimenzije":{dimenzija : [0,0] for dimenzija in self.tvorjene_dimenzije},
                    "vnosi":[]
                    } 
        with open(ime + '.json','w') as dat:
            json.dump(slovar, dat, indent = 4)
        os.chdir(self.path)
        self.preberi_aktivne_baze()
    
    def preberi_aktivne_baze(self):
        os.chdir('aktivne_baze')
        datoteke_aktivnih_baz = os.listdir()
        seznam_aktivnih_baz = []
        os.chdir(self.path)
        for dat in datoteke_aktivnih_baz: 
            baza = Baza(self.path,'aktivne_baze',dat)
            seznam_aktivnih_baz.append(baza)
        self.aktivne_baze = seznam_aktivnih_baz
        
    def vrni_aktivno_bazo(self,tip):
        self.preberi_aktivne_baze()
        for baza in self.aktivne_baze:
            if baza.tip == tip:
                return baza
        return None
###########################################################################################################

    def doloci_delovno_bazo(self,baza):
        self.delovna_baza = baza

    def nastavi_radius(self,radius):
        self.radius = radius

    def nastavi_height(self,height):
        self.height = height
    
    def nastavi_width(self,width):
        self.width = width
    
    def ponastavi_velikosti(self):
        self.radius = None
        self.height = None
        self.width = None

####################################################################################################

    def nalozi_stranke(self):
        os.chdir(self.path)
        with open('stranke.json') as dat:
            slovar = json.load(dat)
        self.stranke = slovar

    def ustvari_stranke(self):
        os.chdir(self.path)
        slovar = {
            "stevilo_strank": 0,
            "stranke": [],
            "stare_stranke": []
        }
        with open('stranke.json',"w") as dat:
            json.dump(slovar,dat,indent=4) 

    def shrani_stranke(self):
        os.chdir(self.path)
        with open('stranke.json',"w") as dat:
            json.dump(self.stranke,dat,indent=4) 

    def dodaj_stranko(self,ime_stranke,telefonska,mail,boniranje):
        self.nalozi_stranke()
        index = self.stranke["stevilo_strank"] + 1
        stranka = {
            "index" : index,
            "aktivna" : True,
            "ime" : ime_stranke,
            "telefon" : telefonska,
            "e-mail" : mail,
            "boniranje" : boniranje,
            "narocila" : [],
            "nakupi" : []
        }
        self.stranke["stranke"].append(stranka)
        self.stranke["stevilo_strank"] += 1
        self.shrani_stranke()
       
    def dodaj_narocilo(self,index_stranke,baza_narocila,datum):
        self.nalozi_stranke()
        for stranka in self.stranke["stranke"]:
            if stranka["index"] == index_stranke:
                break
        narocilo = {
            "ime_datoteke": baza_narocila.slovar["ime_datoteke"],
            "path": baza_narocila.slovar["moj_path"],
            "datum": datum
            }
        if len(stranka["narocila"]) == 0:
            stranka["narocila"].append(narocilo)
        else:
            stranka["narocila"].insert(0,narocilo)
        self.shrani_stranke()

    def dodaj_nakup(self,index_stranke,baza_nakupa,datum):
        self.nalozi_stranke()
        for stranka in self.stranke["stranke"]:
            if stranka["index"] == index_stranke:
                break
        narocilo = {
            "ime_datoteke": baza_nakupa.slovar["ime_datoteke"],
            "path": baza_nakupa.slovar["moj_path"],
            "datum": datum
            }
        if len(stranka["nakupi"]) == 0:
            stranka["nakupi"].append(narocilo)
        else:
            stranka["nakupi"].insert(0,narocilo)
        self.shrani_stranke()

    def spremeni_stranko(self,index_stranke,slovar_sprememb):
        self.nalozi_stranke()
        for stranka in self.stranke["stranke"]:
            if stranka["index"] == index_stranke:
                for sprememba in slovar_sprememb:
                    if sprememba in stranka:
                        stranka[sprememba] = slovar_sprememb[sprememba]
                break
        self.shrani_stranke()

    def odstrani_stranko(self,index_stranke):
        self.nalozi_stranke()
        for stranka in self.stranke["stranke"]:
            if stranka["index"] == index_stranke:
                stranka["aktivna"] = False 
                self.stranke["stare_stranke"].append(stranka)      
                self.stranke["stranke"].remove(stranka)
        self.shrani_stranke()        
    
#####################################################################################################

    def v_arhiv(self, baza):
        prvotni_path = os.path.join(baza.moj_path, baza.ime_datoteke) 
        path_arhiva = self.vrni_path_arhiva(baza.tip)
        ciljni_path = os.path.join(self.path, path_arhiva , baza.ime_datoteke)
        os.rename(prvotni_path, ciljni_path)
        baza.spremeni_path(path_arhiva)
        baza.doloci_cas_zakljucka()


class Zaloga:
    def __init__(self,ime_datoteke='zaloga.json'):
        self.ime_datoteke = ime_datoteke
        self.path = os.getcwd()
        self.baza = Baza(self.path,self.path,self.ime_datoteke)
        self.baza.nalozi()

    def dodaj_iz_baze(self,baza):
        self.baza.nalozi()
        slovar_baze = baza.slovar["dimenzije"]
        slovar_zaloge = self.baza.slovar["dimenzije"]
        for dimenzija in slovar_baze:
            if dimenzija in slovar_zaloge:
                slovar_zaloge[dimenzija][0] += slovar_baze[dimenzija][0]
                slovar_zaloge[dimenzija][1] += slovar_baze[dimenzija][1]
        self.baza.slovar["dimenzije"] = slovar_zaloge
        self.baza.shrani()

    def odstrani_iz_baze(self,baza):
        self.baza.nalozi()
        slovar_baze = baza.slovar["dimenzije"]
        slovar_zaloge = self.baza.slovar["dimenzije"]
        for dimenzija in slovar_baze:
            if dimenzija in slovar_zaloge:
                slovar_zaloge[dimenzija][0] += - (slovar_baze[dimenzija][0])
                slovar_zaloge[dimenzija][1] += - (slovar_baze[dimenzija][1])
        self.baza.slovar["dimenzije"] = slovar_zaloge
        self.baza.shrani()

    def dodaj_stevilo(self,dimenzija,tip,stevilo):
        self.baza.nalozi()
        slovar = self.baza.slovar["dimenzije"]
        if dimenzija in slovar:
            if tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
                slovar[dimenzija][0] += int(stevilo)
            elif tip == "white" or tip == "w" or tip == "W" or tip == 2:
                slovar[dimenzija][1] += int(stevilo)
        self.baza.slovar["dimenzije"] = slovar
        self.baza.shrani()

    def odstrani_stevilo(self,dimenzija,tip,stevilo):
        self.baza.nalozi()
        slovar = self.baza.slovar["dimenzije"]
        if dimenzija in slovar:
            if tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
                slovar[dimenzija][0] += - int(stevilo)
            elif tip == "white" or tip == "w" or tip == "W" or tip == 2:
                slovar[dimenzija][1] += - int(stevilo)
        self.baza.slovar["dimenzije"] = slovar
        self.baza.shrani()   

    def uveljavi_inventuro(self,baza,ohrani = False):
        slovar_dimenzij_baze = baza.slovar["dimenzije"]
        spremembe = []
        if ohrani:
            spremembe = self.uveljavi_inventuro_ohrani(baza,slovar_dimenzij_baze,spremembe)
        else:
            spremembe = self.uveljavi_inventuro_neohrani(baza,slovar_dimenzij_baze,spremembe)
        baza.slovar.update({"spremembe":spremembe})
        baza.shrani()

    def uveljavi_inventuro_ohrani(self,baza,slovar_dimenzij_baze,spremembe):
        slovar_dimenzij = self.baza.slovar["dimenzije"]
        for dimenzija in slovar_dimenzij_baze:
            if slovar_dimenzij_baze[dimenzija][0] == 0:
                for vnos in baza.slovar["vnosi"]:
                    if vnos["dimenzija"] == dimenzija and vnos["tip"] == "yellow":
                        slovar_dimenzij[dimenzija][0] = slovar_dimenzij_baze[dimenzija][0]
                        razlika = slovar_dimenzij_baze[dimenzija][0] - slovar_dimenzij[dimenzija][0]
                        spremembe.append({"dimenzija":dimenzija,"tip":"yellow","razlika":razlika})
                        break
            else:
                slovar_dimenzij[dimenzija][0] = slovar_dimenzij_baze[dimenzija][0]
                razlika = slovar_dimenzij_baze[dimenzija][0] - slovar_dimenzij[dimenzija][0]
                spremembe.append({"dimenzija":dimenzija,"tip":"yellow","razlika":razlika})
            if slovar_dimenzij_baze[dimenzija][1] == 0:
                for vnos in baza.slovar["vnosi"]:
                    if vnos["dimenzija"] == dimenzija and vnos["tip"] == "white":
                        slovar_dimenzij[dimenzija][1] = slovar_dimenzij_baze[dimenzija][1]
                        razlika = slovar_dimenzij_baze[dimenzija][1] - slovar_dimenzij[dimenzija][1]
                        spremembe.append({"dimenzija":dimenzija,"tip":"white","razlika":razlika})
                        break
            else:
                slovar_dimenzij[dimenzija][0] = slovar_dimenzij_baze[dimenzija][0]
                razlika = slovar_dimenzij_baze[dimenzija][0] - slovar_dimenzij[dimenzija][0]
                spremembe.append({"dimenzija":dimenzija,"tip":"yellow","razlika":razlika})
        self.baza.slovar["dimenzije"] = slovar_dimenzij
        self.baza.shrani()
        return spremembe

    def uveljavi_inventuro_neohrani(self,baza,slovar_dimenzij_baze,spremembe):
        slovar_dimenzij = self.baza.slovar["dimenzije"]
        for dimenzija in slovar_dimenzij_baze:
            razlika = slovar_dimenzij_baze[dimenzija][0] - slovar_dimenzij[dimenzija][0]
            if razlika != 0:
                slovar_dimenzij[dimenzija][0] = slovar_dimenzij_baze[dimenzija][0]
                spremembe.append({"dimenzija":dimenzija,"tip":"yellow","razlika":razlika})
            razlika = slovar_dimenzij_baze[dimenzija][1] - slovar_dimenzij[dimenzija][1]
            if razlika != 0:
                slovar_dimenzij[dimenzija][1] = slovar_dimenzij_baze[dimenzija][1]
                spremembe.append({"dimenzija":dimenzija,"tip":"white","razlika":razlika})            
        self.baza.slovar["dimenzije"] = slovar_dimenzij
        self.baza.shrani()
        return spremembe



    def dodaj_v_arhiv(self,baza):
        self.baza.nalozi()
        self.baza.slovar[self.zamenjaj_v_mnozino(baza.tip)].insert(0,baza.ime_datoteke)
        self.dodaj_v_spremembe(baza)
        self.baza.shrani()

    def dodaj_v_spremembe(self, baza):
        slovar = {
                    "ime_datoteke": baza.slovar["ime_datoteke"],
                    "tip": baza.slovar["tip"],
                    "datum": baza.slovar["datum"]
                }
        if len(self.baza.slovar["spremembe"]) == 0:
            self.baza.slovar["spremembe"].append(slovar)
        else:
            for sprememba in self.baza.slovar["spremembe"]:
                cas_baze = datetime.strptime(baza.slovar["datum"], '%Y-%m-%d')
                cas_spremembe = datetime.strptime(sprememba["datum"], '%Y-%m-%d')
                index_spremembe = self.baza.slovar["spremembe"].index(sprememba)
                if cas_baze < cas_spremembe:
                    self.baza.slovar["spremembe"].insert(index_spremembe,slovar)
                    break
                elif index_spremembe == len(self.baza.slovar["spremembe"]) - 1:
                    self.baza.slovar["spremembe"].append(slovar)
                    break
        
    def zamenjaj_v_mnozino(self,tip):
        if tip == "prevzem":
            return "prevzemi"
        elif tip == "inventura":
            return "inventure"
        elif tip == "vele_prodaja":
            return "vele_prodaje"
        elif tip == "dnevna_prodaja":
            return "dnevne_prodaje"
        elif tip == "odpis":
            return "odpisi"

class Baza:
    def __init__(self,osnovni_path,moj_path,ime_datoteke):
        self.osnovni_path = osnovni_path
        self.moj_path = moj_path
        self.ime_datoteke = ime_datoteke
        self.nalozi()
        self.ime = self.slovar["ime"]
        self.tip = self.slovar["tip"]
        self.dimenzije = self.slovar["dimenzije"]
        if self.tip == "zaloga":
            self.prevzemi = self.slovar["prevzemi"]
            self.inventure = self.slovar["inventure"]
            self.dnevne_prodaje = self.slovar["dnevne_prodaje"]
            self.vele_prodaje = self.slovar["vele_prodaje"]
            self.odpisi = self.slovar["odpisi"]
        else:
            self.vnosi = self.slovar["vnosi"]
            self.cas_zakljucka = self.slovar["cas_zakljucka"]
            self.datum = self.slovar["datum"]

    def __repr__(self):
        return self.ime

#######################################################################################################

    def stevilo(self, dimenzija, tip = ""):
        self.nalozi()
        if dimenzija in self.dimenzije:
            yellow = self.dimenzije[dimenzija][0]
            white = self.dimenzije[dimenzija][1]
            if tip == "":
                return yellow + white
            elif tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
                return yellow
            elif  tip == "white" or tip == "w" or tip == "W" or tip == 2:
                return white
        else:
            print("Napacna dimenzija!")
            return -1

    def skupno_stevilo(self,tip = ""):
        self.nalozi()
        yellow = 0
        white = 0
        slovar = self.slovar["dimenzije"]
        for dimenzija in slovar:
            yellow += slovar[dimenzija][0]
            white += slovar[dimenzija][1]
        if tip == "":
            return yellow + white
        elif tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
            return yellow
        elif  tip == "white" or tip == "w" or tip == "W" or tip == 2:
            return white

#######################################################################################################
    def ponastavi_na_zacetno_stanje(self):
        self.nalozi()
        slovar = self.slovar["dimenzije"]
        for dimenzija in slovar:
            slovar[dimenzija][0] = 0
            slovar[dimenzija][1] = 0
        self.slovar["dimenzije"] = slovar
        self.slovar["vnosi"] = []
        self.shrani()

    def vrni_nevnesene(self):
        self.nalozi()
        slovar_dimenzij = self.slovar["dimenzije"]
        slovar_vnosov = self.slovar["vnosi"]
        nevnesene = {}
        for dimenzija in slovar_dimenzij:
            yellow = False
            white = False
            for vnos in slovar_vnosov:
                if vnos["dimenzija"] == dimenzija and vnos["tip"] == "yellow":
                    yellow = True
                if vnos["dimenzija"] == dimenzija and vnos["tip"] == "white":
                    white = True
                if yellow and white:
                    break
            if not yellow and not white:
                nevnesene.update({dimenzija:["yellow","white"]})
            elif not yellow:
                nevnesene.update({dimenzija:["yellow"]})
            elif not white:
                nevnesene.update({dimenzija:["white"]})
        return nevnesene

    def dodaj_iz_datoteke(self,datoteka):
        besedilo = ""
        for vrstica in datoteka.readlines():
            seznam = vrstica.decode().split(";")
            dimenzija = seznam[0]
            yellow = int(seznam[1])
            white = int(seznam[2])
            if dimenzija in self.slovar["dimenzije"]:
                if yellow > 0:
                    self.nov_vnos(dimenzija,yellow,"yellow")
                if white > 0:
                    self.nov_vnos(dimenzija,white,"white")
            else: besedilo += dimenzija + ";"
        self.shrani()
        return besedilo

    def dodaj_iz_grde_datoteke(self,path_datoteke):
        with open(path_datoteke) as dat:
            besedilo = ""
            for vrstica in dat:
                seznam = vrstica.split(";")
                dimenzija = seznam[0]
                stevilo = int(seznam[1].replace("\n",""))
                if "-B" in dimenzija:
                    dimenzija = dimenzija.replace("-B","")
                    if dimenzija in self.slovar["dimenzije"]:
                        self.nov_vnos(dimenzija,stevilo,"white")
                    else:
                        besedilo += dimenzija + ","
                else:
                    if dimenzija in self.slovar["dimenzije"]:
                        self.nov_vnos(dimenzija,stevilo,"yellow")
        self.shrani()
        return besedilo
    
    def ustvari_lepo_datoteko(self,ime_datoteke):
        with open(ime_datoteke,"w") as dat:
            for dimenzija in self.slovar["dimenzije"]:
                yellow = str(self.slovar["dimenzije"][dimenzija][0])
                white = str(self.slovar["dimenzije"][dimenzija][1])
                dat.write(dimenzija + ";" + yellow +  ";" + white + "\n")
             
        
    def preveri_dimenzije(self,path_datoteke):
        with open(path_datoteke) as dat:
            besedilo = ""
            for vrstica in dat:
                if not (vrstica.replace("\n","") in self.slovar["dimenzije"]):
                    besedilo += vrstica + ","
        return besedilo

    def nov_vnos(self,dimenzija,stevilo,tip):
        self.nov_vnos_dimenzije(dimenzija,stevilo,tip)
        self.nov_vnos_vnosi(dimenzija,stevilo,tip)

    def nov_vnos_shrani(self, dimenzija, stevilo, tip):
        self.nalozi()
        self.nov_vnos_dimenzije(dimenzija,stevilo,tip)
        self.nov_vnos_vnosi(dimenzija,stevilo,tip)
        self.shrani()

    def nov_vnos_dimenzije(self,dimenzija,stevilo,tip):
        slovar = self.slovar["dimenzije"]
        if tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
            slovar[dimenzija][0] += stevilo
        elif  tip == "white" or tip == "w" or tip == "W" or tip == 2:
            slovar[dimenzija][1] += stevilo
        self.slovar["dimenzije"] = slovar
    
    def nov_vnos_vnosi(self,dimenzija,stevilo,tip):
        seznam = self.slovar["vnosi"]
        if tip == "yellow" or tip == "y" or tip == "Y" or tip == 1:
            tip = "yellow"
        elif tip == "white" or tip == "w" or tip == "W" or tip == 2:
            tip = "white"
        slovar = {
            "index": len(seznam) + 1,
            "dimenzija": dimenzija,
            "stevilo": stevilo,
            "tip": tip,
            "cas": str(datetime.now())
        }
        seznam.append(slovar)
        self.slovar["vnosi"] = seznam

    def poprava_vnosa(self,index_vnosa,nacin,stevilo = None):
        '''obstajajo trije načini popravne vnosa:
            1. izbris
            2. poprava_tipa
            3. poprava_stevila
        '''
        self.nalozi()
        if nacin == "izbris":
            self.izbrisi_vnos(index_vnosa)
        elif nacin == "poprava_tipa":
            self.popravni_vnos_tip(index_vnosa)
        elif nacin == "poprava_stevila":
            if stevilo != None:
                self.popravi_vnos_stevilo(index_vnosa, stevilo)
            else:
                print("Izberi novo število!")
        else:
            print("Nacin poprave vnosa ne obstaja!")
        self.shrani()

    def popravni_vnos_tip(self,index_vnosa):
        seznam = self.slovar["vnosi"]
        slovar = seznam[index_vnosa]
        self.popravi_vnos_tip_dimenzije(slovar["dimenzija"],slovar["stevilo"],slovar["tip"])
        if slovar["tip"] == "yellow":
            slovar["tip"] = "white"
        elif slovar["tip"] == "white":
            slovar["tip"] = "yellow"
        seznam[index_vnosa] = slovar
        self.slovar["vnosi"] = seznam

    def popravi_vnos_tip_dimenzije(self,dimenzija,stevilo,tip):
        slovar = self.slovar["dimenzije"]
        if tip == "yellow":
            slovar[dimenzija][0] += - stevilo
            slovar[dimenzija][1] += stevilo
        elif tip == "white":
            slovar[dimenzija][0] += stevilo
            slovar[dimenzija][1] += - stevilo
        self.slovar["dimenzije"] = slovar

    def popravi_vnos_stevilo(self,index_vnosa,novo_stevilo):
        seznam = self.slovar["vnosi"]
        slovar = seznam[index_vnosa]
        self.popravi_vnos_stevilo_dimenzije(slovar["dimenzija"],novo_stevilo - slovar["stevilo"],slovar["tip"])
        slovar["stevilo"] = novo_stevilo
        seznam[index_vnosa] = slovar
        self.slovar["vnosi"] = seznam
    
    def popravi_vnos_stevilo_dimenzije(self, dimenzija, razlika, tip):
        slovar = self.slovar["dimenzije"]
        if tip == "yellow":
            slovar[dimenzija][0] += razlika
        elif tip == "white":
            slovar[dimenzija][1] += razlika
        self.slovar["dimenzije"] = slovar

    def izbrisi_vnos(self,index_vnosa):
        seznam = self.slovar["vnosi"]
        slovar = seznam[index_vnosa]
        self.izbrisi_vnos_dimenzije(slovar["dimenzija"],slovar["stevilo"],slovar["tip"])
        seznam.remove(seznam[index_vnosa])
        i = 0
        for vnos in seznam:
            i += 1
            vnos["index"] = i
        self.slovar["vnosi"] = seznam

    def izbrisi_vnos_dimenzije(self,dimenzija,stevilo,tip):
        slovar = self.slovar["dimenzije"]
        if tip == "yellow":
            slovar[dimenzija][0] += - stevilo
        elif tip == "white":
            slovar[dimenzija][1] += - stevilo
        self.slovar["dimenzije"] = slovar

#######################################################################################################

    def zadnji_vnos(self):
        if len(self.slovar["vnosi"]) > 0:
            return self.slovar["vnosi"][-1]
        else:
            return -1

#######################################################################################################
    
    def spremeni_path(self,path):
        self.slovar["moj_path"] = path
        self.moj_path = path
        self.shrani()
        self.nalozi()

    def doloci_cas_zakljucka(self):
        self.nalozi()
        self.slovar["cas_zakljucka"] = str(datetime.now())
        self.shrani()

    def nalozi(self):
        os.chdir(self.moj_path)
        with open(self.ime_datoteke) as dat:
            slovar = json.load(dat)
        self.slovar = slovar
        os.chdir(self.osnovni_path)

    def shrani(self):
        os.chdir(self.moj_path)
        with open(self.ime_datoteke,"w") as dat:
            json.dump(self.slovar, dat, indent = 4)
        os.chdir(self.osnovni_path)

class Design:
    def __init__(self):
        self.ime = "design"
        self.razmak_med_gumbi = 2

    def button_position(self,stevilo_vseh_gumbov, index_gumba):
        if stevilo_vseh_gumbov == 1:
            return {"left": 0, "top": 0}
        elif stevilo_vseh_gumbov == 2:
            return {"left": index_gumba * ((100 - self.razmak_med_gumbi) // 2 + self.razmak_med_gumbi) ,"top": 0}
        elif 2 < stevilo_vseh_gumbov <= 4:
            return {"left": (index_gumba % 2) * ((100 - self.razmak_med_gumbi) // 2 + self.razmak_med_gumbi), "top": (index_gumba // 2) * ((100 - self.razmak_med_gumbi) // 2 + self.razmak_med_gumbi)}
        elif 4 < stevilo_vseh_gumbov <= 6:
            return {"left": (index_gumba % 3) * ((100 - 2 * self.razmak_med_gumbi) // 3 + self.razmak_med_gumbi) , "top": (index_gumba // 3) * ((100 - self.razmak_med_gumbi) // 2 + self.razmak_med_gumbi)}   
        elif 6 < stevilo_vseh_gumbov <= 9:
            return {"left": (index_gumba % 3) * ((100 - 2 * self.razmak_med_gumbi) // 3 + self.razmak_med_gumbi), "top": (index_gumba // 3) * ((100 - 2 * self.razmak_med_gumbi) // 3 + self.razmak_med_gumbi)}
        elif 9 < stevilo_vseh_gumbov <= 12:
            return {"left": (index_gumba % 4) * ((100 - 3 * self.razmak_med_gumbi) // 4 + self.razmak_med_gumbi), "top": (index_gumba // 4) * ((100 - 2 * self.razmak_med_gumbi) // 3 + self.razmak_med_gumbi)}
        elif 12 < stevilo_vseh_gumbov <= 16:
            return {"left": (index_gumba % 4) * ((100 - 3 * self.razmak_med_gumbi) // 4 + self.razmak_med_gumbi), "top": (index_gumba // 4) * ((100 - 3 * self.razmak_med_gumbi) // 4 + self.razmak_med_gumbi)}
        elif 16 < stevilo_vseh_gumbov <= 21:
            return {"left": (index_gumba % 5) * ((100 - 4 * self.razmak_med_gumbi) // 5 + self.razmak_med_gumbi), "top": (index_gumba // 5) * ((100 - 2 * self.razmak_med_gumbi) // 4 + self.razmak_med_gumbi)}

    def button_size(self,stevilo_vseh_gumbov):
        if stevilo_vseh_gumbov == 1:
            return {"width":100,"height":100}
        elif stevilo_vseh_gumbov == 2:
            return {"width": (100 - self.razmak_med_gumbi) / 2, "height": 100}   
        elif 2 < stevilo_vseh_gumbov <= 4:
            return {"width": (100 - self.razmak_med_gumbi) / 2, "height": (100 - self.razmak_med_gumbi) / 2}  
        elif 4 < stevilo_vseh_gumbov <= 6:
            return {"width": (100 - 2 * self.razmak_med_gumbi) / 3, "height": (100 - self.razmak_med_gumbi) / 2}  
        elif 6 < stevilo_vseh_gumbov <= 9:
            return {"width": (100 - 2 * self.razmak_med_gumbi) / 3, "height": (100 - 2 * self.razmak_med_gumbi) / 3}    
        elif 9 < stevilo_vseh_gumbov <= 12:
            return {"width": (100 - 3 * self.razmak_med_gumbi) / 4, "height": (100 - 2 * self.razmak_med_gumbi) / 3}  
        elif 12 < stevilo_vseh_gumbov <= 16:
            return {"width": (100 - 3 * self.razmak_med_gumbi) / 4, "height": (100 - 3 * self.razmak_med_gumbi) / 4}  
        elif 16 < stevilo_vseh_gumbov <= 21:
            return {"width": (100 - 4 * self.razmak_med_gumbi) / 5, "height": (100 - 3 * self.razmak_med_gumbi) / 4}  