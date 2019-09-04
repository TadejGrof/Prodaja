<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div style="position:absolute;width:60%;height:5%;top:15%;left:20%">
        %include('dinamic_select.tpl',action='/pregled_zaloge_meni/')
    </div>
    %slovar = program.zaloga.baza.slovar["dimenzije"]
        <table class="tabela_zaloge">
            <tr class="header">
                <th width="30% class="dimenzija">
                    Dimenzija
                </th>
                <th width="25%" class="tip">
                    Tip:
                </th>
                <th width="25% class="total">
                    V skladiscu::
                </th>
                <th width="20%" class="vpogled">
                    Vpogled:
                </th>  
            </tr>
            %for dimenzija in dimenzije:
                    <tr class="yellow">
                        <td class="dimenzija" rowspan="2">
                            {{dimenzija}}
                        </td>
                        <td bgcolor="yellow">
                            yellow
                        </td>
                        <td>
                            {{slovar[dimenzija][0]}}
                        </td>
                        <td style="border-right: 2px solid black">
                            %spremenjena_dimenzija = dimenzija.replace("/","-")
                            <form action={{'/pregled_zaloge_meni/pregled_prometa/' + spremenjena_dimenzija + '/yellow/'}} method="get">
                                <input type="submit" value="pogled prometa">
                            </form>
                        </td>
                    </tr>
                    <tr class="white">
                        <td bgcolor="white" style="border-bottom: 2px solid black">
                            white
                        </td>
                        <td style="border-bottom: 2px solid black"> 
                            {{slovar[dimenzija][1]}}
                        </td>
                        <td style="border-bottom: 2px solid black;border-right: 2px solid black"> 
                            %spremenjena_dimenzija = dimenzija.replace("/","-")
                            <form action={{'/pregled_zaloge_meni/pregled_prometa/' + spremenjena_dimenzija + '/white/'}} method="get">
                                <input type="submit" value="pogled prometa">
                            </form>
                        </td>
                    </tr>
            %end
        </table>
</body>
</html>
