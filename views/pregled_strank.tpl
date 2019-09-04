<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div style="position:absolute;left:20%;top:15%;height:10%;width:60%">
        <form action="/vele_prodaja/stranke/dodaj_stranko/" method="post">
            <fieldset>
                    <legend> Nova stranka </legend>
                    ime stranke : <input type="text" autocomplete="off" id="ime" name="ime" value="" placeholder="ime" required>
                    telefon: <input type="text" autocomplete="off" id="telefon" name="telefon" value="" placeholder="telefon" >  <br>
                    e-mail: <input type="text" autocomplete="off" id="e-mail" name="mail" value="" placeholder="mail"  >
                    boniranje: <input type="text" autocomplete="off" id="boniranje" name="boniranje" value="" placeholder="boniranje" required><br>
                    <input type="submit" style="position:absolute;height:70%;width:20%;left:70%;top:45%" value="dodaj stranko" id="potrdi">
            </fieldset>
        </form>
    </div>
    <p style="position:absolute;width:80%;left:10%;height:5%;top:28%;text-align:center;font-size:5vh">
        OBSTOJEČE STRANKE
    </p>
    %top = 40
    %for stranka in program.stranke["stranke"]:
        <div style="position:absolute;width:80%;left:10%;height:10%;top:{{str(top) + "%"}}">
            <form stlye="width:100%;height:100%" action="/vele_prodaja/stranke/spremeni_stranko/" method="post">
                <fieldset>
                    <legend> {{stranka["index"]}} </legend>
                    <input type="hidden" autocomplete="off" id="index" name="index" value={{stranka["index"]}} >
                    ime stranke : <input type="text" autocomplete="off" id="ime" name="ime" value={{stranka["ime"]}} >
                    telefon: <input type="text" autocomplete="off" id="telefon" name="telefon" value={{stranka["telefon"]}} >  <br>
                    e-mail: <input type="text" autocomplete="off" id="e-mail" name="mail" value={{stranka["e-mail"]}} >
                    boniranje: <input type="text" autocomplete="off" id="boniranje" name="boniranje" value={{stranka["boniranje"]}} ><br>
                    stevilo odprtih narocil: <input type="text" value={{str(len(stranka["narocila"]))}} readonly>
                    stevilo nakupov: <input type="text" value={{str(len(stranka["nakupi"]))}} readonly>
                    <input type="submit" style="position:absolute;height:70%;width:15%;left:70%;top:45%" value="spremeni" id="potrdi">
                </fieldset>
            </form>
            <form action="/vele_prodaja/stranke/odstrani_stranko/" method="post">
                <input type="hidden" name="index" value={{str(stranka["index"])}}>
                <input style="position:absolute;height:70%;width:10%;left:88%;top:45%" type="submit" value="izbrisi">
            </form>
        </div>
        
        %top +=18
    %end
</body>
</html>