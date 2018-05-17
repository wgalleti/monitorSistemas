SQL_LOCKS = """
SELECT C.SECONDS_IN_WAIT AS TEMPO,
       C.SID,
       A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID AS SESSIONID,
       C.MACHINE AS MAQUINA,
       A.OS_USER_NAME AS USUARIO,
       A.ORACLE_USERNAME AS ORACLEDB,
       TO_CHAR(WM_CONCAT(B.OBJECT_NAME)) AS OBJETOS,
       B.OBJECT_TYPE AS OBJETOTIPO,
       C.PROCESS AS PROCESSO,
       C.INST_ID AS RAC,
       C.SQL_ADDRESS,
       C.PREV_SQL_ID,
       'ALTER SYSTEM KILL SESSION ''' || A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID || ''' IMMEDIATE' AS COMANDO,
       COUNT(1) AS QTD_LOCKED
  FROM SYS.GV_$LOCKED_OBJECT A,
       SYS.ALL_OBJECTS B,
       SYS.GV_$SESSION C
 WHERE A.OBJECT_ID = B.OBJECT_ID
   AND A.INST_ID = C.INST_ID
   AND C.SID = A.SESSION_ID   
   AND C.SECONDS_IN_WAIT >= 90
 GROUP BY C.SECONDS_IN_WAIT,
          C.SID,
          A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID,
          C.MACHINE,
          A.OS_USER_NAME,
          A.ORACLE_USERNAME,
          B.OBJECT_TYPE,
          C.PROCESS,
          C.INST_ID,
          C.SQL_ADDRESS,
          C.PREV_SQL_ID,
          'ALTER SYSTEM KILL SESSION ''' || A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID || ''' IMMEDIATE'
 ORDER BY SECONDS_IN_WAIT DESC, 5 DESC
"""

SQL_SQLID = """
SELECT SQL_TEXT, 
       SQL_FULLTEXT 
  FROM SYS.GV_$SQL 
 WHERE SQL_ID = :sql_id
"""

EMAIL_BODY = """
<h1>Locks no banco de dados</h1>
Foram encontrados {locks} locks no banco de dados:
"""

EMAIL_MESSAGE = """
<br>
<h3>Sessão {sessao} em {maquina} para {usuario}</h3>
<table width="94%" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
    <tbody>
        <tr>
            <td align="left" bgcolor="#252525" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;">Objeto(s)</td>
            <td align="left" bgcolor="#252525" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;">Tempo em Execução</td>
            <td align="left" bgcolor="#252525" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;">Banco de Dados</td>
            <td align="left" bgcolor="#252525" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #EEEEEE; padding:10px; padding-right:0;">Rac</td>
        </tr>
        <tr>
            <td align="left" bgcolor="#FFFFFF" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;">{objeto}</td>
            <td align="left" bgcolor="#FFFFFF" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;">{tempo}</td>
            <td align="left" bgcolor="#FFFFFF" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;">{banco}</td>
            <td align="left" bgcolor="#FFFFFF" style="font-family: Verdana, Geneva, Helvetica, Arial, sans-serif; font-size: 12px; color: #252525; padding:10px; padding-right:0;">{rac}</td>
        </tr>
    </tbody>
</table>
<br>
<small>Para encessar essa sessão, execute o comando <b>{comando}</b></small>
<br>
SQL em execução:
<pre>{sql}</pre>
<hr>
"""

EMAIL_FOOTER = """
<h3>Utilidade</h3>
Para encessar essa sessão, siga os passos abaixo
<br>
<pre>
  1. Abra o Terminal.
  2. Execute o aplicativo SQLPlus conectando com um usuário DBA: sqlplus system@producao
  3. Rode o comando: ALTER SYSTEM KILL SESSION '123,123,@1' IMMEDIATE;
  4. Saia do SQLPlus: exit
</pre>
<br>
"""
