<html>
<head>
    <title>Dnevna prodaja</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    
    <div id="prodaja" style="position:absolute;width:80%;left:10%;top:15%;height:60%;border:1px solid black">
        <button id="dodaj" onclick="Dodaj()"> Dodaj </button>
        <div id="dodajanje" hidden="hidden" style="position:absolute;width:80%;left:10%;top:15%;height:60%;border:1px solid black">
            <div id="selecti">    
                Radius: <select id="radius" onchange="ChangeRadius(this)">
                    <option value="all"> None </option>
                    %for radius in program.vrni_vse_radiuse():
                        <option value={{str(radius)}}> {{"R" + str(radius)}} </option> 
                    %end
                </select>
                Height: <select id="height" onchange="ChangeHeight(this)">
                    <option value="all"> None </option>
                </select>
                Width: <select id="width" onchange="ChangeWidth(this)">
                    <option value="all"> None </option>
                </select>
            </div>
            <div id="gumbi">
                %for n in range(0,20):
                    <button style="float:left;width:30%;height:15%;margin:1%" id="{{"Button" + str(n)}}" onclick="Spremeni({{n + 1}})"> {{str(n)}}</button>
                %end 
            </div>
            <div id="koncno" hidden="hidden">
                <form>
                    <input type="number" value="" name="amount">
                    <input type="submit" hidden = "hidden">
                    <input type="hidden" value="" name="tip">
                    <input type="hidden" value="" name="dimenzija">
                    <label id="dimenzija_label" > dsdasdas</label>
                </form>
                <button style="background-color:yellow" id="yellow"> yellow </button>
                <button style="background-color:white" id="white"> white </button>
            </div>
        </div>
            
            
        </div>
    </div>
    <div id="arhiv_racunov">

    </div>
    </div>
    <script>
        function ChangeRadius() {
            var radiusbox = document.getElementById("radius");
            var Radiusvalue = radiusbox.options[radiusbox.selectedIndex].value;
            var dimenzije = [];
            var dimarray;
            %for dimenzija in program.dimenzije:
                dimarray = [];
                dimarray.push("{{dimenzija[0]}}");
                dimarray.push("{{dimenzija[1]}}");
                %if dimenzija[3]:
                    dimarray.push("{{dimenzija[2]}}" + "C");
                %else:
                    dimarray.push("{{dimenzija[2]}}");
                %end
                dimenzije.push(dimarray);
            %end
            if ( Radiusvalue == "all") {
                var h = document.getElementById("height");
                h.options.length = 1;
                var w = document.getElementById("width");
                w.options.length = 1;
                document.getElementById("koncno").style.display = "none"; 
                document.getElementById("gumbi").style.display = "block"; 
                Dodaj();
            } else{
                document.getElementById("koncno").style.display = "none"; 
                document.getElementById("gumbi").style.display = "block"; 
                var radiusheighti = []
                var x = document.getElementById("height");
                x.options.length = 1;
                var w = document.getElementById("width");
                w.options.length = 1;
                var option
                for (var i = 0; i < dimenzije.length; i++) {
                    if ( dimenzije[i][0] == Radiusvalue ) {
                        if (!(radiusheighti.includes(dimenzije[i][1]))) {
                            option = document.createElement("option");
                            option.text = dimenzije[i][1];
                            option.value = dimenzije[i][1];
                            x.add(option);
                            radiusheighti.push(dimenzije[i][1]) 
                        };
                    };
                };
                SkrijGumbe();
                DodajHeightGumbe();
            }; 
        };
        function ChangeHeight() {
            var radiusbox = document.getElementById("radius");
            var Radiusvalue = radiusbox.options[radiusbox.selectedIndex].value;
            var heightbox = document.getElementById("height");
            var Heightvalue = heightbox.options[heightbox.selectedIndex].value;
            var dimenzije = [];
            var dimarray;
            %for dimenzija in program.dimenzije:
                dimarray = [];
                dimarray.push("{{dimenzija[0]}}");
                dimarray.push("{{dimenzija[1]}}");
                %if dimenzija[3]:
                    dimarray.push("{{dimenzija[2]}}" + "C");
                %else:
                    dimarray.push("{{dimenzija[2]}}");
                %end
                dimenzije.push(dimarray);
            %end
            if ( Heightvalue == "all") {
                var x = document.getElementById("width");
                x.options.length = 1;
                document.getElementById("koncno").style.display = "none"; 
                document.getElementById("gumbi").style.display = "block";
                DodajHeightGumbe(); 
            } else{
                document.getElementById("koncno").style.display = "none"; 
                document.getElementById("gumbi").style.display = "block"; 
                var heightwidthi = []
                var x = document.getElementById("width");
                x.options.length = 1;
                var option
                for (var i = 0; i < dimenzije.length; i++) {
                    if ( dimenzije[i][0] == Radiusvalue && dimenzije[i][1] == Heightvalue ) {
                        if (!(heightwidthi.includes(dimenzije[i][2]))) {
                            option = document.createElement("option");
                            option.text = dimenzije[i][2];
                            option.text = dimenzije[i][2];
                            x.add(option);
                            heightwidthi.push(dimenzije[i][2]) 
                        };
                    };
                };
                SkrijGumbe();
                DodajWidthGumbe();
            };
        };
        function ChangeWidth() {
            var widthbox = document.getElementById("width")
            if (widthbox.value == "all") {
                document.getElementById("koncno").style.display = "none"; 
                document.getElementById("gumbi").style.display = "block";
                DodajWidthGumbe();  
            } else{
            var radius = document.getElementById("radius").value
            var height = document.getElementById("height").value
            var width = document.getElementById("width").value
            document.getElementById("koncno").style.display = "block"; 
            document.getElementById("gumbi").style.display = "none";
            document.getElementById("dimenzija_label").innerText = TvoriDimenzijo(radius, height, width);
            };     
        };
        function TvoriDimenzijo(radius, height, width) {
            if ( width == "R"){
                var dimenzija = height + "/R" + radius;
                return dimenzija;
            } else if ( width.slice(-1) == "C") {
                var dimenzija = height + "/" + width.slice(0, -1) + "/R" + radius + "C";
                return dimenzija;
            } else {
                var dimenzija = height + "/" + width + "/R" + radius;
                return dimenzija;
            };
        };
        function Spremeni(n) {
            var radiusindex = document.getElementById("radius").selectedIndex
            var heightindex = document.getElementById("height").selectedIndex
            if (radiusindex == 0){
                document.getElementById("radius").selectedIndex = n;
                ChangeRadius();
                SkrijGumbe();
                DodajHeightGumbe();
            } else if ( heightindex == 0){
                document.getElementById("height").selectedIndex = n;
                ChangeHeight();
                SkrijGumbe();
                DodajWidthGumbe();
            } else{
                document.getElementById("width").selectedIndex = n; 
                ChangeWidth(); 
            }
        };
        function Dodaj(){
            %radiusi = program.vrni_vse_radiuse()
            SkrijGumbe();
            %for n in range(len(radiusi)):
                var Buttonid = "{{'Button' + str(n)}}"
                document.getElementById(Buttonid).style.visibility = "visible";       
                document.getElementById(Buttonid).innerHTML = "{{"R" + radiusi[n]}}"; 
            %end     
            document.getElementById("dodajanje").style.display = "block";
            
            
        };
        function SkrijGumbe(){
            var i
            for (i = 0; i < 20; i++) {
                var Buttonid = "Button" + i.toString();
                document.getElementById(Buttonid).style.visibility = "hidden";             
            };
        };
        function DodajHeightGumbe(){
            var i
            var heightselect = document.getElementById("height")
            for (i = 0; i < heightselect.options.length - 1; i++) {
                var Buttonid = "Button" + i.toString();
                document.getElementById(Buttonid).style.visibility = "visible";    
                document.getElementById(Buttonid).innerHTML = heightselect[i + 1].value;
            };
        };
        function DodajWidthGumbe(){
            var i
            var widthselect = document.getElementById("width")
            for (i = 0; i < widthselect.options.length - 1; i++) {
                var Buttonid = "Button" + i.toString();
                document.getElementById(Buttonid).style.visibility = "visible";    
                document.getElementById(Buttonid).innerHTML = widthselect[i + 1].value;
            };
        };
        
    </script>
</body>
</html>