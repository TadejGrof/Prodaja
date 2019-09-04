<html>
<head>
    <title>Osnovni meni</title>
    <link rel="stylesheet" type="text/css" href="design/design.css">
</head>
<body>
    <table frame=border rules=all style="position:absolute;left:10%;width:80%;top:5%">
            <tr class="header">
                <th width="30% class="dimenzija">
                    Dimenzija
                </th>
                <th width="20% class="tip">
                    Tip
                </th>
                <th width="15% class="total">
                    Zaloga:
                </th>
                <th width="20% class="tip">
                    Tip
                </th>
                <th width="15% class="total">
                    Zaloga:
                </th>
            </tr>
            %for dimenzija in program.zaloga.baza.slovar["dimenzije"]:
                <tr class="dimenzija">
                    <td class="dimenzija">
                        {{dimenzija}}
                    </td>
                    <td  class="tip">
                        yellow
                    </td>
                    <td class="total">
                        {{program.zaloga.baza.slovar["dimenzije"][dimenzija][0]}}
                    </td>
                    <td  class="tip">
                        white
                    </td>
                    <td class="total">
                        {{program.zaloga.baza.slovar["dimenzije"][dimenzija][1]}}
                    </td>
                </tr>     
            %end
        </table>
</body>
</html>