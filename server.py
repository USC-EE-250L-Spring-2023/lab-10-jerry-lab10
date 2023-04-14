# Team members: Jerry Appelhans
# Link to Github repo: https://github.com/USC-EE-250L-Spring-2023/lab-10-jerry-lab10

from flask import Flask, request, jsonify

from main import process1, process2

#
import pandas as pd
import plotly.express as px
#

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

# TODO: Create a flask app with two routes, one for each function.
# The route should get the data from the request, call the function, and return the result.
@app.route('/process1', methods=['POST'])
def offload_1():
    data1 = request.get_json()
    res = process1(data1)
    return jsonify(res)

@app.route('/process2', methods=['POST'])
def offload_2():
    data2 = request.get_json()
    res = process2(data2)
    return jsonify(res)

# Extra endpoint that I added to save the create and save the plot on my laptop
# See README for explanation
@app.route('/save', methods=['POST'])
def save_image():
    data = request.get_json()
    df = pd.DataFrame(data, columns=['method', 'runtime_mean', 'runtime_std'])
    print(df)
    fig = px.bar(
        df, 
        x="method", 
        y="runtime_mean", 
        error_y="runtime_std", 
        labels={
            "runtime_mean": "Average Runtime (s)",
            "method": "Processes Offloaded",
        },
        title="Plot of Offloading Runtimes",
    )

    # TODO: save plot to "makespan.png"
    fig.write_image("makespan.png", engine="kaleido")

    return jsonify(1)

if __name__ == '__main__':
    app.run(host="0.0.0.0")