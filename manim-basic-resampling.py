from manim import *

class TableOfVariables(MovingCameraScene):
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

    def makeRow(self, row1, row2, row3, row4):
        headingPosition = Text(row1).scale(0.5).move_to(LEFT*6)
        headingWholeNumber = Text(row2).scale(0.5).move_to(LEFT*4)
        headingRemainder = Text(row3).scale(0.5).move_to(LEFT*2)
        headingRate = Text(row4).scale(0.5)

        headings = VGroup(headingPosition, headingWholeNumber, headingRemainder, headingRate)
        return headings

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
        #lower frequency input (better choice for increasing playback rate)
        self.input_values = [223,2011,4086,6003,7889,9602,11203,12596,13819,14804,15568,16086,16344,16360,16101,15610,14848,13886,12666,11292,9694,7990,6116,4189,2155,124,-1937,-3952,-5907,-7780,-9507,-11123,-12510,-13774,-14728,-15564,-16024,-16382,-16314,-16181,-15580,-14967,-13875,-12812,-11308,-9850,-8036,-6272,-4264,-2296,-232,1833,3804,5857,7589,9534,10875,12644,13443,15016,15090,16582,15534,17798]
        #higher frequency input (better choice for decreasing playback rate)
        #self.input_values = [1835,13491,15032,2034,-12419,-15735,-4204,10943,16221,6277,-9268,-16422,-8241,7429,16339,10056,-5457,-15971,-11694,3387,15326,13123,-1252,-14422,-14309,-919,13277,15237,3077,-11902,-15892,-5190,10327,16261,7216,-8572,-16346,-9116,6670,16140,10858,-4646,-15665,-12390,2523,14926,13699,-347,-13942,-14743,-1864,12741,15506,4061,-11338,-15967,-6229,9791,16079,8376,-8194,-15718,-10736,7347];

        input_values_graph = self.makeGraph(self.input_values, DOWN * 2)
        self.add(input_values_graph)

        self.output_values = []
        self.output_value_indexes = []
        self.output_values_table = None
        
        self.output_values_fake = []
        for i in self.input_values:
            self.output_values_fake.append(0);

        self.output_values_graph = self.makeGraph(self.output_values_fake, UP * 1)
        self.add(self.output_values_graph)

        rate = 1.5
        position = 0.0
        whole_number = 0
        remainder = 0.0
        last_whole_number = 0
        step = 0

        sampleTable = self.createInputSampleTable()
        self.add(sampleTable)

        self.output_values_table = self.createInitialOutputSampleTable()            
        self.output_values_table.align_to(sampleTable, UP)
        self.output_values_table.shift(RIGHT)
        self.add(self.output_values_table)
        
        anchor = Text(str(whole_number)).move_to(UP*3.5 + LEFT*4)
        self.add(anchor)

        self.highlightedCell = None
        self.highlightedCell2 = None

        row = self.makeRow("Rate","Position","Whole number","Remainder").move_to(UP*3.5+RIGHT*1.5)
        group = Group(row)
        #self.play(self.camera.frame.animate.move_to(row), run_time=0.1)
        #self.play(Write(row), run_time=2)
        self.add(row)

        last_row = row

        for i in range(40):        
            if whole_number >= len(self.input_values):
                return
            row2 = self.makeRow('{0:.2f}'.format(rate), '{0:.2f}'.format(position),str(whole_number),str('{0:.2f}'.format(remainder)))
            if (last_row != row):
                group.remove(last_row)   
                row2.next_to(last_row, DOWN*0)
                self.play( FadeIn(row2), FadeOut(last_row),run_time=0.5 )
            else:
                row2.next_to(row, DOWN)
                self.play( FadeIn(row2),run_time=0.5 )

            group.add(row2)  

            if (self.highlightedCell2 != None):
                self.play( FadeOut(self.highlightedCell2, run_time=0.1) )

            last_whole_number_changed = False
            if (self.highlightedCell == None):
                self.highlightedCell = SurroundingRectangle(row2.submobjects[2], GREEN)
                self.play( Create(self.highlightedCell))
            
            if last_whole_number != whole_number:
                self.play(FadeOut(anchor), run_time=0.5)
                anchor = Text(str(whole_number)).move_to(UP*3.5 + LEFT*4)
                self.play(FadeIn(anchor), run_time=0.5)
                cell = sampleTable[0]
                self.play(cell.animate.set_opacity(0),run_time=0.2)

                last_whole_number = whole_number

                self.highlightedCell.generate_target()
                self.highlightedCell.target.next_to(row2.submobjects[2], UP*0)
                self.play( MoveToTarget(self.highlightedCell), run_time=1)

                sampleTable.add_highlighted_cell((2+whole_number,2), color=GREEN)

                last_whole_number_changed = True


            self.highlightedCell.generate_target()
            self.highlightedCell.target.set_fill(color=BLUE)
            self.highlightedCell.target.next_to(sampleTable.get_cell((2 + whole_number, 1)) , UP*0)
            self.play( MoveToTarget(self.highlightedCell), run_time=1)

            self.output_values.append(self.input_values[whole_number])
            self.output_value_indexes.append(whole_number)
            
            if (self.output_values_table != None):
                self.remove(self.output_values_table)

            self.output_values_table = self.createOutputSampleTable(self.output_value_indexes, self.output_values)
            self.output_values_table.align_to(sampleTable, UP)
            self.output_values_table.shift(RIGHT)
            self.add(self.output_values_table)

            self.remove(self.output_values_graph)
            self.output_values_fake[step] = self.input_values[whole_number]
            
            self.output_values_graph = self.makeGraph(self.output_values_fake, UP * 1)
            self.add(self.output_values_graph)

            self.highlightedCell2 = SurroundingRectangle(row2.submobjects[0], BLUE)
            self.play( Create(self.highlightedCell2))


            position += rate
            whole_number = int(position)
            remainder = position - whole_number

            self.highlightedCell2.generate_target()
            self.highlightedCell2.target.next_to(row2.submobjects[1] , UP*0)
            self.play( MoveToTarget(self.highlightedCell2), run_time=1)

            last_row = row2     
            step = step + 1
            #self.wait(0.1)
