<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

  <xsl:template match="one">
    textsssss
  </xsl:template>

  <xsl:template match="two"/>
  
  <xsl:template match="three">
    <root>sss</root>
  </xsl:template>
  
  <xsl:template match="four" mode="mode" priority="priority" name="name">
    <!-- comment -->
  </xsl:template>

  <xsl:template match="five" mode="mode" priority="priority" name="name">
    <!-- comment -->
    <node>
        asdf
        <!-- ref -->
        <text>adf</text>
    </node>
  </xsl:template>

</xsl:stylesheet>