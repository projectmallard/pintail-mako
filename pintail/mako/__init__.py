# pintail - Build static sites from collections of Mallard documents
# Copyright (c) 2020 Shaun McCance <shaunm@gnome.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

import mako.template
import pintail.site
import xml.sax.saxutils

class MakoTemplate(pintail.site.ToolsProvider, pintail.site.XslProvider):
    @classmethod
    def build_tools(cls, site):
        fd = open(os.path.join(site.tools_path, 'pintail-mako.xsl'),
                  'w', encoding='utf-8')
        fd.write('<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">\n')
        for tmpl in ('html.head', 'html.top', 'html.bottom'):
            makofile = os.path.join(site.topdir, tmpl + '.mako')
            print(makofile)
            if os.path.exists(makofile):
                makotmpl = mako.template.Template(filename=makofile)
                attrs = {}
                fd.write('<xsl:template name="' + tmpl + '.custom">\n')
                fd.write('<xsl:text disable-output-escaping="yes">\n')
                fd.write(xml.sax.saxutils.escape(makotmpl.render(**attrs)))
                fd.write('</xsl:text>\n')
                fd.write('</xsl:template>\n')
        # html.head.custom (html <head> element)
        # html.top.custom
        #   html.sidebar.custom
        #   html.header.custom
        #   html.footer.custom
        # html.bottom.custom

        # html.content.post.custom
        # html.content.pre.custom
        # html.css.custom
        # html.head.top.custom
        # html.js.content.custom
        # html.js.custom
        # html.linktrails.empty
        # html.linktrails.prefix
        fd.write('</xsl:stylesheet>\n')
        fd.close()


    @classmethod
    def get_xsl(cls, site):
        return [os.path.join(site.tools_path, 'pintail-mako.xsl')]


    @classmethod
    def get_xsl_params(cls, output, obj, lang=None):
        return []
