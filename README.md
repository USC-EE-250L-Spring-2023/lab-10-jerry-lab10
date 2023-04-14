# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- Jerry Appelhans

## Important Note
My RPi was unable to save the image properly because kaleido was not working.  Whenever I tried to run my code, I received the issue shown below.  I tried running the command, and it said that kaleido was already installed.  I uninstalled, and reinstalled it, but I still got the exact same error message.

    ValueError:
    Image export using the "kaleido" engine requires the kaleido package,
    which can be installed using pip:
        $ pip install -U kaleido

However, kaleido works perfectly fine on my local windows machine.  To circumvent this issue, instead of saving the image in main.py on the RPi, I sent another POST request to the server containing all the test results.  Then in the server.py, I wrote the code to create and save the plot on my windows machine.


## Lab Question Answers

Question 1: Under what circumstances do you think it will be worthwhile to offload one or both
of the processing tasks to your PC? And conversely, under what circumstances will it not be
worthwhile?

Answer: It is worthwhile to offload one or both of the processing tasks if the total time it takes to tranfer the data to the laptop, processes it, and send it back is less that the time it would take to just process the data directly on the RPi.  This depends on a variety of factors.  One of these is the type of computation.  Certain processes will benefit more from the increased performance of the laptop while others may be relatively unaffected.  Another factor in this decision is the network status.  If the network is very congested, it may take a long time to transfer the data between the RPi and the laptop.  In this case, it may still be faster to just process the data on the RPi even though the laptop could be faster.


Question 2: Why do we need to join the thread here?

Answer: The join function tells the main function to wait until the thread is finished with its processing.  After it is done, the main function can continue normally.


Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
  See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
  ChatGPT is also good at explaining the difference between parallel and concurrent execution!
  Make sure to cite any sources you use to answer this question.

Answer: Concurrency is when multiple tasks run in overlapping periods.  This gives the illusion that the tasks are happening at the same time, the in reality, the CPU is just switching between them rapidly.  Parallelism is when tasks actually run at the same time on different CPUs.  In our code, when we offload one of the functions, we are using parallelism because when the process is offloaded, the RPi works on one, and our laptop works on the other at the same time.


Question 4: What is the best offloading mode? Why do you think that is?

Answer: The best offloading mode is "both" with an average time of 0.7 seconds.  This makes sense because the laptop is so much faster than the RPi that it is quicker to send both sets of data over the network.


Question 5: What is the worst offloading mode? Why do you think that is?

Answer: The worst offloading mode is "None" with an average time of 5.2 seconds.  This makes sense because the RPi is very slow at doing the computations.


Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
  What kind of processing functions would be more likely to be used in a real-world application?
  When would you want to offload these functions to a server?

Answer: In a real-world application, 