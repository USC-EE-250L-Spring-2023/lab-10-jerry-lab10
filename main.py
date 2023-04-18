# Team members: Jerry Appelhans
# Link to Github repo: https://github.com/USC-EE-250L-Spring-2023/lab-10-jerry-lab10

import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px
# import kaleido

import warnings
warnings.filterwarnings("ignore")

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
        Summary: This function finds the next highest prime number for each element in a list of integers.
        Inputs: list of arbitrary integers
        Outputs: list of prime numbers
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
        Summary: This function finds the next highest perfect square for each element in a list of integers.
        Inputs: list of arbitrary integers
        Outputs: list of perfect squares
    """
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
        Summary: This function subtracts the elements in data2 from data1 entrywise.  Then it finds the average value of this new list.
        Inputs: Lists of ints, data1 and data2
        Outputs: Average difference between the elements in data1 and data2
    """
    
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://172.20.10.6:5000' # TODO: Change this to the IP address of your server
# offload_url = 'http://127.0.0.1:5000'

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    data1 = []
    data2 = []
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        # data1 = None
        def offload_process1(data):
            global data1
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/process1', json=data)
            # response = requests.post(f'{offload_url}')
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        # data2 = None
        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/process2', json=data)
            data2 = response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data2 = process1(data)
        thread.join()
        pass
    elif offload == 'both':
        # TODO: Implement this case
        # data1 = None
        # data2 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/process1', json=data)
            data1 = response.json()
        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            response = requests.post(f'{offload_url}/process2', json=data)
            data2 = response.json()
        
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        thread.join()

        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        thread.join()
        pass

    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference

    data = []
    methods = [None, "process1", "process2", "both"]
    for i in range(0,4):
        runtimes = []
        # runtimes = [0,0,0,0,0]
        method = methods[i]
        print(method) ####################################################################
        for j in range(0,5):
            start = time.time()
            run(method)
            end = time.time()
            total = end-start
            print(total) ##############################################################
            runtimes.append(total)
            # runtimes[j] = total
        # print(runtimes)
        print("Mean:", np.mean(runtimes))
        print(" STD:", np.std(runtimes))
        if method == None:
            data.append(("None", np.mean(runtimes), np.std(runtimes)))
        else:
            data.append((method, np.mean(runtimes), np.std(runtimes)))

    # data = []
    # methods = [None, "process1", "process2", "both"]
    # for i in range(0,4):
    #     runtimes = [0,0,0,0,0]
    #     method = methods[i]
    #     print(method) ####################################################################
    #     for j in range(0,5):
    #         start = time.time()
    #         # run(method)
    #         end = time.time()
    #         total = end-start
    #         print(total) ##############################################################
    #         # runtimes.append(total)
    #         runtimes[j] = total
    #     # print(runtimes)
    #     # print("Mean:", np.mean(runtimes))
    #     # print(" STD:", np.std(runtimes))
    #     if method == None:
    #         data.append(("None", i+1, 0.1))
    #     else:
    #         data.append((method, i+1, 0.1))


    # df = pd.DataFrame(data, columns=['method', 'runtime_mean', 'runtime_std'])

    # print(df)

    response = requests.post(f'{offload_url}/save', json=data)


    '''
    Note: I moved this code to create and save the image to server.py.  See README for explanation
        # TODO: Plot makespans (total execution time) as a bar chart with error bars
        # Make sure to include a title and x and y labels
        # fig = px.bar(
        #     df, 
        #     x="method", 
        #     y="runtime_mean", 
        #     error_y="runtime_std", 
        #     labels={
        #         "runtime_mean": "Average Runtime (s)",
        #         "method": "method of offloading",
        #     },
        #     title="Plot of Offloading Runtimes",
        # )

        # TODO: save plot to "makespan.png"
        # fig.write_image("makespan.png", engine="kaleido")
    '''
    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()
