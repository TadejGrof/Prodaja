<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    %if spremeni:
        %vnos = baza.slovar["vnosi"][index]
        <div class="sprememba_vnosa" style="font-size:5vh;position:absolute;width:25%;height:10%;left:40%;top:15%">
            <form style="width:100%;height:100%" method="post" action={{"/" + baza.tip + '/arhiv/vpogled/' + baza.ime_datoteke + '/sprememba_vnosa/' + str(index)}}>
                Dimenzija: {{vnos["dimenzija"]}} <br>
                Stevilo: <input type="text" autocomplete="off" value={{vnos["stevilo"]}} name="stevilo"> <br>
                Tip: <select name="tip">
                    %if vnos["tip"] == "yellow":
                        <option value="yellow" selected="selected"> yellow </option>
                        <option value="white"> white </option>
                    %elif vnos["tip"] == "white":
                        <option value="yellow"> yellow </option>
                        <option value="white" selected="selected"> white </option>
                    %end
                </select> <br>
                <input style="height:60%;width:100%" type="submit" value="spremeni">
            </form>
        </div>
        %top_tabele = 45
    %else:
        %top_tabele = 15
    %end
    <table style="top:{{str(top_tabele) + "%"}}" class="tabela_vnosov_arhiva" frame=border rules=all>
            <tr class="header">
                <th width="10% class="index">
                    Št.
                </th>
                <th width="30%" class="dimenzija">
                    Dimenzija:
                </th>
                <th width="20% class="število">
                    Število:
                </th>
                <th width="20%" class="tip">
                    Tip:
                </th> 
                <th width="13%" class="uredi">
                    Uredi:
                </th>  
                <th width="8%" class="uredi">
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
                        <form style="width:100%;height:5vh" action={{"/" + baza.tip + '/arhiv/vpogled/' + baza.ime_datoteke}} method="get">
                            <input type="hidden" name="spremeni" value={{str(baza.slovar["vnosi"].index(vnos))}}>
                            <input type="submit" value="uredi" style="width:100%;height:100%">
                        </form>
                    </td>  
                    <td class="izbrisi">
                        <form style="width:100%;height:5vh" action={{"/" + baza.tip + '/arhiv/vpogled/' + baza.ime_datoteke + '/izbris_vnosa/' + str(baza.slovar["vnosi"].index(vnos))}} method="post">
                            <input type="submit" value="x" style="width:100%;height:100%">
                        </form>
                    </td>  
                </tr>
            %end
    </table> 

    <script>
        function KlikSpremeni() {
            %if vnos["tip"] == "yellow":
                document.getElementById("tip_vnosa").value = "white"
            %elif vnos["tip"] == "white":
                document.getElementById("tip_vnosa").value = "yellow"
            %end
            document.getElementById("potrdi").click();
        };
    </script>
</body>
</html>
