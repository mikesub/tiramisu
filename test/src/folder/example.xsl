<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

  <xsl:template match="doc">
    <!--xsl:value-of select="x:http-header-out('Content-Type', 'text/html; charset=UTF-8')"/>
    <xsl:apply-templates sele ct="." mode="identity-transform"/-->
    <xsl:apply-templates select="result"/>
    <xsl:apply-templates select="xscript_invoke_failed"/>
  </xsl:template>

  <xsl:template match="xscript_invoke_failed"/>

</xsl:stylesheet>