from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

# Create or refresh a DOCX reference template with brand styles

doc = Document()

# Normal (body) – Tahoma per office guidance
normal = doc.styles['Normal']
normal.font.name = 'Tahoma'
normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Tahoma')
normal.font.size = Pt(11)

# Title
styles = doc.styles
if 'Title' in styles:
    title = styles['Title']
else:
    title = styles.add_style('Title', WD_STYLE_TYPE.PARAGRAPH)

for s in [title]:
    s.font.name = 'Hurme Geometric Sans 4'
    s.font.size = Pt(28)
    s.font.bold = True
    s.font.color.rgb = RGBColor(0x4D,0x1D,0x82)

# Heading 1..3
for name, size in [('Heading 1', 18), ('Heading 2', 16), ('Heading 3', 14)]:
    st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH) if name not in styles else styles[name]
    st.font.name = 'Hurme Geometric Sans 4'
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0x4D,0x1D,0x82)

# Character style for brand accent (links, highlights)
accent = styles.add_style('Brand Accent', WD_STYLE_TYPE.CHARACTER) if 'Brand Accent' not in styles else styles['Brand Accent']
accent.font.color.rgb = RGBColor(0xCF,0x02,0x2B)

# Save
out = 'skills/brand-document/tools/templates/reference.docx'
doc.save(out)
print(f'Wrote {out}')
