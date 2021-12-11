#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import traceback
import asyncio
import sys

HOST = sys.argv[1]
PORT = sys.argv[2]

entranceList = []
totalCars = 0


async def newConnection(reader, writer):
    print("starting the connection.... \n")

    
    try:
        writer.write(b'Welcome! Please enter the street name: \n')
        await writer.drain()       
        encodedData = await reader.readline()
        streetName = encodedData.decode('utf-8').strip()
        #If street name is blank, dis allow
        objectPos = len(entranceList) #checking the length before adding a new item to give us the index where the item WILL be in the array

        #entranceList.append({data: 0}) could do it with object to store name with num, for now lets just store the count

        entranceList.append( 0 )
        print(entranceList)


        writer.write(('Counter started for ' + streetName + ' \n').encode('utf-8'))
        await writer.drain()

        while (True):
            global totalCars
            try:       
                encodedData = await reader.readline()
                newCarCount = int(encodedData.decode('utf-8').strip())

                print(newCarCount)
                entranceList[objectPos] = (entranceList[objectPos] + newCarCount) 
                totalCars = (totalCars + newCarCount)

                print(str(entranceList[objectPos] ) + " is the current count for entrance at index" + str(objectPos))
                print("total cars seen is : " + str(totalCars))


            except Exception as details:
                print(details)
                writer.write(("Invalid Input \n").encode('utf-8'))
                await writer.drain()
                traceback.print_exc()
                pass


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