#!/usr/bin/env python
# 
# Eurorack Panel Designer by THX2112
#
# v2
#

import sys
import math

import inkex
from simplestyle import *

class EurorackPanelEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-t', '--hp', action='store', type='int', dest='hp', default=6, help='Panel HP?')
        self.OptionParser.add_option('-o', '--offset', action='store', type='float', dest='offset', default=0.36, help='Amount of material to remove for fitting?')
        self.OptionParser.add_option('-s', '--symmetrical', action='store', type='inkbool', dest='symmetrical', default='False', help='Remove material from both sides?')
        self.OptionParser.add_option('-v', '--oval', action='store', type='inkbool', dest='oval', default='False', help='Oval holes?')
        self.OptionParser.add_option("-u", "--unit", action="store", type="string", dest="unit", default="mm", help="The unit of the box dimensions")
        self.OptionParser.add_option('-c', '--centers', action='store', type='inkbool', dest='centers', default='False', help='Mark centers?')

    def effect(self):


        ## Create a new layer.
        centre = self.view_center   #Put in in the centre of the current view
        grp_transform = 'translate' + str(centre)

        grp_name = 'grp'
        grp_attribs = {inkex.addNS('label','inkscape'):grp_name,'transform':grp_transform }
        grp = inkex.etree.SubElement(self.current_layer, 'g', grp_attribs)#the group to put everything in


        hp = self.options.hp
        symmetrical = self.options.symmetrical
        offset = self.options.offset
        oval = self.options.oval
        centers = self.options.centers

        svg = self.document.getroot()
       
        DocWidth = self.unittouu(svg.get('width'))
        DocHeight = self.unittouu(svg.attrib['height'])

        height = 128.5
        if symmetrical: 
            width = 7.5 + ((hp - 3) * 5.08) + 7.5
        else:
            width = (hp * 5.08) - offset

        pheight = self.unittouu(str(height) + self.options.unit)
        pwidth = self.unittouu(str(width) + self.options.unit)
        
        def draw_SVG_square((w,h), (x,y), (rx,ry), parent):

                style = {   'stroke'        : '#000000',
                            'stroke-width'  : '.05mm',
                            'fill'          : 'none'
                }
                
                attribs = {
                    'style'     : formatStyle(style),
                    'height'    : str(h),
                    'width'     : str(w),
                    'x'         : str(x),
                    'y'         : str(y),
                    'rx'        : str(rx),
                    'ry'        : str(ry)
                }

                circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs)

        #parent = self.current_layer
        draw_SVG_square((pwidth,pheight), (0,0), (0,0), grp) #grp was parent



        # Draw Holes

        BottomHoles = 3.0
        TopHoles = 125.5
        LeftHoles = 7.5
        RightHoles = ((hp - 3.0) * 5.08) + 7.5
        HoleRadius = 1.6



        #draw an SVG line segment between the given (raw) points
        def draw_SVG_line( (x1, y1), (x2, y2), parent):
            line_style   = {    'stroke': '#000000',
                                'stroke-width':'.05mm',
                                'fill': 'none'
                            }

            line_attribs = {    
                                'style'                     : formatStyle(line_style),
                                #inkex.addNS(grp_attribs)    : grp_name, 
                                'd'                         : 'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)
                           }

            line = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )


        
        if oval == False:


            def draw_SVG_ellipse((rx, ry), (cx, cy), parent, start, end):
                style = {   
                            'stroke'        : '#000000',
                            'stroke-width'  : '.05mm',
                            'fill'          : 'none'            
                        }
                ell_attribs = {'style':formatStyle(style),
                    inkex.addNS('cx','sodipodi')        :str(cx),
                    inkex.addNS('cy','sodipodi')        :str(cy),
                    inkex.addNS('rx','sodipodi')        :str(rx),
                    inkex.addNS('ry','sodipodi')        :str(ry),
                    inkex.addNS('start','sodipodi')     :str(start),
                    inkex.addNS('end','sodipodi')       :str(end),
                    inkex.addNS('open','sodipodi')      :'true',    #all ellipse sectors we will draw are open
                    inkex.addNS('type','sodipodi')      :'arc'
                }
                ell = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), ell_attribs)

            #parent = self.current_layer

        


            rx = self.unittouu(str(HoleRadius) + self.options.unit)
            ry = self.unittouu(str(HoleRadius) + self.options.unit)

            cxl = self.unittouu(str(LeftHoles) + self.options.unit)
            cxr = self.unittouu(str(RightHoles) + self.options.unit)
            cyb = self.unittouu(str(BottomHoles) + self.options.unit)
            cyt = self.unittouu(str(TopHoles) + self.options.unit)

            start = 0
            end = 2 * 3.14159

            #Bottom Left
            draw_SVG_ellipse((rx, ry), (cxl, cyb), grp, start, end)
            #Top Left
            draw_SVG_ellipse((rx, ry), (cxl, cyt), grp, start, end)


            # Draw Left-side Centers
            if centers == True:
                #Bottom Left Centers
                    #Horizontal Line
                    x1=self.unittouu(str(LeftHoles-1.6) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+1.6 ) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Vertical Line
                    x1=self.unittouu(str(LeftHoles) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                #Top Left Centers
                    #Horizontal Line
                    x1=self.unittouu(str(LeftHoles-1.6) + self.options.unit)
                    y1=self.unittouu(str(TopHoles) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+1.6 ) + self.options.unit)
                    y2=self.unittouu(str(TopHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Vertical Line
                    x1=self.unittouu(str(LeftHoles) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)

            
            if hp >= 5:

                #Draw Circles
                #Bottom Right
                draw_SVG_ellipse((rx, ry), (cxr, cyb), grp, start, end)
            
                #Top Right
                draw_SVG_ellipse((rx, ry), (cxr, cyt), grp, start, end)

                # Draw Right-side Centers
                if centers == True:
                    #Bottom Right Centers
                        #Horizontal Line
                        x1=self.unittouu(str(RightHoles-1.6) + self.options.unit)
                        y1=self.unittouu(str(BottomHoles) + self.options.unit)
                        x2=self.unittouu(str(RightHoles+1.6 ) + self.options.unit)
                        y2=self.unittouu(str(BottomHoles ) + self.options.unit)
                        draw_SVG_line( (x1, y1), (x2, y2), grp)
                        #Vertical Line
                        x1=self.unittouu(str(RightHoles) + self.options.unit)
                        y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                        x2=self.unittouu(str(RightHoles) + self.options.unit)
                        y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                        draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Top Right Centers
                        #Horizontal Line
                        x1=self.unittouu(str(RightHoles-1.6) + self.options.unit)
                        y1=self.unittouu(str(TopHoles) + self.options.unit)
                        x2=self.unittouu(str(RightHoles+1.6 ) + self.options.unit)
                        y2=self.unittouu(str(TopHoles ) + self.options.unit)
                        draw_SVG_line( (x1, y1), (x2, y2), grp)
                        #Vertical Line
                        x1=self.unittouu(str(RightHoles) + self.options.unit)
                        y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                        x2=self.unittouu(str(RightHoles) + self.options.unit)
                        y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                        draw_SVG_line( (x1, y1), (x2, y2), grp)

        if oval == True:

            # Oval: (is a square with rounded corners)


            cxl = self.unittouu(str(LeftHoles - 2.75) + self.options.unit)
            cxr = self.unittouu(str(RightHoles - 2.75) + self.options.unit)
            cyb = self.unittouu(str(BottomHoles - 1.6) + self.options.unit)
            cyt = self.unittouu(str(TopHoles - 1.6) + self.options.unit)

            ovalh = self.unittouu(str(3.2) + self.options.unit)

            ovalw = self.unittouu(str(5.5) + self.options.unit)
            ovals = self.unittouu(str(1.6) + self.options.unit)

            #Bottom Left
            draw_SVG_square((ovalw,ovalh), (cxl,cyb), (ovals,0), grp)
            #Top Left
            draw_SVG_square((ovalw,ovalh), (cxl,cyt), (ovals,0), grp)

            # Draw Left-side Centers
            if centers == True:
                #Bottom Left Centers
                    #Horizontal Line
                    x1=self.unittouu(str(LeftHoles-2.75) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+2.75 ) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Left Vertical Line
                    x1=self.unittouu(str(LeftHoles-1.15) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles-1.15) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Center Vertical Line
                    x1=self.unittouu(str(LeftHoles) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Right Vertical Line
                    x1=self.unittouu(str(LeftHoles+1.15) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+1.15) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                #Top Left Centers
                    #Horizontal Line
                    x1=self.unittouu(str(LeftHoles-2.75) + self.options.unit)
                    y1=self.unittouu(str(TopHoles) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+2.75 ) + self.options.unit)
                    y2=self.unittouu(str(TopHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Left Vertical Line -5.5+1.6=-3.9
                    x1=self.unittouu(str(LeftHoles-1.15) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles-1.15) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Center Vertical Line
                    x1=self.unittouu(str(LeftHoles) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Right Vertical Line
                    x1=self.unittouu(str(LeftHoles+1.15) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(LeftHoles+1.15) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)


            
            if hp >= 5:
                #Bottom Right
                draw_SVG_square((ovalw,ovalh), (cxr,cyb), (ovals,0), grp)
                #Top Right
                draw_SVG_square((ovalw,ovalh), (cxr,cyt), (ovals,0), grp)

                # Draw Left-side Centers
                if centers == True:
                #Bottom Right Centers
                    #Horizontal Line
                    x1=self.unittouu(str(RightHoles-2.75) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles) + self.options.unit)
                    x2=self.unittouu(str(RightHoles+2.75 ) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Left Vertical Line
                    x1=self.unittouu(str(RightHoles-1.15) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles-1.15) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Center Vertical Line
                    x1=self.unittouu(str(RightHoles) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Right Vertical Line
                    x1=self.unittouu(str(RightHoles+1.15) + self.options.unit)
                    y1=self.unittouu(str(BottomHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles+1.15) + self.options.unit)
                    y2=self.unittouu(str(BottomHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                #Top Right Centers
                    #Horizontal Line
                    x1=self.unittouu(str(RightHoles-2.75) + self.options.unit)
                    y1=self.unittouu(str(TopHoles) + self.options.unit)
                    x2=self.unittouu(str(RightHoles+2.75 ) + self.options.unit)
                    y2=self.unittouu(str(TopHoles ) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Left Vertical Line
                    x1=self.unittouu(str(RightHoles-1.15) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles-1.15) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Center Vertical Line
                    x1=self.unittouu(str(RightHoles) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)
                    #Right Vertical Line
                    x1=self.unittouu(str(RightHoles+1.15) + self.options.unit)
                    y1=self.unittouu(str(TopHoles+1.6) + self.options.unit)
                    x2=self.unittouu(str(RightHoles+1.15) + self.options.unit)
                    y2=self.unittouu(str(TopHoles-1.6) + self.options.unit)
                    draw_SVG_line( (x1, y1), (x2, y2), grp)


# Create effect instance and apply it.
effect = EurorackPanelEffect()
effect.affect()