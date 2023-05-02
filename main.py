from scamp import *
import random
import pygame
import keyboard

class UI:
    def __init__(self, width = 500, height = 500, cols = 10, octaves=1, MIDILowest = 50, MIDIChange = 2, volume = 2, duration = 0.25, tempo = 50, borderWidth = 5):
        pygame.init()
        self.width = width
        self.height = height
        self.WIN = pygame.display.set_mode((width, height))

        self.borderWidth = borderWidth

        self.MIDILowest = MIDILowest
        self.MIDIChange = MIDIChange
        self.volume = volume
        self.duration = duration
        self.tempo = tempo

        s = Session(tempo=tempo)
        self.instrument = s.new_part("french horn")

        self.emptyNoteColor = (125, 125, 125)
        self.hoverNoteColor = (255, 50, 255)
        self.fullNoteColor = (50, 50, 255)
        self.labelNoteColor = (255, 255, 255)

        self.octaves = octaves
        self.rows = octaves*7
        self.cols = cols+1 # how many squares for potential notes? +1 because its accounting for the label

        self.MIDIs = self.createMIDIs()
        
        b = self.createBoard()
        self.board = b[0]
        self.boardValues = b[1]


    def createMIDIs(self):
        MIDIs = []
        for _ in range(self.rows):
            MIDIs.append(self.MIDILowest)
            self.MIDILowest += self.MIDIChange
        return MIDIs

    def createBoard(self):
        board = []
        boardValues = []

        rows = self.octaves*7
        cols = self.cols -1 # columns not for the label
        rowPixels = self.height/(rows)
        colPixels = self.width/self.cols

        for currentRow in range(rows):
            row = []
            row_ = [] # for the second one
            for currentCol in range(cols):
                row.append(pygame.Rect((currentCol * colPixels) + colPixels, currentRow * rowPixels, colPixels - self.borderWidth, rowPixels - self.borderWidth))
                row_.append(0)
            board.append(row)
            boardValues.append(row_)
        
        # adding the labels in
        
        for row in board:
            row.insert(0, pygame.Rect(0, board.index(row) * rowPixels, colPixels - self.borderWidth, rowPixels - self.borderWidth))
        for row_ in boardValues:
            row_.insert(0, self.MIDIs[boardValues.index(row_)])

        return (board, boardValues)

    def convertBoardToNotes(self):
        notes = []

        c = 1 # not counting label at index 0
        while c < self.cols:
            intervalNotes = []
            for row in self.boardValues:
                if row[c] == 1:
                    intervalNotes.append(row[0])
            if len(intervalNotes) == 0:
                intervalNotes.append(0)
            notes.append(intervalNotes)
            c+=1

        return notes
        
    def drawBoard(self):
        for row in self.board:
            for rect in row:

                pressed = pygame.mouse.get_pressed()
                hover = pygame.mouse.get_pos()

                rowIndex = self.board.index(row)
                colIndex = row.index(rect)

                color = self.emptyNoteColor
                val = self.boardValues[rowIndex][colIndex]

                if val == 1:
                    color = self.fullNoteColor
                if rect.collidepoint(hover) and val < 5:
                    color = self.hoverNoteColor
                    if pressed[0]:
                        self.boardValues[rowIndex][colIndex] = 1
                    elif pressed[2]:
                        self.boardValues[rowIndex][colIndex] = 0
                if val > 5:
                    color = self.labelNoteColor
                
                pygame.draw.rect(self.WIN, color, rect)

    def checkCommands(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.play(self.convertBoardToNotes())
            pygame.time.delay(100)

    def update(self):
        self.drawBoard()
        self.checkCommands()
        pygame.display.update()

    def play(self, notes):
        for intervalNotes in notes:
            self.instrument.play_chord(intervalNotes, self.volume, self.duration)
            if keyboard.is_pressed("s"):
                return

    def run(self):
        run = True
        while run:
            pygame.time.delay(0)
            
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

UI(height=750, width=1500, cols=100, borderWidth=1, octaves=2).run()