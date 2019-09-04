<html>
<head>
    <title>Aktivni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    %if program.vrni_aktivno_bazo(tip) == None:
        %if tip == "inventura":
        <div style="position:absolute;left:10%;top:20%;width:80%;height:20%;border:1px solid black">
            <form style="width:100%;height:100%" action={{"/" + tip + "/aktivno/nova_baza/"}} method="post">
                <div style="position:absolute;top:0%;width:38%;height:100%;left:2%;font-size:5vh">
                    %stevilo_inventur = len(program.zaloga.baza.slovar["inventure"])
                    % ime = str(stevilo_inventur + 1) + ".inventura"
                    <p style="margin:5%">
                        Index: {{ime}}
                    <p>
                </div>
                <div style="position:absolute;width:40%;height:100%;left:40%;font-size:5vh">
                    <p style="margin:5%" >
                        Datum: <input id="datum" style="height:5vh" type="date" name="datum" min="2019-01-01" max="2021-01-01" value={{program.vrni_danes()}}>
                    </p>
                </div>
                <div style="position:absolute;top:0%;width:20%;height:100%;left:80%">
                    <input style="position:absolute;top:20%;width:80%;height:60%;left:10%" id="potrdi" type="submit" value="nova inventura">
                </div>
            </form>
        </div>
        %elif tip == "prevzem":
            <div style="position:absolute;left:10%;top:20%;width:80%;height:20%;border:1px solid black">
                <form style="width:100%;height:100%" action={{"/" + tip + "/aktivno/nova_baza/"}} method="post">
                    <div style="position:absolute;top:0%;width:38%;height:100%;left:2%;font-size:5vh">
                        <p style="margin:5%">
                            Kontejner: <input id="kontejner" style="height:5vh" autocomplete="off" type="text" name="kontejner">
                        <p>
                    </div>
                    <div style="position:absolute;width:40%;height:100%;left:40%;font-size:5vh">
                    <p style="margin:5%" >
                        Datum: <input id="datum" style="height:5vh" type="date" name="datum" min="2019-01-01" max="2021-01-01" value={{program.vrni_danes()}}>
                    </p>
                    </div>
                    <div style="position:absolute;top:0%;width:20%;height:100%;left:80%">
                        <input style="position:absolute;top:20%;width:80%;height:60%;left:10%" id="potrdi" type="submit" value="nov prevzem">
                    </div>
                </form>
            </div>
        %elif tip == "dnevna_prodaja":
            <div style="position:absolute;left:10%;top:20%;width:80%;height:20%;border:1px solid black">
                <form style="width:100%;height:100%" action={{"/" + tip + "/aktivno/nova_baza/"}} method="post">
                    <div style="position:absolute;top:0%;width:38%;height:100%;left:2%;font-size:5vh">
                        <p style="margin:5%" >
                            Datum: <input id="datum" style="height:5vh" type="date" name="datum" min="2019-01-01" max="2021-01-01" value={{program.vrni_danes()}}>
                        </p>
                    </div>
                    <div style="position:absolute;width:40%;height:100%;left:40%;font-size:5vh">
                    </div>
                    <div style="position:absolute;top:0%;width:20%;height:100%;left:80%">
                        <input style="position:absolute;top:20%;width:80%;height:60%;left:10%" id="potrdi" type="submit" value="nova prodaja">
                    </div>
                </form>
            </div>
        %elif tip == "vele_prodaja":
            <div style="position:absolute;left:10%;top:20%;width:80%;height:20%;border:1px solid black">
                <form style="width:100%;height:100%" action={{"/" + tip + "/aktivno/nova_baza/"}} method="post">
                    <div style="position:absolute;top:0%;width:26%;height:100%;left:2%;font-size:4vh">
                        <p style="margin:4%" >
                            Faktura:  <label for="faktura">{{program.slovar["naslednja_faktura"]}}</label>
                        </p>
                        <p style="margin:4%" >
                            Datum: <input id="datum" style="height:4vh" type="date" name="datum" min="2019-01-01" max="2021-01-01" value={{program.vrni_danes()}}>
                        </p>
                        <p style="margin:4%" >
                            Stranka: 
                            <select name="stranka" id="stranka" style="height:4vh">
                                %for stranka in program.stranke["stranke"]:
                                    <option value={{stranka["ime"]}}> {{stranka["ime"]}} </option>
                                %end
                            </select>
                        </p>
                    </div>
                    <div style="position:absolute;width:28%;height:100%;left:30%;font-size:4vh">
                        <p style="margin:4%" >
                            Email:  
                        </p>
                        <p style="margin:4%" >
                            Telefon:  
                        </p>
                        <p style="margin:4%" >
                            TRR:
                        </p>
                    </div>
                    <div style="position:absolute;top:0%;width:20%;height:100%;left:80%">
                        <input style="position:absolute;top:20%;width:80%;height:60%;left:10%" id="potrdi" type="submit" value="nova prodaja">
                    </div>
                </form>          
            </div>
        %elif tip == "odpis":
            <div style="position:absolute;left:10%;top:20%;width:80%;height:20%;border:1px solid black">
                <form style="width:100%;height:100%" action={{"/" + tip + "/aktivno/nova_baza/"}} method="post">
                    <div style="position:absolute;top:0%;width:38%;height:100%;left:2%;font-size:5vh">
                        <p style="margin:5%" >
                            Datum: <input id="datum" style="height:5vh" type="date" name="datum" min="2019-01-01" max="2021-01-01" value={{program.vrni_danes()}}>
                        </p>
                    </div>
                    <div style="position:absolute;width:40%;height:100%;left:40%;font-size:5vh">
                    </div>
                    <div style="position:absolute;top:0%;width:20%;height:100%;left:80%">
                        <input style="position:absolute;top:20%;width:80%;height:60%;left:10%" id="potrdi" type="submit" value="nov odpis">
                    </div>
                </form>
            </div>
        %end
    %else:
        %baza = program.vrni_aktivno_bazo(tip)
        <div class="okno">
            <div>
                Ime: {{baza.ime}}
                <input style="width:20%;height:30%" id="spremeni_kontejner" type="submit" value="spremeni">
            </div>
        </div>
        <div class="delovno_okno" id="popravljanje" hidden="hidden">
            %slovar = baza.slovar["vnosi"]
            <form action={{"/" + tip + "/aktivno/popravljanje_vnosa/"}} method="post">
                <input id="index_vnosa" type="hidden" name="index" value="">
                index: <label id="index_label" > a </label>
                dimenzija: <label id="dimenzija_label" > a </label>
                stevilo: <input id="stevilo_vnosa" autocomplete="off" type="text" name="stevilo" value="">
                tip: 
                <select id="tip_vnosa" name="tip">
                    <option value="yellow"> Yellow </option>
                    <option value="white"> White </option>
                </select>
                <input id="potrdi" type="submit" value="spremeni">
            </form>
            <button onClick="SkrijPopravljanja()"> preklici </button>
        </div>
        <div class="delovno_okno" id="delovno">
            <form style="height:100%;width:30%" action={{"/" + tip + "/aktivno/preusmeri_na_radius/"}} method="post">
                <input style="height:100%;width:100%"  id="dodaj" type="submit" value="dodaj">
            </form>
            %if tip == "inventura":
                <form style="position:absolute;top:0%;left:32%;height:100%;width:30%" action={{"/inventura/primerjava_stanja/"}} method="get">
                    <input style="height:100%;width:100%" id="primerjava" type="submit" value="primerjava stanja">
                </form>
            %else:
                <form style="position:absolute;top:0%;left:32%;height:100%;width:30%" action={{"/" + tip + "/aktivno/uveljavi_bazo/"}} method="post">
                    <input style="height:100%;width:100%" id="uveljavi" type="submit" value="uveljavi">
                </form>
            %end
            <form enctype='multipart/form-data' style="position:absolute;top:0%;left:65%;height:100%;width:30%" action={{"/" + tip + "/aktivno/dodaj_iz_datoteke/"}} method="post">
                <input style="position:absolute;left:0%;top:0%;height:100%;width:60%" id="iz_datoteke" name="file_path" type="file" value="Brskaj">
                <input type="submit" style="position:absolute;left:60%;top:0%;height:100%;width:40%" value="dodaj">
            </form>
        </div>


        <table class="tabela_vnosov" frame=border rules=all>
            <tr class="header">
                <th width="10% class="index">
                    Št.
                </th>
                <th width="30%" class="dimenzija">
                    Dimenzija:
                </th>
                <th width="14% class="število">
                    Število:
                </th>
                <th width="22%" class="tip">
                    Tip:
                </th> 
                <th width="18%" class="uredi">
                    Uredi:
                </th>  
                <th width="6%" class="brisi">
                    X
                </th>    
            </tr>
            %slovar = baza.slovar["vnosi"]
            %for vnos in slovar:
                <tr class="vnos">
                    <td class="index">
                        {{str(vnos["index"]) + "."}} 
                    </td>
                    <td class="dimenzija">
                        {{vnos["dimenzija"]}}
                    </td>
                    <td class="stevilo">
                        {{vnos["stevilo"]}}
                    </td>
                    %if vnos["tip"] == "yellow":
                        <td bgcolor="yellow" class="tip">
                            yellow
                        </td> 
    	            %elif vnos["tip"] == "white":
                        <td bgcolor="white" class="tip">
                            white
                        </td>
                    %end
                    <td class="uredi">
                        %index_vnosa = str(slovar.index(vnos))
                        %stevilo = str(vnos["stevilo"])
                        %tip = vnos["tip"]
                        %dimenzija = vnos["dimenzija"]
                        %print(dimenzija)
                        <button style="height:5vh;width:100%" id="uredi" onclick="UrediVnos('{{index_vnosa}}', '{{dimenzija}}', '{{stevilo}}', '{{tip}}')"> Uredi </button>
                    </td> 
                    <td class="brisi">
                        %index_vnosa = str(slovar.index(vnos))
                        <form style="position:relative;left:5%;width:90%;height:5vh" action={{'/' + tip + '/aktivno/izbris_vnosa/' + index_vnosa}} method="post">
                            <input type="submit" value="X" style="width:100%;height:100%"> 
                        </form>
                    </td>  
                </tr>
            %end
        </table>
    %end

    <script>
        function UrediVnos(index_vnosa, dimenzija, stevilo, tip) {
            document.getElementById("delovno").style.display = "none";
            document.getElementById("index_vnosa").value = index_vnosa;
            document.getElementById("stevilo_vnosa").value = stevilo;
            document.getElementById("dimenzija_label").innerHTML = dimenzija;
            document.getElementById("index_label").innerHTML = index_vnosa;
            var tip_box = document.getElementById("tip_vnosa")
            if (tip == "yellow"){
                tip_box.selectedIndex = 0
            } else {
                tip_box.selectedIndex = 1
            }
            document.getElementById("popravljanje").style.display = "block";
        };
        function SkrijPopravljanja(index_vnosa, dimenzija, stevilo, tip) {
            document.getElementById("delovno").style.display = "block";
            document.getElementById("popravljanje").style.display = "none";  
        };
    </script>
</body>
</html>