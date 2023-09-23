req = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sin="http://creditregistry.ru/2010/webservice/SingleFormatService">

   <soapenv:Header/>

   <soapenv:Body>


      <sin:GroupRequestData>
      <AuthData>

         <login>admin</login>

         <password>admin</password>

      </AuthData>

         <cacheUse>0</cacheUse>

         <uid>1145670650372952065</uid>

         <uidApplication>9362</uidApplication>

         <dateTimeApplication>2023-08-28T13:44:56.000+0000</dateTimeApplication>

         <connectorCodes>

            <connectorCode>300</connectorCode>

            <subRequestCode></subRequestCode>

         </connectorCodes>

         <connectorCodes>

            <connectorCode>3</connectorCode>

            <subRequestCode></subRequestCode>

         </connectorCodes>

         <personParam>

            <actAddrCity>Москва</actAddrCity>

            <actAddrOKATO>45000000000</actAddrOKATO>  

<regAddrCountry>RU</regAddrCountry>

<regAddrSettlement>тест</regAddrSettlement>

            <companyName>ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "СБЕРБАНК РОССИИ"</companyName>

            <companyShortName>ПАО "СБЕРБАНК РОССИИ"</companyShortName>

<inn>3664069397</inn>

            <consentDate>2023-08-28T10:46:08.577+0000</consentDate>

            <consentPeriod>1</consentPeriod>

            <consentUserType>2</consentUserType>

            <consentBusinessCompany>ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "СБЕРБАНК РОССИИ"</consentBusinessCompany>

            <consentBusinessRegNum>1027700132195</consentBusinessRegNum>

            <consentBusinessInn>7707083893</consentBusinessInn>

            <reportUserRegNum>1026400001870</reportUserRegNum>

            <reportUserTaxID>6453031840</reportUserTaxID>

            <requestReason>11</requestReason>

            <taxpayerCode>1</taxpayerCode>

            <idType>1</idType>

            <idNum>1027700132195</idNum>

            <nationality>RU</nationality>

         </personParam>

      </sin:GroupRequestData>

   </soapenv:Body>

</soapenv:Envelope>'''

req2 = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sin="http://creditregistry.ru/2010/webservice/SingleFormatService">
  <soapenv:Header/>


<soapenv:Body>


<sin:GroupRequestData>


<authData>

<login>admin</login>

<password>admin</password>

</authData>

<cacheUse>0</cacheUse>

<uid>1145670650372952065</uid>

<uidApplication>9362</uidApplication>

<dateTimeApplication>2023-08-28T13:44:56.000+0000</dateTimeApplication>


<connectorCodes>

<connectorCode>300</connectorCode>

<subRequestCode/>

</connectorCodes>


<connectorCodes>

<connectorCode>3</connectorCode>

<subRequestCode/>

</connectorCodes>


<personParam>

<actAddrCity>Москва</actAddrCity>

<actAddrOKATO>45000000000</actAddrOKATO>

<regAddrCountry>RU</regAddrCountry>

<regAddrSettlement>тест</regAddrSettlement>

<companyName>ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "СБЕРБАНК РОССИИ"</companyName>

<companyShortName>ПАО "СБЕРБАНК РОССИИ"</companyShortName>

<inn>7707083893</inn>

<regNumCode>1</regNumCode>

<consentDate>2023-08-28T10:46:08.577+0000</consentDate>

<consentPeriod>1</consentPeriod>

<consentUserType>2</consentUserType>

<consentBusinessCompany>ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "СБЕРБАНК РОССИИ"</consentBusinessCompany>

<consentBusinessRegNum>1027700132195</consentBusinessRegNum>

<consentBusinessInn>7707083893</consentBusinessInn>

<reportUserRegNum>1026400001870</reportUserRegNum>

<reportUserTaxID>6453031840</reportUserTaxID>

<requestReason>11</requestReason>

<taxpayerCode>1</taxpayerCode>

<idType>34</idType>

<idNum>1027700132195</idNum>

<nationality>RU</nationality>

</personParam>

</sin:GroupRequestData>

</soapenv:Body>

</soapenv:Envelope>
'''

print(''.join(req2.split('\n')))