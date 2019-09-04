    <form action={{action}} method="get" style="position:absolute;width:80%;height:100%;top:0%;left:20%">
        RADIUS:
        <select id="radius" name="radius" onchange="ChangeRadius(this)">
            <option value="all"> None </option>
            %for radius in program.vrni_vse_radiuse():
                <option value={{str(radius)}}> {{"R" + str(radius)}} </option> 
            %end
        </select>
        HEIGHT:
            <select id="height" name="height" onchange="ChangeHeight(this)">
                <option value="all"> None </option>
            </select>
        WIDTH:                                  
            <select id="width" name="width">
                <option value="all"> None </option>
            </select>
            <input type="hidden" value="numeric" name="order" id="order">
            <input type="submit" value="filtriraj" id="filtriraj">
    </form>
            <input type="submit" onclick="ChangeOrder()" style="position:absolute;width:12%;height:80%;top:0%;left:5%" id="order" value="alphabetic">
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
                dimarray.push("{{dimenzija[2]}}");
                dimenzije.push(dimarray);
            %end
            if ( Radiusvalue == "all") {
                var h = document.getElementById("height");
                h.options.length = 1;
                var w = document.getElementById("width");
                w.options.length = 1;
            } else{
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
                dimarray.push("{{dimenzija[2]}}");
                dimenzije.push(dimarray);
            %end
            if ( Heightvalue == "all") {
                var x = document.getElementById("width");
                x.options.length = 1;
            } else{
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
            };
        };
        function ChangeOrder() {
            document.getElementById("order").value = "alphabetic";
            document.getElementById("filtriraj").click();
        };
    </script>
    </div>
</body>
</html>