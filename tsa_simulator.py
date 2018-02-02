"""
Dillon Sienko
CS 200
10/5/2017
Lab 6
tsa_simulator.py
"""

# import necessary modules
import tsa_lines
import passenger
import random

def no_preCheck(num_scanLanes,num_min,prob_perSec,t1,t2):
    """Runs the TSA simulation without TSA PreCheck."""
    
    # *** ID Line ***
    # initialize id line
    id_line = tsa_lines.IDLine()  
    
    # *** SCANNER Lines *** 
    # create scan line(s) dictionaries 
    scan_linesDict = {}      # dictionary for lines themselves
    scan_linesLen = {}       # dictionary for lengths of scan lines
    scan_linesTimes = {}     # dictionary for scan line times (for passenger to complete line)
    # create keys and values for line dictionary and times dictionary
    for i in range(1,num_scanLanes+1):
        scan_linesDict['scan_line{0}'.format(i)] = tsa_lines.ScannerLane()
        scan_linesTimes['scan_line{0}'.format(i)] = []

    # main simulation loop
    num_minSec = num_min * 60     # convert minutes to seconds
    pass_number = 1               # initialize passenger naming value
    pass_count = 0                # initialize count of passenger
    total_timeList = []           # intialize list to store times to complete full simulation

    # from time 1 until end of simulation time
    for i in range(1,num_minSec+1):
        
        # add people to ID line
        if (random.random() < prob_perSec) == True:

            # create passenger instance and update it's number value
            pass_in = passenger.Passenger()
            pass_in._element = pass_number
        
            pass_in._startTime = i        # update its line start time
            
            pass_in = tsa_lines.IDLine._Node(pass_in,None)  # add passenger to ID line
            id_line.enqueue(pass_in)
            
            pass_number += 1     # increment passenger counts           
         
        # if line not empty 
        if id_line.is_empty() != True:
            # if in id check for >= t1 seconds pop
            if id_line.first()._element._idStart != 0:
                
                # update lengths of lines in length dictionary
                for key,values in scan_linesDict.items():
                    scan_linesLen[key] = values.__len__()
                    
                # find shortest line
                min_line = min(scan_linesLen,key=scan_linesLen.get)
                
                # if passegner has been at ID check for at least t1 seconds
                if (i - id_line.first()._element._idStart) >= t1:  
                    # if there are open scanner lines
                    if scan_linesLen[min_line] < 10:
                    
                        # remove from id line 
                        pass_out = id_line.dequeue()
                        pass_out = pass_out._element

                        # add passenger to shortest line
                        pass_out._scan_lineStart = i
                        scan_linesDict[min_line].enqueue(pass_out)
                        
        # if line is not empty
        if id_line.is_empty() != True: 
            # if passenger is new to front of line
            if id_line.first()._element._idStart == 0:
                    # start timer for id check
                    id_line.first()._element._idStart = i
        
        # look at each scanner lane
        for key,values in scan_linesDict.items():        
            # if lane empty, ignore
            if scan_linesDict[key].__len__() == 0:
                continue
            else:
                # if passenger just got to front, start his scanner timer
                if scan_linesDict[key].first()._scanStart == 0:
                    scan_linesDict[key].first()._scanStart = i
                # check scanner timer for passenger at front, pop if there for at least t2 seconds
                if (i - scan_linesDict[key].first()._scanStart) >= t2:
                    
                    pass_out = scan_linesDict[key].dequeue()          # remove from scanner lane
                    pass_count += 1                                   # update total compeleted passenger count

                    total_scanTime = (i - pass_out._scan_lineStart)   # time taken for passenger to finish scan line
                    scan_linesTimes[key] += [total_scanTime]          # add that to list of scan line times
                    
                    total_time = (i - pass_out._startTime)/60         # total time taken for passenger to complete simulation
                    total_timeList += [total_time]                    # add that time to list of times
                    
    # **Simulation output**
    # calculate average total time for passenger completion of simulation
    avg_totalTime = sum(total_timeList)/len(total_timeList)
    
    # scanner lane outputs
    scan_linesData = {}
    scans_lens = []
    #loop through dictionary containing scanner line times
    for key,values in scan_linesTimes.items():
        # if the line was not used return zeroes
        if len(scan_linesTimes[key]) == 0:
            scan_linesData[key] = [0,0]
        else: 
            # calculate data for function return
            avg_time = (sum(scan_linesTimes[key])/len(scan_linesTimes[key])/60) 
            scans_lens += [scan_linesLen[key]]
            scan_linesData[key] = [("%.2f" % round(avg_time,2)),len(scan_linesTimes[key])]
      
    # total remaining passengers output
    scans_left = sum(scans_lens)
    ids_left = id_line.__len__()
    total_left = ids_left + scans_left
    
    # create/return  tuple of data to return
    no_preCheck_results = [pass_count,("%.2f" % round(avg_totalTime,2)),scan_linesData,total_left]
    return no_preCheck_results

def preCheck(num_scanLanes,num_min,prob_perSec,prob_preCheck,t1,t3,t2):
    """Runs the TSA simulation with the inclusion of TSA PreCheck."""
    
    # *** ID Lines ***
    # initialize id line
    id_line = tsa_lines.IDLine()
    preCheck_line = tsa_lines.IDLine()
    
    # *** SCANNER LINES *** 
    # create scan lines dictionary and scan line lengths 
    scan_linesDict = {}
    scan_linesLen = {}
    scan_linesTimes = {}
    for i in range(1,num_scanLanes):
        scan_linesDict['scan_line{0}'.format(i)] = tsa_lines.ScannerLane()
        scan_linesTimes['scan_line{0}'.format(i)] = []
    # update dictionaries specifically regarding precheck
    scan_linesDict['preCheck_scan'] = tsa_lines.ScannerLane()
    scan_linesTimes['preCheck_scan'] = []

    # main simulation loop
    num_minSec = num_min * 60
    pass_number = 1
    pass_count = 0
    total_timeList = []

    # from time 1 until end of simulation time
    for i in range(1,num_minSec+1):
         
        # ***ID LINE***
        # add people to ID line
        if (random.random() < prob_perSec) == True:
            
            # create passenger instance and update it's count value
            pass_in = passenger.Passenger()
            pass_in._element = pass_number
            pass_in._startTime = i     # update its line start time
            pass_in = tsa_lines.IDLine._Node(pass_in,None)    # create passenger node
            
            # if they have pre check
            if (random.random() < prob_preCheck) == False:
                id_line.enqueue(pass_in)        # add passenger to precheck line   
            else:
                preCheck_line.enqueue(pass_in)  # add to normal id line
            
            pass_number += 1     # increment passenger counts            
         
        # if line not empty 
        if id_line.is_empty() != True:
            # if in id check for >= t1 seconds pop
            if id_line.first()._element._idStart != 0:
                
                # update lengths of lines in length dictionary
                for key,values in scan_linesDict.items():
                    scan_linesLen[key] = values.__len__()   
                # find shortest line
                min_line = min(scan_linesLen,key=scan_linesLen.get)
                
                # if passegner has been at ID check for at least t1 seconds
                if (i - id_line.first()._element._idStart) >= t1:  
                    # if there are open scanner lines
                    if scan_linesLen[min_line] < 10:
                    
                        # remove passenger from id line
                        pass_out = id_line.dequeue()
                        pass_out = pass_out._element
                        pass_out._scan_lineStart = i   # update scanner line time

                        # add next passenger to shortest scanner line
                        scan_linesDict[min_line].enqueue(pass_out)
                        
        # if line is not empty
        if id_line.is_empty() != True: 
            # if passenger is new to front of line
            if id_line.first()._element._idStart == 0:
                    # start timer for id check
                    id_line.first()._element._idStart = i
                    
        # ***PRE CHECK LINE***
        # if line not empty 
        if preCheck_line.is_empty() != True:   
            # if in id check for >= t1 seconds pop
            if preCheck_line.first()._element._idStart != 0:
                
                # update scan line length for precheck line
                scan_linesLen['preCheck_scan'] = preCheck_line.__len__()
                
                # if passegner has been at ID check for at least t1 seconds
                if (i - preCheck_line.first()._element._idStart) >= t1:             
                    if scan_linesDict['preCheck_scan'].__len__() < 10:
                    
                        # remove from precheck id line
                        pass_out = preCheck_line.dequeue()
                        pass_out = pass_out._element
                        pass_out._scan_lineStart = i      # update scan line start time

                        # add next passenger to shortest precheck scanner line
                        scan_linesDict['preCheck_scan'].enqueue(pass_out)
                        
        # if line is not empty
        if preCheck_line.is_empty() != True: 
            # if passenger is new to front of line
            if preCheck_line.first()._element._idStart == 0:
                    # start timer for id check
                    preCheck_line.first()._element._idStart = i
        
        # look at each scanner lane
        for key,values in scan_linesDict.items():
            
            # if lane empty, ignore
            if scan_linesDict[key].__len__() == 0:
                continue
            else:
                # if passenger just got to front, start his scanner timer
                if scan_linesDict[key].first()._scanStart == 0:
                    scan_linesDict[key].first()._scanStart = i
                
                # if considering pre check scanner line
                if key == 'preCheck_scan':
                    # check scanner timer for passenger at front, pop if there for at least t2 seconds
                    if (i - scan_linesDict[key].first()._scanStart) >= t2:

                        pass_out = scan_linesDict[key].dequeue()         # remove from scanner lane when passenger done 
                        pass_count += 1                                  # update total compeleted passenger count

                        total_scanTime = (i - pass_out._scan_lineStart)  # time taken for passenger to finish scan line
                        scan_linesTimes[key] += [total_scanTime]         # add that time to list of times

                        total_time = (i - pass_out._startTime)/60        # total time taken for passenger to complete who simulation
                        total_timeList += [total_time]                   # add that time to list of times     
                else:
                    # check scanner timer for passenger at front, pop if there for at least t2 seconds
                    if (i - scan_linesDict[key].first()._scanStart) >= t3:

                        # remove from scanner lane when passenger done getting scanned
                        pass_out = scan_linesDict[key].dequeue()
                        # update total compeleted passenger count
                        pass_count += 1

                        # calculate time taken for passenger to fnsih scan line
                        total_scanTime = (i - pass_out._scan_lineStart)
                        # add that time to list of times
                        scan_linesTimes[key] += [total_scanTime]

                        # calculate total time taken for passenger to complete who simulation
                        total_time = (i - pass_out._startTime)/60
                        # add that time to list of times
                        total_timeList += [total_time]
                    
    # **Simulation output**
    # calculate average total time for passenger completion of simulation
    avg_totalTime = sum(total_timeList)/len(total_timeList)
    
    # scanner lane outputs
    scan_linesData = {}
    scans_lens = []
    # loop trhgouh dictionary containing time info
    for key,values in scan_linesTimes.items():
        # if line wasn't used return zeroes
        if len(scan_linesTimes[key]) == 0:
            scan_linesData[key] = [0,0]
        else: 
            # create and update line data
            avg_time = (sum(scan_linesTimes[key])/len(scan_linesTimes[key])/60) 
            scans_lens += [scan_linesLen[key]]
            scan_linesData[key] = [("%.2f" % round(avg_time,2)),len(scan_linesTimes[key])]
      
    # total remaining passengers output
    scans_left = sum(scans_lens)
    ids_left = id_line.__len__()
    total_left = ids_left + scans_left
    
    # create/return tuple of data to return
    no_preCheck_results = [pass_count,("%.2f" % round(avg_totalTime,2)),scan_linesData,total_left]
    return no_preCheck_results
            
def main():
    """Main function that requests and validates user input, and calls the function that runs the simulations."""
    
    # Input/Input Validation
    # input for number of scanner lanes
    print()
    while True:
        try:
            num_scanLanes = int(input("Number of scanner lanes to simulate? "))
            if num_scanLanes < 0:
                print("Sorry, your input must be larger than 0. Try again.")
                continue     
        except ValueError:
            print("Sorry, your input must be an integer. Try again.")
            continue
        else:
            break
            
    # input for number of minutes to simulate
    while True:
        try:
            num_min = int(input("Number of minutes to simulate? "))
            if num_min < 0:
                print("Sorry, your input must be larger than 0. Try again.")
                continue 
        except ValueError:
            print("Sorry, your input must be an integer. Try again.")
            continue
        else:
            break
       
    # input for probability a passenger gets in line each second
    while True:
        try:
            prob_perSec = float(input("Probability that a passenger gets in line each second? "))
            if prob_perSec > 1 or prob_perSec < 0:
                print("Sorry, your input must be between 0 and 1 (inclusive). Try again.")
                continue 
        except ValueError:
            print("Sorry, your input must be between 0 and 1 (inclusive). Try again.")
        else:
            break
            
    # input for ask whether or not to simulate TSA
    while True:
        try:
            tsa_yesNo = input("Simulate TSA PreCheck lane? (y/n) ")
            if tsa_yesNo not in ['y','n','Y','N']:
                print("Sorry, your input must be the values y, Y, n, or N. Try again.")
                continue         
        except ValueError:
            print("Sorry, your input must be the values y, Y, n, or N. Try again.")
            continue
        else:
            break
     
    # input to determine the probability that a given passenger has a TSA PreCheck
    if tsa_yesNo in ['y','Y']:
        while True:
            try:
                prob_preCheck = float(input("Probability that passenger has TSA PreCheck? "))
                if prob_preCheck > 1 or prob_preCheck < 0:
                    print("Sorry, your input must be between 0 and 1 (inclusive). Try again.")
                    continue 
            except ValueError:
                print("Sorry, your input must be between 0 and 1 (inclusive). Try again.")
                continue
            else:
                break
                
    # input for time required to check ID
    while True:
        try:
            time_ID = int(input("Time required to check ID (in seconds)? "))
            if time_ID < 0:
                print("Sorry, your input must be larger than 0. Try again.")
                continue 
        except ValueError:
            print("Sorry, your input must be an integer. Try again.")
            continue
        else:
            break
                
    # input for time required for general passenger to be scanned
    while True:
        try:
            time_scan = int(input("Time required for general passenger to be scanned (in sec)? "))
            if time_scan < 0:
                print("Sorry, your input must be larger than 0. Try again.")
                continue 
        except ValueError:
            print("Sorry, your input must be an integer. Try again.")
            continue
        else:
            break
  
    # input for time required for TSA PreCheck passenger to be scanned
    if tsa_yesNo in ['y','Y']:
        while True:
            try:
                time_preCheckScan = int(input("Time required for a TSA PreCheck passenger to be scanned (in sec)? "))
                if time_preCheckScan < 0:
                    print("Sorry, your input must be larger than 0. Try again.")
                    continue 
            except ValueError:
                print("Sorry, your input must be an integer. Try again.")
                continue
            else:
                break 
             
    # if yes, run tsa precheck simulation
    if tsa_yesNo in ['y','Y']:
        run_simulation(num_scanLanes,num_min,prob_perSec,prob_preCheck,time_ID,time_scan,time_preCheckScan)
    # if no, run simulation without pre check
    else:
        run_simulation(num_scanLanes,num_min,prob_perSec,None,time_ID,time_scan,None)
        
                
def run_simulation(num_scanLanes,num_min,prob_perSec,prob_preCheck,time_ID,time_scan,time_preCheckScan):
    """Function that calls and runs the PreCheck or No PreCheck simulations, and prints the results."""
    
    # if not precheck, run simulation without pre check
    if prob_preCheck == None:
        no_preCheck_results = no_preCheck(num_scanLanes,num_min,prob_perSec,time_ID,time_scan)
        
        # **Output**
        print()
        print("Number of scanners:",num_scanLanes)
        print("Simulation Length:",num_min,"minutes")
        print("Passenger arrival probability:",prob_perSec)
        print("Simulate PreCheck: NO")
        print()
        print("Number of passengers cleared:",no_preCheck_results[0])
        print("Average wait time:",no_preCheck_results[1],"minutes")
    
        scan_linesData = no_preCheck_results[2]
        for key,values in scan_linesData.items():
            print("Avg Lane",key[-1],"Wait Time:", values[0],"minutes", "("+str(values[1])+" people)")  
            
        print()
        print("Total number of passengers in line at end of simulation:",no_preCheck_results[3]) 
        print()
      
    # run simulation with precheck
    else:
        preCheck_results = preCheck(num_scanLanes,num_min,prob_perSec,prob_preCheck,time_ID,time_scan,time_preCheckScan)
       
        # **Output**
        print()
        print("Number of scanners:",num_scanLanes)
        print("Simulation Length:",num_min,"minutes")
        print("Passenger arrival probability:",prob_perSec)
        print("Simulate PreCheck: YES")
        print()
        print("Number of passengers cleared:",preCheck_results[0])
        print("Average wait time:",preCheck_results[1],"minutes")
    
        scan_linesData = preCheck_results[2]
        for key,values in scan_linesData.items():
            if key == 'preCheck_scan':
                print("Avg PreCheck Scan Wait Time:",values[0],"minutes","("+str(values[1])+" people)")
            else:
                print("Avg Lane",key[-1],"Wait Time:", values[0],"minutes", "("+str(values[1])+" people)")  
            
        print()
        print("Total number of passengers in line at end of simulation:",preCheck_results[3]) 
        print()
    
if __name__ == "__main__":
    main()
    