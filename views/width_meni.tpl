<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    %include('navbar.tpl')
    <div class="zgornja_vrstica">
        <form action="/width_meni/nazaj" method="post">
            <input type="submit" value="<-">
        </form>
    </div>
    <div class="gumbi">
        %n = -1
        %for width in program.urejene_dimenzije[program.radius][program.height]:
            %n += 1
            %position = program.design.button_position(len(program.urejene_dimenzije[program.radius][program.height]),n)
            %size = program.design.button_size(len(program.urejene_dimenzije[program.radius][program.height]))

            <form action={{"/width_meni/klik_gumba/" + width}} method="post" style="position:absolute;left:{{str(position["left"]) + "%"}};top:{{str(position["top"]) + "%" }};width:{{str(size["width"]) + "%"}};height:{{str(size["height"]) + "%"}}">
                <input type="submit" style="width:100%;height:100%" value={{width}}>
            </form>
        %end
    </div>
</body>
</html>