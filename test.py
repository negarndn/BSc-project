import xml.etree.ElementTree as ET

# Your SPARQL response
sparql_response = '''
<sparql xmlns="http://www.w3.org/2005/sparql-results#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/sw/DataAccess/rf1/result2.xsd">
 <head>
  <variable name="o"/>
 </head>
 <results distinct="false" ordered="true">
  <result>
   <binding name="o"><uri>http://fkg.iust.ac.ir/resource/شیراز</uri></binding>
  </result>
  <result>
   <binding name="o"><literal xml:lang="fa">شیراز، امپراتوری تیموری</literal></binding>
  </result>
 </results>
</sparql>
'''
# Parse the SPARQL response
root = ET.fromstring(sparql_response)

# Extract and print the values from the "o" variable
for elem in root.iter():
    if 'name' in elem.attrib and elem.attrib['name'] == 'o':
        value = elem.find('.//*').text
        print(value)