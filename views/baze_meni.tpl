<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div class="gumbi">
        %n = -1
        %for aktivna_baza in program.aktivne_baze:
            %n += 1
            %position = program.design.button_position(len(program.aktivne_baze) + 1, n)
            %size = program.design.button_size(len(program.aktivne_baze) + 1)

            <form action={{"/zaloga_meni/klik_gumba/" + str(n)}} method="post" style="position:absolute;left:{{str(position["left"]) + "%"}};top:{{str(position["top"]) + "%" }};width:{{str(size["width"]) + "%"}};height:{{str(size["height"]) + "%"}}">
                <input type="submit" value={{aktivna_baza.ime}}>
            </form>
        %end
        %if n < 19:
            %n += 1
            %position = program.design.button_position(len(program.aktivne_baze) + 1, n)
            %size = program.design.button_size(len(program.aktivne_baze) + 1)
            <form action="/zaloga_meni/dodaj_bazo/" method="post" style="position:absolute;left:{{str(position["left"]) + "%"}};top:{{str(position["top"]) + "%" }};width:{{str(size["width"]) + "%"}};height:{{str(size["height"]) + "%"}}">
                <input type="submit" value="+">
            </form>
        %end
    </div>
</body>
</html>