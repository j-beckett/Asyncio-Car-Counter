#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import traceback
import asyncio
import sys

HOST = sys.argv[1]
PORT = sys.argv[2]

entranceList = []
totalCars = 0

async def waitForTally(writer, reader, objectPos):
        while (True):
            global totalCars
            try:       
                encodedData = await reader.readline()
                newCarCount = int(encodedData.decode('utf-8').strip())

                print(newCarCount)


                #these next two lines actually adds the newly seen cars to the connections position in the array. 
                entranceList[objectPos] = (entranceList[objectPos] + newCarCount) 
                totalCars = (totalCars + newCarCount)

            except Exception as details:
                print(details)
                writer.write(("Invalid Input \n").encode('utf-8'))
                await writer.drain()
                traceback.print_exc()
                pass

async def updateClientTotal(writer):
    while (True):
        writer.write(("total cars seen is now " + str(totalCars)+ " \n").encode('utf-8'))
        await writer.drain()
        await asyncio.sleep(2)


async def newConnection(reader, writer):

    print("starting the connection.... \n")

    try:
        writer.write(b'Welcome! Please enter the street name: \n')
        await writer.drain()       
        encodedData = await reader.readline()
        streetName = encodedData.decode('utf-8').strip()
        #If street name is blank, dis allow

        #the program needs to be aware of what position in the index it is for everything to work smoothly.
        #IE: the first connection will be position 0. SO the function waitForTally needs to know that it's only updating the number at that specific position
        objectPos = len(entranceList) #checking the length before adding a new item to give us the index where the item WILL be in the array


        #entranceList.append({data: 0}) could do it with object to store name with num, for now lets just store the count

        #Init the count at the newest connection to 0
        entranceList.append( 0 )
        print(entranceList)


        writer.write(('Counter started for ' + streetName + ' \n').encode('utf-8'))
        await writer.drain()
        

        taskT = asyncio.create_task(waitForTally(writer, reader, objectPos))
        taskC = asyncio.create_task(updateClientTotal(writer))

    #two tasks needed to balance the thread. Otherwise, either the function awaiting input or the function sending over the total count will block. 
    #This makes everything run so smoothly!! 
        await taskT
        await taskC
        

    except Exception as e:
        print("failed to READ the message")
        traceback.print_exc()
        return
        pass

    #print(data)
            
        






async def main():
    try:
        server = await asyncio.start_server(newConnection, HOST, PORT)   #first arg is what will be run by our server
        await server.serve_forever() # without this, program terminates
    except Exception as details:
                    print(details)
                    #traceback.print_exc()
                    pass 


asyncio.run(main())