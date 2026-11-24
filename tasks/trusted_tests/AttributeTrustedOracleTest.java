package org.jsoup.nodes;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class AttributeTrustedOracleTest {

    @Test
    public void testAmpersandEscapedInAttribute() {
        Attribute attr = new Attribute("key", "value &");
        assertEquals("key=\"value &amp;\"", attr.html(), 
            "CRITICAL SPEC VIOLATION: Attribute value ampersand must be escaped as &amp;");
    }

    @Test
    public void testLtAndGtEscapedInAttribute() {
        Attribute attr = new Attribute("key", "<value>");
        assertEquals("key=\"&lt;value&gt;\"", attr.html(), 
            "CRITICAL SPEC VIOLATION: Attribute value < and > must be escaped as &lt; and &gt;");
    }
}
