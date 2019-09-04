<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div style="position:absolute;width:80%;height:10%;left:10%;top:15%;text-align:center;font-size:5vmin">
        PRIMERJAVA STANJA
    </div>
    <div style="position:absolute;width:14%;height:60%;top:30%;left:3%">
        <form style="position:absolute;width:100%;height:20%;top:0%;left:0%" action="/inventura/primerjava_stanja/" method="get">
            <input type="hidden" name="ohrani" value="true">
            <input style="width:100%;height:100%"  type="submit" value="ohrani nenapisane">
        </form>
        <form style="position:absolute;width:100%;height:20%;top:25%;left:0%" action="/inventura/primerjava_stanja/" method="get">
            <input type="hidden" name="ohrani" value="false">
            <input style="width:100%;height:100%"  type="submit" value="nenapisane na 0">
        </form>
        <form style="position:absolute;width:100%;height:20%;top:50%;left:0%" action="/inventura/aktivno/" method="get">
            <input style="width:100%;height:100%" type="submit" value="popravi inventuro">
        </form>
        %if ohrani:
            <form style="position:absolute;width:100%;height:20%;top:75%;left:0%" action="/inventura/primerjava_stanja/uveljavi_inventuro/true" method="post">
                <input style="width:100%;height:100%" type="submit" value="uveljavi inventuro">
            </form>
        %else:
            <form style="position:absolute;width:100%;height:20%;top:75%;left:0%" action="/inventura/primerjava_stanja/uveljavi_inventuro/false" method="post">
                <input style="width:100%;height:100%" type="submit" value="uveljavi inventuro">
            </form>
        %end
    </div>
    <div style="position:absolute;width:60%;height:5%;top:25%;left:20%">
        %include('dinamic_select.tpl',action='/inventura/primerjava_stanja/')
    </div>
    <table class="tabela_zaloge" style="top:35%">
            <tr class="header">
                <th width="30% class="dimenzija">
                    Dimenzija:
                </th>
                <th width="20%" class="tip">
                    Tip:
                </th>
                <th width="20% class="prvotno_stevilo">
                    Prvotno stanje:
                </th>
                <th width="20%" class="inventurno_stevilo">
                    Inventurno stanje:
                </th>
                <th width="10%" class="razlika">
                    Razlika:
                </th>
            </tr>
            %slovar = baza.slovar["dimenzije"]
            %for dimenzija in dimenzije:
                <tr class="yellow">
                    <td class="dimenzija" rowspan="2">
                        {{dimenzija}}
                    </td>
                    <td class="tip" bgcolor="yellow">
                        yellow
                    </td>
                    <td class="prvotno_stevilo">
                        %prvotno_stevilo = program.zaloga.baza.slovar["dimenzije"][dimenzija][0]
                        {{str(prvotno_stevilo)}}
                    </td>
                    <td class="inventurno_stevilo">
                        %if ohrani:
                            %inventurno_stevilo = None
                            %for vnos in baza.slovar["vnosi"]:
                                %if vnos["dimenzija"] == dimenzija and vnos["tip"] == "yellow":
                                    %inventurno_stevilo = slovar[dimenzija][0]
                                    %break
                                %end
                            %end
                            %if inventurno_stevilo == None:
                                %inventurno_stevilo = prvotno_stevilo
                            %end
                            {{str(inventurno_stevilo)}}
                        %else:
                            %inventurno_stevilo = slovar[dimenzija][0]
                            {{str(inventurno_stevilo)}}
                        %end
                    </td>
                    <td class="razlika" style="border-right: 2px solid black">
                        %if inventurno_stevilo - prvotno_stevilo > 0:
                            {{"+" + str(inventurno_stevilo - prvotno_stevilo)}}
                        %else:
                            {{str(inventurno_stevilo - prvotno_stevilo)}}
                        %end
                    </td>
                </tr>
                <tr class="white">
                    <td class="tip" bgcolor="white" style="border-bottom: 2px solid black">
                        white
                    </td>
                    <td class="prvotno_stevilo" style="border-bottom: 2px solid black">
                        %prvotno_stevilo = program.zaloga.baza.slovar["dimenzije"][dimenzija][1]
                        {{str(prvotno_stevilo)}}
                    </td>
                    <td class="inventurno_stevilo" style="border-bottom: 2px solid black">
                        %if ohrani:
                            %inventurno_stevilo = None
                            %for vnos in baza.slovar["vnosi"]:
                                %if vnos["dimenzija"] == dimenzija and vnos["tip"] == "white":
                                    %inventurno_stevilo = slovar[dimenzija][1]
                                    %break
                                %end
                            %end
                            %if inventurno_stevilo == None:
                                %inventurno_stevilo = prvotno_stevilo
                            %end
                            {{str(inventurno_stevilo)}}
                        %else:
                            %inventurno_stevilo = slovar[dimenzija][1]
                            {{str(inventurno_stevilo)}}
                        %end
                    </td>
                    <td class="razlika" style="border-bottom: 2px solid black;border-right: 2px solid black">
                       %if inventurno_stevilo - prvotno_stevilo > 0:
                            {{"+" + str(inventurno_stevilo - prvotno_stevilo)}}
                        %else:
                            {{str(inventurno_stevilo - prvotno_stevilo)}}
                        %end
                    </td>
                </tr>
            %end
    </table>
</body>
</html>