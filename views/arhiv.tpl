<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <table class="tabela_baz" frame=border rules=all>
            <tr class="header">
                <th width="8% class="index">
                    Št.
                </th>
                <th width="31%" class="kontejner">
                    Kontejner:
                </th>
                <th width="30% class="datum">
                    Datum:
                </th>
                <th width="6%" class="yellow">
                    Y
                </th> 
                <th width="6%" class="white">
                    W
                </th> 
                <th width="6%" class="total">
                    T
                </th>  
                <th width="13%" class="vpogled">
                    Vpogled:
                </th>  
            </tr>
            %n=0
            %for  baza in program.zaloga.baza.slovar[program.zaloga.zamenjaj_v_mnozino(tip)]:
                %n+=1
                %baza = program.vrni_bazo(program.vrni_path_arhiva(tip),baza)
                %baza.nalozi()
                <tr class="baza">
                    <td class="index">
                        {{str(n) + '.'}} 
                    </td>
                    <td class="kontejner">
                        {{baza.ime}}
                    </td>
                    <td class="datum">
                        {{baza.datum}}
                    </td>
                    <td class="yellow">
                        {{baza.skupno_stevilo("yellow")}}
                    </td> 
                    <td class="white">
                        {{baza.skupno_stevilo("white")}}
                    </td>
                    <td class="total">
                        {{baza.skupno_stevilo()}}
                    </td>
                    <td class="uredi">
                        <form style="width:100%;height:6vh" action={{'/' + tip + '/arhiv/vpogled/' + baza.ime_datoteke}}>
                        <input style="width:100%;height:100%" type="submit" value="vpogled">
                        </form>
                    </td>  
                </tr>
            %end
        </table>
</body>
</html>