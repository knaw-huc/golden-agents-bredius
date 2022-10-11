<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text"/>
  <xsl:template match="/">
    { "Collection": [
    <xsl:for-each select="ead/archdesc/dsc/c01">
      
      {"URI": "https://rkd.nl/explore/archives/file/<xsl:value-of select="did/unitid/@identifier"/>",
      "Inventarisnummer":"<xsl:value-of select="did/unitid"/>",
      "Titel":"<xsl:value-of select="did/unittitle"/>",
      "Onderdelen": [
      <xsl:for-each select="c02">   
        {"URI": "https://rkd.nl/explore/archives/file/<xsl:value-of select="did/unitid/@identifier"/>",
        "Inventarisnummer":"<xsl:value-of select="did/unitid"/>",
        "Titel":"<xsl:value-of select="did/unittitle"/>",
        "Onderdelen": [
        <xsl:for-each select="c03">
          {"URI": "https://rkd.nl/explore/archives/file/<xsl:value-of select="did/unitid/@identifier"/>",
          "Inventarisnummer":"<xsl:value-of select="did/unitid"/>",
          "Titel":"<xsl:value-of select="did/unittitle"/>",
          "Personen" : [
          <xsl:for-each select="controlaccess/persname">
            {"URI":"<xsl:value-of select="@authfilenumber"/>","Naam":"<xsl:value-of select="text()"/>"},
          </xsl:for-each>
          ]
          },   
        </xsl:for-each>
        ]},
      </xsl:for-each>
      ]}, 
    </xsl:for-each>
    ]
    }
    
  </xsl:template>
</xsl:stylesheet>
