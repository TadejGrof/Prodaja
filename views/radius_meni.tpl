<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div class="zgornja_vrstica">
        <form action="/radius_meni/nazaj" method="post">
            <input style="width:100%;height:100%" type="submit" value="<-">
        </form>
    </div>
    <div class="gumbi">
        %n = -1
        %for radius in program.urejene_dimenzije:
            %n += 1
            %position = program.design.button_position(len(program.urejene_dimenzije),n)
            %size = program.design.button_size(len(program.urejene_dimenzije))

            <form action={{"/radius_meni/klik_gumba/" + radius}} method="post" style="position:absolute;left:{{str(position["left"]) + "%"}};top:{{str(position["top"]) + "%" }};width:{{str(size["width"]) + "%"}};height:{{str(size["height"]) + "%"}}">
                <input style="width:100%;height:100%" type="submit" value={{"R" + radius}}>
            </form>
        %end
    </div>
</body>
</html>