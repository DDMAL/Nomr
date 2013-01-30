import os
from PIL import Image
from pymei import XmlImport, MeiDocument, MeiElement

class GlyphGen:

    def __init__(self, image_path, mei_path):
        '''
        Creates a GlyphGen object.

        PARAMETERS
        ----------
        image_path: path to the image to generate glyphs for.
        mei_path: path to the mei file containing glyph bounding box information.
        '''

        self.page_image = Image.open(image_path)
        self.meidoc = XmlImport.documentFromFile(mei_path)

    def gen_glyphs(self, output_path):
        '''
        Generates a cropped image of each glyph on the image
        of the page being processed according to the bounding
        box information of the glyph in the corresponding MEI file.

        PARAMETERS
        ----------
        output_path: path to write the glyphs
        '''

        zones = []

        # gather bounding boxes for the following glyph types
        allow_glyphs = ['clef', 'neume', 'division', 'custos']
        for gname in allow_glyphs:
            glyphs = self.meidoc.getElementsByName(gname)
            for g in glyphs:
                if g.hasAttribute('facs'):
                    g_fac = g.getAttribute('facs').value
                    zone = self.meidoc.getElementById(g_fac)
                    zones.append(zone)

        for z in zones:
            glyph_id = self.meidoc.getElementById(z.getId()).getId()

            # get bounding box information
            ulx = int(z.getAttribute('ulx').value)
            uly = int(z.getAttribute('uly').value)
            lrx = int(z.getAttribute('lrx').value)
            lry = int(z.getAttribute('lry').value)
            bb = (ulx, uly, lrx, lry)

            glyph = self.page_image.crop(bb)
            glyph_path = os.path.join(output_path, glyph_id + '.jpg')
            glyph.save(glyph_path, 'JPEG')

if __name__ == "__main__":
    image_path = '/Volumes/MarkovProperty/gburlet/work/Gold/gold/media/images/0400_corr.jpg'
    mei_path = '/Volumes/MarkovProperty/gburlet/work/Gold/gold/media/mei/0400_corr.mei'
    output_path = '/Volumes/MarkovProperty/gburlet/work/GOLDProject/glyphs'

    gg = GlyphGen(image_path, mei_path)
    gg.gen_glyphs(output_path)
