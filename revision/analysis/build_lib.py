import copy, re
import docx
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Inches

SRC = '/root/.claude/uploads/dc34ef3b-dba4-5208-8b99-16334d39897b/f9d3227e-manuscript.docx'

def esc(s):
    return (s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))

def body_children(doc):
    return list(doc.element.body.iterchildren())

def find_para(doc, needle, start=0):
    """Return the w:p element whose text starts with / contains needle."""
    hits = [p for p in doc.paragraphs if needle in p.text]
    if len(hits) != 1:
        raise SystemExit(f"find_para: {len(hits)} hits for {needle!r}")
    return hits[0]

def set_text(p, text):
    """Replace a paragraph's text, keeping the first run's formatting."""
    runs = p._p.findall(qn('w:r'))
    if not runs:
        raise SystemExit("set_text: no runs in %r" % p.text[:40])
    for r in runs[1:]:
        p._p.remove(r)
    r = runs[0]
    ts = r.findall(qn('w:t'))
    for t in ts[1:]:
        r.remove(t)
    if not ts:
        t = parse_xml('<w:t %s/>' % nsdecls('w')); r.append(t); ts=[t]
    ts[0].text = text
    ts[0].set(qn('xml:space'), 'preserve')

def clone_para(template_p, text):
    new = copy.deepcopy(template_p._p)
    runs = new.findall(qn('w:r'))
    for r in runs[1:]:
        new.remove(r)
    r = runs[0]
    ts = r.findall(qn('w:t'))
    for t in ts[1:]:
        r.remove(t)
    ts[0].text = text
    ts[0].set(qn('xml:space'), 'preserve')
    # drop bookmarks / proofing marks that may carry over
    for tag in ('w:bookmarkStart','w:bookmarkEnd','w:proofErr'):
        for e in new.findall(qn(tag)):
            new.remove(e)
    return new

TBLPR = '''<w:tblPr><w:tblStyle w:val="af"/><w:tblW w:w="{tot}" w:type="dxa"/><w:jc w:val="center"/>
<w:tblBorders><w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/><w:left w:val="none" w:sz="6" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/><w:right w:val="none" w:sz="6" w:space="0" w:color="auto"/><w:insideH w:val="none" w:sz="6" w:space="0" w:color="auto"/><w:insideV w:val="none" w:sz="6" w:space="0" w:color="auto"/></w:tblBorders>
<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'''

def build_table(rows, widths):
    """rows: list of list of str (row 0 = header). widths: dxa per column."""
    assert all(len(r) == len(widths) for r in rows), "ragged table"
    tot = sum(widths)
    out = ['<w:tbl %s>' % nsdecls('w'), TBLPR.format(tot=tot)]
    out.append('<w:tblGrid>' + ''.join('<w:gridCol w:w="%d"/>' % w for w in widths) + '</w:tblGrid>')
    n = len(rows)
    for ri, row in enumerate(rows):
        first, last = ri == 0, ri == n - 1
        out.append('<w:tr>')
        if first:
            out.append('<w:trPr><w:tblHeader/></w:trPr>')
        for ci, cell in enumerate(row):
            if first:
                borders = ('<w:tcBorders><w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                           '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>')
                shd = ''
            elif last:
                borders = ('<w:tcBorders><w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/></w:tcBorders>')
                shd = '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
            else:
                borders = ''
                shd = '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
            keep = '<w:keepNext/><w:keepLines/>' if first else '<w:keepLines/>'
            bold = '<w:b/>' if first else ''
            out.append(
                '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s'
                '<w:tcMar><w:top w:w="70" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
                '<w:bottom w:w="70" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr>%s<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:rPr><w:rFonts w:eastAsia="Times New Roman"/>%s<w:sz w:val="16"/></w:rPr>'
                '<w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
                % (widths[ci], borders, shd, keep, bold, esc(cell)))
        out.append('</w:tr>')
    out.append('</w:tbl>')
    return parse_xml(''.join(out))
