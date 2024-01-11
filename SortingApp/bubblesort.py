from tkinter import *
import random
import time



def visualiser():

    root = Tk()
    root.title('Bubble Sort Visualization')
    root.maxsize(1600, 1080)
    root.config(bg='#138F89')

    # Variables
    runTime = time.time()

    

                    
    def update_runTime(timeLabel,startTime):
        timeLabel.config(text=time.time() - runTime)

    def drawArray(data, colorArray, canvas):
        canvas.delete("all")
        x_width = 560 / (len(data) + 1)
        offset = 3
        spacing = x_width / 2
        normalizedData = [ i / max(data) for i in data]
        for i, height in enumerate(normalizedData):
            
            x0 = i * x_width + offset + spacing
            y0 = 460 - height * 340
            
            x1 = (i + 1) * x_width + offset
            y1 = 460

            canvas.create_rectangle(x0, y0, x1, y1, fill=colorArray[i])
        
        root.update_idletasks()


    def bubble_sort(data, drawArray, timeTick, canvas):
        global runTime
        runTime = time.time()
        
        for _ in range(len(data)-1):
            for j in range(len(data)-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    drawArray(data, ['yellow' if x == j or x == j+1 else 'red' for x in range(len(data))], canvas)
                    time.sleep(timeTick)
                    update_runTime(timer2,runTime)

    def generateArray():
        global data1
        global data2
        data1 = []
        data2 = []

        size = int(sizeEntry.get())
        data1 = random.sample(range(1, size+1), size)

        data2[:] = data1[:]
        drawArray(data2,['red' for x in range(len(data2))], canvas2)

    def startAlgorithm():
        global data1
        global data2

        global runTime
        runTime = time.time()

        bubble_sort(data2, drawArray, speedScale.get(), canvas2)
        drawArray(data2, ['green' for x in range(len(data2))], canvas2)

    # Canvas & Frame

    labelFrame2 = Frame(root, width = 300, height = 20, bg='#6ADF27')
    labelFrame2.grid(row= 0,column=2, padx=20,pady=20)
    Label(labelFrame2, text="BUBBLE SORT", fg='white', bg='#6ADF27', font=('Verdana', 12, 'bold')).grid(row=0, column=2)

    canvas2 = Canvas(root, width=560, height=460, bg = 'white')
    canvas2.grid(row=1, column=2, padx=10, pady=10)

    buttonFrame = Frame(root, width = 300, height = 100, bg ='#6ADF27')
    buttonFrame.grid(row = 1, column=0, padx =10, pady=10)


    labelFrame4 = Frame(root, width = 500, height = 30, bg='#6ADF27')
    labelFrame4.grid(row= 2, column=2, padx=20,pady=20)
    Label(labelFrame4, text="Running Time (seconds):", fg='white', bg='#6ADF27', font=('Courier New', 10, 'bold')).grid(row=1,column=2)
    timer2 = Label(labelFrame4, text="", fg='green', bg="white")
    timer2.grid(row=2, column=2, pady=20)

    # Buttons
    Label(buttonFrame, text="Insert number of array (integer):", fg='white', bg='#6ADF27', font=('Verdana', 10, 'bold')).grid(row=0, column=0, padx=5,pady=5)

    sizeEntry = Entry(buttonFrame)
    sizeEntry.grid(row=1, column=0, padx=5,pady=5)

    generateButton = Button(buttonFrame, text="Generate", fg='white', bg='blue', font=('Verdana', 10, 'bold'), command=generateArray)
    generateButton.grid(row=2, column=0, padx=5, pady=5)

    speedScale = Scale(buttonFrame, from_=0.001, to=1.000, length=300, digits=3, resolution=0.001, orient=HORIZONTAL, label="Select Speed [seconds]")
    speedScale.grid(row=3, column=0, padx=5, pady=5)

    startButton = Button(buttonFrame, text="START", fg='white', bg='red', font=('Verdana', 10, 'bold'), command=startAlgorithm)
    startButton.grid(row=4, column=0, padx=5, pady=5)

    root.mainloop()
