<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    <div class="dimenzija">
        {{program.tvori_dimenzijo(program.radius,program.height,program.width)}}
    </div>
    
    <div class="text_box">
        <form action={{program.zacetna_stran + "nov_vnos/"}} method="post">
            <input style="font-size:25vh;text-align:center;width:100%;height:100%" id="stevilo" type="text" name="stevilo" autocomplete="off" autofocus onkeypress="return /\d/.test(String.fromCharCode(((event||window.event).which||(event||window.event).which)));">
            <input id="tip" type="hidden" name="tip" value={{tip}}>
            <input id="gumb" type="submit" hidden="hidden">
        </form>
    </div>

    <div class="gumba">
            <div class="yellow_gumb">
                <input style="background-color:yellow;width:100%;height:100%" id="yellow" type="submit" value="" onclick="KlikYellow()" style="background-color:yellow">
            </div>

            <div class="white_gumb">
                <input style="background-color:white;width:100%;height:100%" id="white" type="submit" value="" onclick="KlikWhite()" style="background-color:white">
            </div>
    </div>

    <div class="spodnja_vrstica">
        <div class="nazaj">
            <input style="width:100%;height:100%" id="nazaj" type="submit" value="nazaj">
        </div>
        <div class="preklici">
            <input style="width:100%;height:100%" id="preklici" type="submit" value="preklici">
        </div>
    </div>

<script>
    function KlikYellow() {
        document.getElementById("tip").value = "yellow"
        document.getElementById("gumb").click();
    };

    function KlikWhite() {
        document.getElementById("tip").value = "white"
        document.getElementById("gumb").click();
    }

</script>
</body>
</html>