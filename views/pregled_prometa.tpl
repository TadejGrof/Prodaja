<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div style="position:absolute;left:20%;height:10%;top:18%;width:60%;font-size:5vh;text-align:center">
        Pregled prometa za dimenzijo {{dimenzija}} tipa {{tip}}:
    </div>
    <table class="pregled_prometa_table" frame=border rules=all>
        %if tip == "yellow":
            %stanje = program.zaloga.baza.slovar["dimenzije"][dimenzija][0]
        %elif tip == "white":
            %stanje = program.zaloga.baza.slovar["dimenzije"][dimenzija][1]
        %end

        <tr class="trenutno_stanje">
            <td class="datum">
                {{program.vrni_danes()}} 
            </td>
            <td class="ime" colspan="2">
                Trenutno stanje:
            </td>
            <td class="stanje" colspan="2">
                {{str(stanje)}}
            </td>
        </tr>
        <tr class="header">
            <th width="25% class="datum">
                 Datum
            </th>
            <th width="20%" class="tip">
                Tip prometa:
            </th>
            <th width="25% class="ime">
                Ime:
            </th>
            <th width="15%" class="promet">
                Promet:  
            </th> 
            <th width="15%" class="stanje">
                Stanje:
            </th> 
        </tr>

        %for sprememba in program.zaloga.baza.slovar["spremembe"][::-1]:
            %baza_spremembe = program.vrni_bazo(program.vrni_path_arhiva(sprememba["tip"]),sprememba["ime_datoteke"])
            %if tip == "yellow":
                %int_tip = 0
            %elif tip == "white":
                %int_tip = 1
            %end
            %if baza_spremembe.tip == "inventura": 
                <tr class="baza">
                    <td class="datum">
                        {{sprememba["datum"]}} 
                    </td>
                    <td class="tip">
                        {{baza_spremembe.tip}}
                    </td>
                    <td class="ime">
                        {{baza_spremembe.ime}}
                    </td>
                    <td class="promet">
                        %stanje = baza_spremembe.slovar["dimenzije"][dimenzija][int_tip]
                        {{stanje}}
                    </td> 
                    <td class="skupno_stevilo">
                        {{stanje}}
                    </td>
                </tr>
            %else:
                %if baza_spremembe.slovar["dimenzije"][dimenzija][int_tip] > 0:
                    %je_dimenzija_v_bazi = True   
                %else:
                    %je_dimenzija_v_bazi = False
                %end
                %if je_dimenzija_v_bazi:
                    <tr class="baza">
                        <td class="datum">
                            {{sprememba["datum"]}} 
                        </td>
                        <td class="tip">
                            {{baza_spremembe.tip}}
                        </td>
                        <td class="ime">
                            {{baza_spremembe.ime}}
                        </td>
                        <td class="promet">
                            %if baza_spremembe.tip == "prevzem":
                                %promet = baza_spremembe.slovar["dimenzije"][dimenzija][int_tip]
                                + {{str(promet)}}
                            %else:
                                %promet = baza_spremembe.slovar["dimenzije"][dimenzija][int_tip]
                                - {{str(promet)}}
                            %end
                        </td> 
                        <td class="stanje">
                            {{stanje}}
                            %if baza_spremembe.tip == "prevzem":
                                %stanje += - promet
                            %else:
                                %stanje += + promet
                            %end
                        </td>
                    </tr>
                %end
            %end
        %end
        <tr class="zacetno_stanje">
            <td class="datum">
                2019-08-07 
            </td>
            <td class="ime" colspan="2">
                Začetno stanje:
            </td>
            <td class="stanje" colspan="2">
                0
            </td>
        </tr>
    </table>
</body>
</html>