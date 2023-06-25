from manim import *
class LinearInterpolation(MovingCameraScene):
    def makeGraph(self, values, moveto):
        plane = BarChart(
            values,
            y_range=[-18000, 18000, 36000],
            x_length=len(self.input_values)/5,
            y_length=5,
            x_axis_config={"include_ticks": False},
        )

        plane_group = VGroup(plane).scale(0.5).move_to(RIGHT + moveto)
        return plane_group

    def makeRow(self, row1, row2, row3, row4, row5):
        headingPosition = Text(row1).scale(0.5).move_to(LEFT*8)
        headingWholeNumber = Text(row2).scale(0.5).move_to(LEFT*6)
        headingRemainder = Text(row3).scale(0.5).move_to(LEFT*4)
        headingRate = Text(row4).scale(0.5).move_to(LEFT*2)
        headingOneMinusRem = Text(row5).scale(0.5)
        headings = VGroup(headingPosition, headingWholeNumber, headingRemainder, headingRate, headingOneMinusRem)
        return headings

    def makeInterpolationRow(self, row1:Mobject, row2:Mobject, row3:Mobject, row4:Mobject, row5:Mobject):
        cell1 = row1.scale(0.4).move_to(LEFT*6)
        cell2 = row2.scale(0.4).move_to(LEFT*4.5)
        cell3 = row3.scale(0.4).move_to(LEFT*3)
        cell4 = row4.scale(0.4).move_to(LEFT*1.5)
        cell5 = row5.scale(0.4)
        headings = VGroup(cell1, cell2, cell3, cell4, cell5).shift(RIGHT)
        return headings
    
    def makeInterpolationTable(self, row1:Mobject, row2:Mobject, row3:Mobject, row4:Mobject, row5:Mobject, value1: str, value2: str, value3: str, value4: str, value5: str):
        interpolationRow = self.makeInterpolationRow( row1, row2, row3, row4, row5.shift(RIGHT/2) )
        interpolationRow2 = self.makeInterpolationRow( Text(value1), Text(value2), Text(value3), Text(value4), Text(value5).shift(RIGHT/2) )
        interpolationRow2.align_to(interpolationRow, LEFT )
        interpolationRow2.shift( DOWN/4 )

        interpolationGroup = VGroup(interpolationRow, interpolationRow2)
        return interpolationGroup.shift(UP * 2.3 + RIGHT * 2.5)

    def createInputSampleTable(self):
        table_values = []
        for index in range(len(self.input_values)):
            values = []
            table_values.append(values)
            values.append(str(self.input_values[index]))

        row_label_values = []      
        for index in range(len(self.input_values)):
            row_label_values.append(Text(str(index)))

        samplesTable = Table(
            table_values,
            row_labels=row_label_values,
            col_labels=[Text("Amplitude")],
            line_config={"stroke_width": 1, "color": YELLOW}
        )
        samplesTable.add_highlighted_cell((2,2), color=GREEN)

        return samplesTable.scale(0.2).shift(LEFT * 5 + DOWN * 5)
    
    def createInitialOutputSampleTable(self):
        table_values = []
        
        values = []
        table_values.append(values)
        values.append(" - ")

        row_label_values = []      
        row_label_values.append(Text(" - "))

        samplesTable = Table(
            table_values,
            row_labels=row_label_values,
            col_labels=[Text("Amplitude")],
            line_config={"stroke_width": 1, "color": YELLOW}
        )
        #samplesTable.add_highlighted_cell((2,2), color=GREEN)

        return samplesTable.scale(0.2).shift(LEFT * 4 + UP * 3)

    def createOutputSampleTable(self, outputIndexValues, outputValues):
        table_values = []
        for index in range(len(outputValues)):
            values = []
            table_values.append(values)
            values.append(str(outputValues[index]))

        row_label_values = []      
        for index in range(len(outputIndexValues)):
            row_label_values.append(Text(str(outputIndexValues[index])))

        samplesTable = Table(
            table_values,
            row_labels=row_label_values,
            col_labels=[Text("Amplitude")],
            line_config={"stroke_width": 1, "color": YELLOW}
        )
        #samplesTable.add_highlighted_cell((2,2), color=GREEN)

        return samplesTable.scale(0.2).shift(LEFT * 4 + UP * 3)


    def construct(self):
        self.input_values = [1835,13491,15032,2034,-12419,-15735,-4204,10943,16221,6277,-9268,-16422,-8241,7429,16339,10056,-5457,-15971,-11694,3387,15326,13123,-1252,-14422,-14309,-919,13277,15237,3077,-11902,-15892,-5190,10327,16261,7216,-8572,-16346,-9116,6670,16140,10858,-4646,-15665,-12390,2523,14926,13699,-347,-13942,-14743,-1864,12741,15506,4061,-11338,-15967,-6229,9791,16079,8376,-8194,-15718,-10736,7347]
        #self.input_values = [223,2011,4086,6003,7889,9602,11203,12596,13819,14804,15568,16086,16344,16360,16101,15610,14848,13886,12666,11292,9694,7990,6116,4189,2155,124,-1937,-3952,-5907,-7780,-9507,-11123,-12510,-13774,-14728,-15564,-16024,-16382,-16314,-16181,-15580,-14967,-13875,-12812,-11308,-9850,-8036,-6272,-4264,-2296,-232,1833,3804,5857,7589,9534,10875,12644,13443,15016,15090,16582,15534,17798]
        input_values_graph = self.makeGraph(self.input_values, DOWN * 2.5)
        self.add(input_values_graph)

        self.output_values = []
        self.output_value_indexes = []
        self.output_values_table = None
        
        self.output_values_fake = []
        for i in self.input_values:
            self.output_values_fake.append(0)

        self.output_values_graph = self.makeGraph(self.output_values_fake, UP * 0.5)
        self.add(self.output_values_graph)

        rate = 0.5
        position = 0.0
        whole_number = 0
        remainder = 0.0
        one_minus_remainder = 1.0 - remainder
        last_whole_number = 0
        step = 0

        sampleTable = self.createInputSampleTable().shift(LEFT)
        self.add(sampleTable)

        self.output_values_table = self.createInitialOutputSampleTable()            
        self.output_values_table.align_to(sampleTable, UP)
        #self.output_values_table.shift(RIGHT)
        self.add(self.output_values_table)
        
        self.highlightedCell = None
        self.highlightedCell2 = None
        #r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots"
        interpolationTable = None
        

        row = self.makeRow("Rate","Position","Whole","1 - Rem", "Rem").move_to(UP*3.5+RIGHT*1.5)
        group = Group(row)
        #self.play(self.camera.frame.animate.move_to(row), run_time=0.1)
        #self.play(Write(row), run_time=2)
        self.add(row)

        last_row = row
        #return
    
        #for i in range(len(self.input_values)):        
        for i in range(4):        
            if whole_number >= len(self.input_values):
                return
            
            if (interpolationTable != None):
                self.remove(interpolationTable)

            f_zero_str = r"f("+str(whole_number)+")"
            f_zero = MathTex( f_zero_str )
            f_zero.set_color(GREEN)

            f_one_str = r"f("+str(whole_number+1)+")"
            f_one = MathTex( f_one_str )
            f_one.set_color(BLUE)

            f_zero2 = MathTex( f_zero_str )
            f_zero2.set_color(GREEN)

            times_by_rem_minus_one_str = " * (1 - r)"

            f_zero_times_by_rem_minus_one = MathTex(times_by_rem_minus_one_str, substrings_to_isolate=r"r")
            f_zero_times_by_rem_minus_one.set_color_by_tex(r"r", YELLOW)
            f_zero_times_by_rem_minus_one.next_to(f_zero2, RIGHT * 0.5 )
            f_zero_times_by_rem_minus_one_group = VGroup(f_zero2, f_zero_times_by_rem_minus_one)
            
            times_by_rem_str = r" * r"; 
            f_one2 = MathTex( f_one_str )
            f_one2.set_color(BLUE)

            f_one_times_by_rem = MathTex(times_by_rem_str, substrings_to_isolate=r"r")
            f_one_times_by_rem.set_color_by_tex(r"r", YELLOW)
            f_one_times_by_rem.next_to(f_one2, RIGHT * 0.5 )
            f_one_times_by_rem_group = VGroup(f_one2, f_one_times_by_rem)
           
            valueNext = 0
            value = self.input_values[whole_number]

            if (whole_number < len(self.input_values)-1):
                valueNext = self.input_values[whole_number+1]

            interpolated_value = int(round(value * (1 - remainder) + (valueNext * remainder)))

            f_one_times_by_rem_group_copy = VGroup( f_one.copy(), f_one_times_by_rem.copy())
            plusText = Text(" + ").next_to(f_one_times_by_rem_group_copy, RIGHT )
            f_zero_times_by_rem_minus_one_group_copy = VGroup(f_zero2.copy(), f_zero_times_by_rem_minus_one.copy()).next_to(plusText, RIGHT )
            finalFormula = VGroup(f_one_times_by_rem_group_copy, plusText, f_zero_times_by_rem_minus_one_group_copy)

            row2 = self.makeRow(
                '{0:.2f}'.format(rate), 
                '{0:.2f}'.format(position),
                str(whole_number),
                str('{0:.2f}'.format(one_minus_remainder)),
                str('{0:.2f}'.format(remainder)))
            
            if (last_row != row):
                group.remove(last_row)   
                row2.next_to(last_row, DOWN*0)
                self.play( FadeIn(row2), FadeOut(last_row),run_time=0.5 )
            else:
                row2.next_to(row, DOWN)
                self.play( FadeIn(row2),run_time=0.5 )
            group.add(row2)  


            interpolationTable = self.makeInterpolationTable(
                f_zero,
                f_one, 
                f_zero_times_by_rem_minus_one_group,
                f_one_times_by_rem_group,   
                finalFormula.shift(LEFT * 2),
                str(value), 
                str(valueNext),
                str(int(round(value * one_minus_remainder))),
                str(int(round(valueNext * remainder))),
                str(interpolated_value))
            finalresult = interpolationTable.submobjects[1].submobjects[4]
            interpolation_f0_times_1_minus_r = interpolationTable.submobjects[1].submobjects[2]
            interpolation_f1_time_r = interpolationTable.submobjects[1].submobjects[3]
            interpolationTable.submobjects[1].remove(interpolation_f0_times_1_minus_r)
            interpolationTable.submobjects[1].remove(interpolation_f1_time_r)
            interpolationTable.submobjects[1].remove(finalresult)

            self.add(interpolationTable)

            if (self.highlightedCell2 != None):
                self.play( FadeOut(self.highlightedCell2, run_time=0.1) )

            if (self.highlightedCell == None):
                self.highlightedCell = SurroundingRectangle(row2.submobjects[2], GREEN)
                self.play( Create(self.highlightedCell))
            
            if last_whole_number != whole_number:

                whole_number_highlite = SurroundingRectangle(row2.submobjects[2], GREEN)

                #self.camera.frame.save_state()
                self.play(
                    #self.camera.frame.animate.move_to(row2.submobjects[2]).scale(0.9),
                    Create(whole_number_highlite),
                    run_time=1)

                self.wait(1)
                self.play(
                    #self.camera.frame.animate.restore(), 
                    FadeOut(whole_number_highlite))

                cell = sampleTable[0]
                self.play(cell.animate.set_opacity(0),run_time=0.2)

                last_whole_number = whole_number

                #self.highlightedCell.generate_target()
                #self.highlightedCell.target.next_to(row2.submobjects[2], UP*0)
                #self.play( MoveToTarget(self.highlightedCell), run_time=1)

                sampleTable.add_highlighted_cell((2+whole_number,2), color=GREEN)

            self.highlightedCell.generate_target()
            self.highlightedCell.target.set_fill(color=BLUE)
            self.highlightedCell.target.next_to(sampleTable.get_cell((2 + whole_number, 1)) , UP*0)
            self.play( MoveToTarget(self.highlightedCell), run_time=1)

            self.play( 
                FadeIn(interpolation_f0_times_1_minus_r), 
                FadeIn(interpolation_f1_time_r), 
                run_time=0.5)
            self.play( FadeIn(finalresult), run_time=0.5)

            self.output_values.append(interpolated_value)
            self.output_value_indexes.append(whole_number)
            
            if (self.output_values_table != None):
                self.remove(self.output_values_table)

            self.output_values_table = self.createOutputSampleTable(self.output_value_indexes, self.output_values)
            self.output_values_table.align_to(sampleTable, UP)
            result_cell = self.output_values_table.get_cell((2+i, 2))

            #self.output_values_table.shift(RIGHT)
            self.add(self.output_values_table)

            finalresult.generate_target()
            #finalresult.target.set_fill(color=BLUE)
            finalresult.target.next_to(result_cell, UP*0)
            self.play( MoveToTarget(finalresult), run_time=1)
            self.play( FadeOut(finalresult), run_time=0.1)

            self.remove(self.output_values_graph)
            self.output_values_fake[step] = interpolated_value
            
            self.output_values_graph = self.makeGraph(self.output_values_fake, UP * 0.5)
            self.add(self.output_values_graph)

            self.highlightedCell2 = SurroundingRectangle(row2.submobjects[0], BLUE)
            self.play( Create(self.highlightedCell2))


            position += rate
            whole_number = int(position)
            remainder = position - whole_number
            one_minus_remainder = 1 - remainder

            self.highlightedCell2.generate_target()
            self.highlightedCell2.target.next_to(row2.submobjects[1] , UP*0)
            self.play( MoveToTarget(self.highlightedCell2), run_time=1)

            self.play( 
                FadeOut(interpolation_f0_times_1_minus_r),
                FadeOut(interpolation_f1_time_r),
                run_time=0.5)
            
            last_row = row2     
            step = step + 1
            #self.wait(0.1)
