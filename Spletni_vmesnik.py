import bottle
import os
from Model import Program, Baza

program = Program()

########################################################################################################
@bottle.route("/<karkoli1>/design/<path>")
def static_karkoli1(karkoli1,path):
    return bottle.static_file(path, root="./static")

@bottle.route("/<karkoli1>/<karkoli2>/design/<path>")
def static_karkoli2(karkoli1,karkoli2,path):
    return bottle.static_file(path, root="./static")

@bottle.route("/<karkoli1>/<karkoli2>/<karkoli3>/design/<path>")
def static_karkoli3(karkoli1,karkoli2,karkoli3,path):
    return bottle.static_file(path, root="./static")

@bottle.route("/<karkoli1>/<karkoli2>/<karkoli3>/<karkoli4>/design/<path>")
def static_karkoli4(karkoli1,karkoli2,karkoli3,karkoli4,path):
    return bottle.static_file(path, root="./static")

#########################################################################################################

@bottle.get("/")
def preusmeri():
    bottle.redirect('/osnovni_meni/')

@bottle.get('/osnovni_meni/')
def osnovni_meni():
    return bottle.template('osnovni_meni.tpl')

######################################################################################################

@bottle.get('/pregled_zaloge_meni/')
def pregled_zaloge_meni():
    global program
    if "radius" in bottle.request.query:
        order = bottle.request.query["order"]
        print(order)
        radius = bottle.request.query["radius"]
        height = bottle.request.query["height"]
        width = bottle.request.query["width"]
        if order == "numeric":
            dimenzije = program.filtrirane_dimenzije(radius,height,width)
        elif order == "alphabetic":
            dimenzije = sorted(program.filtrirane_dimenzije(radius,height,width))
    else:
         dimenzije = program.tvorjene_dimenzije
    return bottle.template('pregled_zaloge_meni.tpl', program = program, dimenzije = dimenzije)

@bottle.get('/pregled_zaloge_meni/filter_po_radiusu/<radius>')
def pregled_zaloge_fileter_po_radiusu(radius):
    global program
    dimenzije = program.vrni_tvorjene_dimenzije_dolocenega_radiusa(radius)
    return bottle.template('pregled_zaloge_meni.tpl', program = program, dimenzije = dimenzije)

@bottle.get('/pregled_zaloge_meni/filter_po_dimenziji/<dimenzija>')
def pregled_zaloge_fileter_po_dimenziji(dimenzija):
    global program
    return bottle.template('pregled_zaloge_meni.tpl', program = program, dimenzije = [dimenzija])

@bottle.get('/pregled_zaloge_meni/pregled_prometa/<dimenzija>/<tip>/')
def pregled_zaloge_pregled_prometa(dimenzija,tip):
    global program
    dimenzija = dimenzija.replace('-','/')
    return bottle.template('pregled_prometa.tpl', program = program, dimenzija = dimenzija, tip = tip)

@bottle.get('/pregled_zaloge_meni/pdf_table/')
def pregled_zaloge_pdf_table():
    global program
    return bottle.template('pdf_table.tpl', program = program)

@bottle.get('/pregled_zaloge_meni/pregled_pdf/')
def pregled_zaloge_pregled_pdf():
    global program
    return bottle.template('pregled_pdf.tpl', program = program)

######################################################################################################
@bottle.get('/poskus/')
def poskus():
    global program
    return bottle.template('dinamic_select.tpl' , program = program)

@bottle.get('/<tip>/aktivno/')
def aktivno_meni(tip):
    global program
    return bottle.template('aktivni_meni.tpl', program=program, tip = tip, popravljanje = False, vnos_za_spreminjanje = {"tip":None})

@bottle.post('/<tip>/aktivno/nova_baza/')
def aktivno_ustvari_novo_bazo(tip):
    global program
    datum = bottle.request.forms["datum"]
    if tip == "prevzem":
        kontejner = bottle.request.forms["kontejner"]
        program.dodaj_bazo(kontejner,datum,"prevzem")
    elif tip == "vele_prodaja":
        stranka = bottle.request.forms["stranka"]
        program.dodaj_bazo_vele_prodaje(stranka,datum)
    elif tip == "dnevna_prodaja":
        program.dodaj_bazo_dnevne_prodaje(datum)
    elif tip == "odpis":
        mesec = bottle.request.forms["mesec"]
        ime = "Odpis " + mesec
        program.dodaj_bazo(ime,datum,"odpis")
    elif tip == "inventura":
        stevilo_inventur = len(program.zaloga.baza.slovar["inventure"])
        ime = str(stevilo_inventur + 1) + ".inventura"
        program.dodaj_bazo(ime,datum,"inventura")
    bottle.redirect('/' + tip + '/aktivno/')

@bottle.post('/<tip>/aktivno/preusmeri_na_radius/')
def aktivno_preusmeri(tip):
    global program
    baza = program.vrni_aktivno_bazo(tip)
    if baza != None:
        program.zacetna_stran = "/" + tip + "/aktivno/"
        program.delovna_baza = baza
        bottle.redirect('/radius_meni/')
    else:
        bottle.redirect(program.zacetna_stran)

@bottle.post('/<tip>/aktivno/nov_vnos/')
def aktivno_nov_vnos(tip):
    global program
    baza = program.vrni_aktivno_bazo(tip)
    dimenzija = program.tvori_dimenzijo(program.radius,program.height,program.width)
    stevilo = bottle.request.forms["stevilo"]
    tip_vnosa = bottle.request.forms["tip"]
    baza.nov_vnos_shrani(dimenzija,int(stevilo),tip_vnosa)
    program.ponastavi_velikosti()
    bottle.redirect('/' + tip + '/aktivno/')

@bottle.post('/<tip>/aktivno/dodaj_iz_datoteke/')
def aktivno_dodaj_iz_datoteke(tip):
    global program
    baza = program.vrni_aktivno_bazo(tip)
    datoteka = bottle.request.files.get("file_path")
    baza.ponastavi_na_zacetno_stanje()
    besedilo = baza.dodaj_iz_datoteke(datoteka.file)
    print(besedilo)
    bottle.redirect('/' + tip + '/aktivno/')

@bottle.post('/<tip>/aktivno/popravljanje_vnosa/')
def aktivno_popravi_vnos(tip):
    global program
    index_vnosa = int(bottle.request.forms["index"])
    baza = program.vrni_aktivno_bazo(tip)
    vnos = baza.slovar["vnosi"][index_vnosa]
    nov_tip = bottle.request.forms["tip"]
    novo_stevilo = bottle.request.forms["stevilo"]
    if nov_tip != vnos["tip"]:
        baza.poprava_vnosa(index_vnosa,"poprava_tipa")
    if novo_stevilo != vnos["stevilo"]:
        baza.poprava_vnosa(index_vnosa,"poprava_stevila", int(novo_stevilo))
    bottle.redirect('/' + tip + '/aktivno/')

@bottle.post('/<tip>/aktivno/izbris_vnosa/<index_vnosa>')
def aktivno_izbris_vnosa(tip,index_vnosa):
    global program
    index_vnosa = int(index_vnosa)
    baza = program.vrni_aktivno_bazo(tip)
    baza.poprava_vnosa(index_vnosa,"izbris")
    bottle.redirect('/' + tip + '/aktivno/')

@bottle.post('/<tip>/aktivno/uveljavi_bazo/')
def aktivno_uveljavi_bazo(tip):
    global program
    baza = program.vrni_aktivno_bazo(tip)
    if tip == "prevzem":
        program.zaloga.dodaj_iz_baze(baza)
    elif tip == "dnevna_prodaja" or tip == "vele_prodaja" or tip == "odpis":
        program.zaloga.odstrani_iz_baze(baza)
    program.v_arhiv(baza)
    program.zaloga.dodaj_v_arhiv(baza)
    bottle.redirect('/' + tip + '/arhiv/')


@bottle.get('/<tip>/arhiv/')
def arhiv(tip):
    global program
    return bottle.template('arhiv.tpl', program = program, tip = tip)

@bottle.get('/<tip>/cenik/')
def cenik(tip):
    global program
    return bottle.template('cenik.tpl', program = program, tip = tip)

@bottle.post('/<tip>/cenik/spremeni_ceno/')
def spremeni_ceno(tip):
    global program
    tip_dimenzije = bottle.request.forms["tip"]
    dimenzija = bottle.request.forms["dimenzija"]
    cena = int(bottle.request.forms["nova_cena"])
    program.spremeni_ceno(tip,dimenzija,tip_dimenzije,cena)
    bottle.redirect('/' + tip + '/cenik/')

@bottle.get('/<tip>/arhiv/vpogled/<ime>')
def arhiv_vpogled(tip,ime):
    global program
    path_baze = program.vrni_path_arhiva(tip)
    baza = program.vrni_bazo(path_baze,ime)
    if "spremeni" in bottle.request.query:
        if "spremeni" != "false" or "spremeni" != "no":
            index = int(bottle.request.query["spremeni"])
            return bottle.template('arhiv_vpogled.tpl',program = program, tip = tip, baza = baza, spremeni = True, index = index)
        else:
            return bottle.template('arhiv_vpogled.tpl', program = program, tip = tip, baza = baza, spremeni = False)
    else:
        return bottle.template('arhiv_vpogled.tpl', program = program, tip = tip, baza = baza, spremeni = False)

@bottle.post('/<tip>/arhiv/vpogled/<ime>/sprememba_vnosa/<index>')
def arhiv_sprememba_vnosa(tip,ime,index):
    global program
    baza = program.vrni_bazo(program.vrni_path_arhiva(tip),ime)
    vnos = baza.slovar["vnosi"][int(index)]
    nov_tip = bottle.request.forms["tip"]
    novo_stevilo = bottle.request.forms["stevilo"]
    if nov_tip != vnos["tip"]:
        baza.poprava_vnosa(int(index),"poprava_tipa")
    if novo_stevilo != vnos["stevilo"]:
        baza.poprava_vnosa(int(index),"poprava_stevila", int(novo_stevilo))         
    if baza.tip == "prevzem":
        program.zaloga.odstrani_stevilo(vnos["dimenzija"],vnos["tip"],vnos["stevilo"])
        program.zaloga.dodaj_stevilo(vnos["dimenzija"],nov_tip,novo_stevilo) 
    elif baza.tip == "dnevna_prodaja" or baza.tip == "vele_prodaja" or baza.tip == "odpis":
        program.zaloga.dodaj_stevilo(vnos["dimenzija"],vnos["tip"],vnos["stevilo"])
        program.zaloga.odstrani_stevilo(vnos["dimenzija"],nov_tip,novo_stevilo)    
    bottle.redirect('/' + tip + '/arhiv/vpogled/' + ime)

@bottle.post('/<tip>/arhiv/vpogled/<ime>/izbris_vnosa/<index>')
def arhiv_izbris_vnosa(tip,ime,index):
    global program
    baza = program.vrni_bazo(program.vrni_path_arhiva(tip),ime)
    vnos = baza.slovar["vnosi"][int(index)]
    baza.poprava_vnosa(int(index),"izbris")
    if baza.tip == "prevzem":
        program.zaloga.odstrani_stevilo(vnos["dimenzija"],vnos["tip"],vnos["stevilo"])
    elif baza.tip == "dnevna_prodaja" or baza.tip == "vele_prodaja" or baza.tip == "odpis":
        program.zaloga.dodaj_stevilo(vnos["dimenzija"],vnos["tip"],vnos["stevilo"])
    bottle.redirect('/' + tip + '/arhiv/vpogled/' + ime)
####################################################################################################
@bottle.get('/dnevna_prodaja/')
def dnevna_prodaja():
    global program
    return bottle.template("dnevna_prodaja.tpl", program = program)

@bottle.get('/inventura/primerjava_stanja/')
def inventura_primerjava_stanja():
    global program
    baza = program.vrni_aktivno_bazo("inventura")
    if baza == None:
        bottle.redirect('/inventura/aktivno/')
    else:
        if "radius" in bottle.request.query:
            order = bottle.request.query["order"]
            radius = bottle.request.query["radius"]
            height = bottle.request.query["height"]
            width = bottle.request.query["width"]
            if order == "numeric":
                dimenzije = program.filtrirane_dimenzije(radius,height,width)
            elif order == "alphabetic":
                dimenzije = sorted(program.filtrirane_dimenzije(radius,height,width))
        else:
            dimenzije = program.tvorjene_dimenzije
        return bottle.template('primerjava_stanja.tpl',program=program,baza=baza,dimenzije=dimenzije,ohrani=False)

@bottle.post('/inventura/primerjava_stanja/uveljavi_inventuro/<ohrani>')
def uveljavi_inventuro_ohrani(ohrani):
    global program
    baza = program.vrni_aktivno_bazo("inventura")
    if ohrani == "true":
        program.zaloga.uveljavi_inventuro(baza,True)
        program.v_arhiv(baza)
        program.zaloga.dodaj_v_arhiv(baza)
        bottle.redirect('/inventura/arhiv/')
    elif ohrani == "false":
        program.zaloga.uveljavi_inventuro(baza)
        program.v_arhiv(baza)
        program.zaloga.dodaj_v_arhiv(baza)
        bottle.redirect('/inventura/arhiv/')
 
####################################################################################################
@bottle.get('/vele_prodaja/stranke/')
def vele_prodaja_stranke():
    global program
    return bottle.template('pregled_strank.tpl', program=program)

@bottle.post('/vele_prodaja/stranke/spremeni_stranko/')
def spremeni_stranko():
    global program
    index_stranke = int(bottle.request.forms["index"])
    slovar_sprememb = {
        "ime": bottle.request.forms["ime"],
        "telefon": bottle.request.forms["telefon"],
        "e-mail": bottle.request.forms["mail"],
        "boniranje": bottle.request.forms["boniranje"]
    }
    program.spremeni_stranko(index_stranke,slovar_sprememb)
    bottle.redirect('/vele_prodaja/stranke/')

@bottle.post('/vele_prodaja/stranke/dodaj_stranko/')
def dodaj_stranko():
    global program
    ime = bottle.request.forms["ime"]
    telefon = bottle.request.forms["telefon"]
    mail = bottle.request.forms["mail"]
    boniranje = bottle.request.forms["boniranje"]
    program.dodaj_stranko(ime,telefon,mail,boniranje)
    bottle.redirect('/vele_prodaja/stranke/')

@bottle.post('/vele_prodaja/stranke/odstrani_stranko/')
def odstrani_stranko():
    global program
    index_stranke = int(bottle.request.forms["index"])
    program.odstrani_stranko(index_stranke)
    bottle.redirect('/vele_prodaja/stranke/')

####################################################################################################

@bottle.get('/radius_meni/')
def radius_meni():
    global program
    if program.delovna_baza != None:
        if program.radius != None:
            if program.height != None:
                if program.width != None:
                    bottle.redirect('/amount_meni/')
                else:
                    bottle.redirect('/width_meni/')
            else:
                bottle.redirect('/height_meni/')
        else:
            return bottle.template('radius_meni.tpl', program = program)
    else:
        bottle.redirect('/zaloga_meni/')
    

@bottle.post('/radius_meni/klik_gumba/<radius>')
def klik_gumba_radius(radius):
    global program
    program.nastavi_radius(radius)
    bottle.redirect('/height_meni/')

@bottle.post('/radius_meni/nazaj')
def radius_nazaj():
    global program
    program.doloci_delovno_bazo(None)
    bottle.redirect(program.zacetna_stran)

####################################################################################################

@bottle.get('/height_meni/')
def height_meni():
    global program
    if program.delovna_baza != None:
        if program.radius != None:
            if program.height != None:
                if program.width!= None:
                    bottle.redirect('/amount_meni/')
                else:
                    bottle.redirect('/width_meni/')
            else:
                return bottle.template('height_meni.tpl', program = program)
        else:
            bottle.redirect('/radius_meni/')
    else:
        bottle.redirect('/zaloga_meni/')

@bottle.post('/height_meni/klik_gumba/<height>')
def klik_gumba_height(height):
    global program
    program.nastavi_height(height)
    bottle.redirect('/width_meni/')

@bottle.post('/height_meni/nazaj')
def height_nazaj():
    global program
    program.nastavi_radius(None)
    bottle.redirect('/radius_meni/')

####################################################################################################

@bottle.get('/width_meni/')
def width_meni():
    global program
    if program.delovna_baza != None:
        if program.radius != None:
            if program.height != None:
                if program.width!= None:
                    bottle.redirect('/amount_meni/')
                else:
                    return bottle.template('width_meni.tpl', program = program)
            else:
                bottle.redirect('/height_meni/')
        else:
            bottle.redirect('/radius_meni/')
    else:
        bottle.redirect('/zaloga_meni/')

@bottle.post('/width_meni/klik_gumba/<width>')
def klik_gumba_width(width):
    global program
    program.nastavi_width(width)
    bottle.redirect('/amount_meni/')

@bottle.post('/width_meni/nazaj')
def width_nazaj():
    global program
    program.nastavi_height(None)
    bottle.redirect('/height_meni/')

##################################################################################################

@bottle.get('/amount_meni/')
def amount_meni():
    global program
    if program.delovna_baza != None:
        if program.radius != None:
            if program.height != None:
                if program.width!= None:
                    return bottle.template('amount_meni.tpl', program = program, tip = "")
                else:
                    bottle.redirect('/width_meni/')
            else:
                bottle.redirect('/height_meni/')
        else:
            bottle.redirect('/radius_meni/')
    else:
        bottle.redirect('/zaloga_meni')

@bottle.post('/amount_meni/klik_gumba/')
def amount_klik_gumba():
    global program
    dimenzija = program.tvori_dimenzijo(program.radius,program.height,program.width)
    tip = bottle.request.forms["tip"]
    stevilo = bottle.request.forms["stevilo"]
    program.delovna_baza.nov_vnos_shrani(dimenzija,int(stevilo),tip)
    program.ponastavi_velikosti()
    bottle.redirect('/radius_meni/')

@bottle.post('/amount_meni/nazaj')
def amount_nazaj():
    global program
    program.nastavi_width(None)
    bottle.redirect('/width_meni/')

bottle.run(debug=True, reloader=True)