SQL_DETALHES = """
SELECT TRIM(INITCAP(EMP.ABV_EMPR)) AS BENEFICIADORA,
       EMP.COD_EMPR AS BENEFICIADORA_ID,
       TRIM(INITCAP(EMP2.ABV_EMPR)) AS PRODUTORA,
       EMP2.COD_EMPR AS PRODUTORA_ID,
       FAR.COD_FARDAO AS FARDAO_ID,
       TRIM(INITCAP(FMT.DSC_FORMATO)) AS TIPO_FARDAO,
       TRIM(INITCAP(DV3.DSC_DIVI3)) AS TALHAO,
       TRIM(INITCAP(VRD.DSC_VARIE)) AS VARIEDADE,
       FAR.FAR_PESO_BAL AS PESO_ALGODAO,
       MIN(PLU.PLU_DTHR_PESO) AS PRIMEIRO_FARDO,
       MAX(PLU.PLU_DTHR_PESO) AS ULTIMO_FARDO,
       SUM(PLU.PLU_PESO_INI - PLU.PLU_PESO_TARA) AS PESO_PLUMA,
       COUNT(DISTINCT PLU.ID_PLUMA) AS FARDINHOS       
  FROM GATEC_SAF.GA_ALG_PLUMA PLU
       JOIN GATEC_SAF.GA_SAF_SAFRAS SAF ON PLU.COD_EMPR = SAF.COD_EMPR
                                       AND PLU.COD_SAFRA = SAF.COD_SAFRA
       JOIN GATEC_SAF.GA_EMPR EMP ON PLU.COD_EMPR = EMP.COD_EMPR
       JOIN GATEC_SAF.GA_ALG_FARDAO FAR ON PLU.COD_FARDAO = FAR.COD_FARDAO
       JOIN GATEC_SAF.GA_SAF_VARIEDADE VRD ON FAR.COD_VARIE = VRD.COD_VARIE
       JOIN GATEC_SAF.GA_EMPR EMP2 ON FAR.COD_EMPR = EMP2.COD_EMPR
       JOIN GATEC_SAF.GA_ALG_FARDAO_FORMATO FMT ON FAR.COD_FORMATO = FMT.COD_FORMATO
       JOIN GATEC_SAF.GA_SAF_DIVI4 DV4 ON FAR.ID_DIVI4 = DV4.ID_DIVI4
       JOIN GATEC_SAF.GA_SAF_DIVI3 DV3 ON DV4.ID_DIVI3 = DV3.ID_DIVI3
 WHERE SAF.SAF_ANO_SAFRA = 2017
   AND FAR.FAR_STATUS = 5
   AND 1 = CASE
             WHEN TO_CHAR(SYSDATE, 'HH24') BETWEEN 0 AND 7 THEN
               CASE WHEN PLU.PLU_DTHR_PESO BETWEEN TO_DATE(TO_CHAR(SYSDATE - 1, 'YYYY/MM/DD') || ' 18:30:00', 'YYYY/MM/DD HH24:MI:SS') 
                                          AND TO_DATE(TO_CHAR(SYSDATE, 'YYYY/MM/DD') || ' 06:59:00', 'YYYY/MM/DD HH24:MI:SS') THEN
                 1
               ELSE
                 0
               END
             ELSE
               CASE WHEN PLU.PLU_DTHR_PESO >= TO_DATE(TO_CHAR(TRUNC(SYSDATE), 'DD/MM/YYYY') || '07:00:00', 'DD/MM/YYYY HH24:MI:SS') THEN
                 1
               ELSE
                 0
               END
            END
 GROUP BY EMP.ABV_EMPR,
          EMP.COD_EMPR,
          EMP2.ABV_EMPR,
          EMP2.COD_EMPR,
          FAR.COD_FARDAO,
          FAR.FAR_PESO_BAL,          
          DV3.DSC_DIVI3,
          VRD.DSC_VARIE,
          FMT.DSC_FORMATO
 ORDER BY EMP.COD_EMPR, 10
"""

SQL_RESUMO = """
SELECT QUA.BENEFICIADORA AS BENEFICIADORA,
       QUA.BENEFICIADORA_ID AS BENEFICIADORA_ID,
       COUNT(DISTINCT QUA.FARDAO_ID) AS FARDOES,
       TO_CHAR(WM_CONCAT(DISTINCT QUA.TALHAO)) AS TALHOES,
       TO_CHAR(WM_CONCAT(DISTINCT QUA.VARIEDADE)) AS VARIEDADES,
       SUM(QUA.PESO_ALGODAO) AS PESO_ALGODAO,
       SUM(QUA.PESO_PLUMA) AS PESO_PLUMA,
       SUM(QUA.FARDINHOS) AS FARDINHOS        
  FROM (
        SELECT TRIM(INITCAP(EMP.ABV_EMPR)) AS BENEFICIADORA,
               EMP.COD_EMPR AS BENEFICIADORA_ID,
               TRIM(INITCAP(EMP2.ABV_EMPR)) AS PRODUTORA,
               EMP2.COD_EMPR AS PRODUTORA_ID,
               FAR.COD_FARDAO AS FARDAO_ID,
               TRIM(INITCAP(FMT.DSC_FORMATO)) AS TIPO_FARDAO,
               TRIM(INITCAP(DV3.DSC_DIVI3)) AS TALHAO,
               TRIM(INITCAP(VRD.DSC_VARIE)) AS VARIEDADE,
               FAR.FAR_PESO_BAL AS PESO_ALGODAO,
               MIN(PLU.PLU_DTHR_PESO) AS PRIMEIRO_FARDO,
               MAX(PLU.PLU_DTHR_PESO) AS ULTIMO_FARDO,
               SUM(PLU.PLU_PESO_INI - PLU.PLU_PESO_TARA) AS PESO_PLUMA,
               COUNT(DISTINCT PLU.ID_PLUMA) AS FARDINHOS       
          FROM GATEC_SAF.GA_ALG_PLUMA PLU
               JOIN GATEC_SAF.GA_SAF_SAFRAS SAF ON PLU.COD_EMPR = SAF.COD_EMPR
                                               AND PLU.COD_SAFRA = SAF.COD_SAFRA
               JOIN GATEC_SAF.GA_EMPR EMP ON PLU.COD_EMPR = EMP.COD_EMPR
               JOIN GATEC_SAF.GA_ALG_FARDAO FAR ON PLU.COD_FARDAO = FAR.COD_FARDAO
               JOIN GATEC_SAF.GA_SAF_VARIEDADE VRD ON FAR.COD_VARIE = VRD.COD_VARIE
               JOIN GATEC_SAF.GA_EMPR EMP2 ON FAR.COD_EMPR = EMP2.COD_EMPR
               JOIN GATEC_SAF.GA_ALG_FARDAO_FORMATO FMT ON FAR.COD_FORMATO = FMT.COD_FORMATO
               JOIN GATEC_SAF.GA_SAF_DIVI4 DV4 ON FAR.ID_DIVI4 = DV4.ID_DIVI4
               JOIN GATEC_SAF.GA_SAF_DIVI3 DV3 ON DV4.ID_DIVI3 = DV3.ID_DIVI3
         WHERE SAF.SAF_ANO_SAFRA = 2017
           AND FAR.FAR_STATUS = 5
           AND 1 = CASE
                     WHEN TO_CHAR(SYSDATE, 'HH24') BETWEEN 0 AND 7 THEN
                       CASE WHEN PLU.PLU_DTHR_PESO BETWEEN TO_DATE(TO_CHAR(SYSDATE - 1, 'YYYY/MM/DD') || ' 18:30:00', 'YYYY/MM/DD HH24:MI:SS') 
                                                  AND TO_DATE(TO_CHAR(SYSDATE, 'YYYY/MM/DD') || ' 06:59:00', 'YYYY/MM/DD HH24:MI:SS') THEN
                         1
                       ELSE
                         0
                       END
                     ELSE
                       CASE WHEN PLU.PLU_DTHR_PESO >= TO_DATE(TO_CHAR(TRUNC(SYSDATE), 'DD/MM/YYYY') || '07:00:00', 'DD/MM/YYYY HH24:MI:SS') THEN
                         1
                       ELSE
                         0
                       END
                    END
         GROUP BY EMP.ABV_EMPR,
                  EMP.COD_EMPR,
                  EMP2.ABV_EMPR,
                  EMP2.COD_EMPR,
                  FAR.COD_FARDAO,
                  FAR.FAR_PESO_BAL,          
                  DV3.DSC_DIVI3,
                  VRD.DSC_VARIE,
                  FMT.DSC_FORMATO  
       ) QUA
 GROUP BY QUA.BENEFICIADORA,
          QUA.BENEFICIADORA_ID
 ORDER BY 2
"""

body = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta name="viewport" content="width=device-width"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Boletim de informativo das Algodoeiras</title>
    <link href="http://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet" type="text/css">
</head>
<body style="margin:0px; background: #FFFFFF; ">
<div width="100%" style="background: #FFF; padding: 0px 0px; font-family:'Ubuntu'; line-height:28px; height:100%;  width: 100%; color: #009d92;">
    <div style="padding:10px;  margin: 0px auto; font-size: 14px">
        <table border="0" cellpadding="0" cellspacing="0" style="width: 100%; margin-bottom: 20px">
            <tbody>
            <tr>
                <td style="vertical-align: top; padding-bottom:30px;" align="center">
                    <a href="http://financeiro.gruposcheffer.com" target="_blank">
                        <img src="https://financeiro.gruposcheffer.com/static/logo_novo.png" alt="Scheffer"
                             style="border:none">
                    </a>
                </td>
            </tr>
            </tbody>
        </table>
        <table border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
            <tbody>
            <tr>
                <td style="background:#383A37; padding:20px; color:#fff; text-align:center; font-weight: 700;">
                    <h1>Boletim informativo das Algodoeiras</h1>
                </td>
            </tr>
            </tbody>
        </table>
        <div style="padding: 10px; background: #FFF;">
            <table border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
                <tbody>
                <tr>
                    <td style="text-align: center; font-size: 1.2em">
                        {tabela_resumo}                       
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; font-size: 1.2em">
                        {tabela_detalhes}                       
                    </td>
                </tr>                    
                </tbody>
            </table>
        </div>
    </div>
</div>
</body>
</html>
"""

tb_detalhe_row = """
<tr>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {produtora}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {fardao_id}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {tipo_fardao}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {talhao}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {variedade}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_algodao}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_pluma}
  </td>
  <td align="center"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {primeiro_fardo}
  </td>
  <td align="center"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {ultimo_fardo}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {fardinhos}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {rendimento}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_medio}
  </td>
</tr>
"""

tb_detalhe_header = """
<h2>{algodoeira}</h2>
<table
  width="100%"
  border="0"
  cellpadding="0"
  cellspacing="0"
  style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
  <tbody>
    <tr>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Fazenda Produtora
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Fardão
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Tipo
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Talhão
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Variedade
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso de Algodão
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso Pluma
      </td>
      <td
        align="center"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Primeiro Fardinho
      </td>
      <td
        align="center"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Ultimo Fardinho
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Fardinhos Produzido
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Rendimento
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso Médio
      </td>
    </tr>
    {itens}
  </tbody>
</table>
"""

tb_resumo_row = """
<tr>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {beneficiadora}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {fardoes}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {talhoes}
  </td>
  <td align="left"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {variedades}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_algodao}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_pluma}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {fardinhos}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {rendimento}
  </td>
  <td align="right"
      bgcolor="#FFFFFF"
      style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #383A37; padding:10px;">
    {peso_medio}
  </td>
</tr>
"""

tb_resumo_header = """
<table
  width="100%"
  border="0"
  cellpadding="0"
  cellspacing="0"
  style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
  <tbody>
    <tr>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Beneficiadora
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Fardões
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Talhões
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Variedades
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso de Algodão
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso Pluma
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Fardinhos Produzido
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Rendimento
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Peso Médio
      </td>
    </tr>
    {itens}
    {totais}
  </tbody>
</table>
"""

tb_resumo_footer = """
<tr>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        Totais
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {fardoes}
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        &nbsp;
      </td>
      <td
        align="left"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        &nbsp;
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {peso_algodao}
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {peso_pluma}
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {fardos_produzido}
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {rendimento}
      </td>
      <td
        align="right"
        bgcolor="#383A37"
        style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px;"
      >
        {peso_medio}
      </td>
    </tr>
"""


def format_number(value, decimais=2):
    a = '{:,.2f}'.format(float(value))
    if decimais != 2:
        a = '{:,.0f}'.format(float(value))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')
