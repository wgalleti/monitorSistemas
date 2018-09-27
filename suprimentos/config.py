body = """
    <h1>Pendências de Entrega</h1>
    Olá <b>{fornecedor}</b>, encontramos algumas ordens de compras com {pendencias} pendência(s). 
    Favor entrar em contato para solucionar com o <a href="mailto:compras@scheffer.agr.br">Departamento de Compras</a>.
    <br>
    <br>
    <br>
"""

table_header = """
<table
  width="94%"
  border="0"
  cellpadding="0"
  cellspacing="0"
  style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
  <tbody>
    <tr>
      <td
        align="left"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Filial
      </td>
      <td
        align="right"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Ordem
      </td>
      <td
        align="left"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Produto
      </td>
      <td
        align="left"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Descrição
      </td>
      <td
        align="left"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Unidade Medida
      </td>
      <td
        align="right"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Qtd Pedido
      </td>
      <td
        align="right"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Qtd Atendido
      </td>
      <td
        align="right"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Qtd Pendente
      </td>
      <td
        align="left"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Previsão de Entrega
      </td>
      <td
        align="right"
        bgcolor="#252525"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;"
      >
        Dias em Atraso
      </td>
    </tr>
"""

table_items = """
    <tr>
      <td
        align="left"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {filial}
      </td>
      <td
        align="right"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {ordem}
      </td>
      <td
        align="left"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {produto}
      </td>
      <td
        align="left"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {descricao}
      </td>
      <td
        align="left"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {unidade_medida}
      </td>
      <td
        align="right"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {pedido}
      </td>
      <td
        align="right"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {entregue}
      </td>
      <td
        align="right"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        <b style="color:#FF0000;">{pendente}</b>
      </td>
      <td
        align="left"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {previsao}
      </td>
      <td
        align="right"
        bgcolor="#FFFFFF"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;"
      >
        {dias}
      </td>
    </tr>
"""

table_end = """
  </tbody>
</table>

<h3>Caso já tenha atendido as ordens acima, favor desconsiderar esse email!</h3>
"""


def format_number(value):
    a = '{:,.2f}'.format(float(value))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')