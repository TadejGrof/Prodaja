<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div style="position:absolute;width:60%;height:15%;left:20%;top:15%;font-size:8vh;text-align:center">
        %if tip == "dnevna_prodaja":
            Cenik dnevne prodaje
        %elif tip == "vele_prodaja":
            Cenik vele prodaje
        %end
    </div>
    <table class="pregled_prometa_table" frame=border rules=all>
        <tr class="header">
            <th width="30%">
                Dimenzija:
            </th>
            <th width="18%" style="background-color:yellow">
                Yellow:
            </th>
            <th width="17%" >
                Spremeni:
            </th>
            <th width="18%" style="background-color:white">
                White:  
            </th> 
            <th width="17%">
                Spremeni:
            </th>  
        </tr>
        %cenik = program.cenik
        %for dimenzija in cenik:
            <tr>
                <td>
                    {{dimenzija}} 
                </td>
                <td>
                    <div id={{dimenzija + "-FY"}} hidden="hidden" style="width:100%;height:4vh">
                        <form action={{"/" + tip + "/cenik/spremeni_ceno/"}} method="post">
                            <input style="position:relative;top:-0.5vh;width:60%;height:4vh" type="text" value="" name="nova_cena"> $
                            <input type="hidden" value="yellow" name="tip">
                            <input type="hidden" value={{dimenzija}} name="dimenzija">
                            <input type="submit" id={{dimenzija + "-BY"}} hidden="hidden" value="">
                        </form> 
                    </div>
                    <div id={{dimenzija + "-CY"}}>
                        {{str(cenik[dimenzija][tip][0]) + " $"}}
                    </div>
                </td>
                <td>
                    <div style="width:100%;height:4vh">
                        <div id="{{dimenzija + "-SY" }}" style="width:100%;height:4vh">
                            <button   style="width:100%;height:4vh" onclick="SpremeniCeno('{{dimenzija}}', 'yellow')"> Spremeni </button>                
                        </div>
                        <div id={{dimenzija + "-UY"}} hidden="hidden" style="width:60%;height:4vh">
                            <button  style="width:100%;height:4vh" onclick="UveljaviNovoCeno('{{dimenzija}}', 'yellow')"> Uveljavi </button>
                        </div>
                        <div id="{{dimenzija + "-PY" }}" hidden="hidden" style="position:relative;left:60%;top:-4vh;width:40%;height:4vh">    
                            <button  style="width:100%;height:4vh" onclick="PrekliciNovoCeno('{{dimenzija}}', 'yellow')"> X </button>
                        </div>
                    </div>
                </td>
                <td >
                    <div id={{dimenzija + "-FW"}} hidden="hidden" style="width:100%;height:4vh">
                        <form action={{"/" + tip + "/cenik/spremeni_ceno/"}} method="post">
                            <input style="position:relative;top:-0.5vh;width:60%;height:4vh" type="text" value="" name="nova_cena"> $
                            <input type="hidden" value="white" name="tip">
                            <input type="hidden" value={{dimenzija}} name="dimenzija">
                            <input type="submit" id={{dimenzija + "-BW"}} hidden="hidden" value="">
                        </form> 
                    </div>
                    <div id={{dimenzija + "-CW"}}>
                        {{str(cenik[dimenzija][tip][1]) + " $"}}
                    </div>
                </td> 
                <td>
                    <div style="width:100%;height:4vh">
                        <div id="{{dimenzija + "-SW" }}" style="width:100%;height:4vh">
                            <button style="width:100%;height:4vh" onclick="SpremeniCeno('{{dimenzija}}', 'white')"> Spremeni </button>                
                        </div>
                        <div id={{dimenzija + "-UW"}} hidden="hidden" style="width:60%;height:4vh">
                            <button  style="width:100%;height:4vh" onclick="UveljaviNovoCeno('{{dimenzija}}', 'white')"> Uveljavi </button>
                        </div>
                        <div id="{{dimenzija + "-PW" }}" hidden="hidden" style="position:relative;left:60%;top:-4vh;width:40%;height:4vh">    
                            <button  style="width:100%;height:4vh" onclick="PrekliciNovoCeno('{{dimenzija}}', 'white')"> X </button>
                        </div>
                    </div>
                </td>
            </tr>
        %end
    </table>
    <script>
        function SpremeniCeno(dimenzija, tip) {
            if ( tip == "yellow"){
                var cenaid = dimenzija.concat("-CY")
                var formid = dimenzija.concat("-FY")
                var spremeniid = dimenzija.concat("-SY")
                var prekliciid = dimenzija.concat("-PY")
                var uveljaviid = dimenzija.concat("-UY") 
            }else{
                var cenaid = dimenzija.concat("-CW")
                var formid = dimenzija.concat("-FW")
                var spremeniid = dimenzija.concat("-SW")
                var prekliciid = dimenzija.concat("-PW")
                var uveljaviid = dimenzija.concat("-UW")  
            }
            document.getElementById(cenaid).style.display="none";
            document.getElementById(formid).style.display="block";   
            document.getElementById(spremeniid).style.display="none";
            document.getElementById(prekliciid).style.display="block";  
            document.getElementById(uveljaviid).style.display="block";
        };
        function UveljaviNovoCeno(dimenzija, tip) {
            if ( tip == "yellow"){
                var buttonid = dimenzija + "-BY"
                document.getElementById(buttonid).click();    
            }else{
                var buttonid = dimenzija + "-BW"
                document.getElementById(buttonid).click();  
            }
        };
        function PrekliciNovoCeno(dimenzija, tip) {
            if ( tip == "yellow"){
                var cenaid = dimenzija.concat("-CY")
                var formid = dimenzija.concat("-FY")
                var spremeniid = dimenzija.concat("-SY")
                var prekliciid = dimenzija.concat("-PY")
                var uveljaviid = dimenzija.concat("-UY")
            }else{
                var cenaid = dimenzija.concat("-CW")
                var formid = dimenzija.concat("-FW")
                var spremeniid = dimenzija.concat("-SW")
                var prekliciid = dimenzija.concat("-PW")
                var uveljaviid = dimenzija.concat("-UW")
            };
            document.getElementById(cenaid).style.display="block";
            document.getElementById(formid).style.display="none";   
            document.getElementById(spremeniid).style.display="block";
            document.getElementById(prekliciid).style.display="none";  
            document.getElementById(uveljaviid).style.display="none"; 
        };
        
    </script>
</body>
</html>