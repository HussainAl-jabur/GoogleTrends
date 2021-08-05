from flask import Flask, render_template, request
from pytrends.request import TrendReq
import matplotlib.pyplot as plt

pytrend = TrendReq()

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    kw_list = []

    if request.method == 'POST':
        Topic1 = request.form.get('Topic1')
        Topic2 = request.form.get('Topic2')
        kw_list.append(Topic1)
        kw_list.append(Topic2)


        pytrend.build_payload(kw_list, timeframe='2020-12-01 2021-01-01', geo='US')

        interest_over_time_df = pytrend.interest_over_time()
        plt.style.use('ggplot')
        plot_searchterms(interest_over_time_df)
        plt.savefig("static/Graph.png")
        return render_template('index.html', Graph='Graph.png')

    return render_template('index.html')

def plot_searchterms(df):
    """Plots google trends


    Parameters
    ----------
    df: pandas dataframe
        As returned from pytrends, without the "isPartial" column

    Returns
    -------
    ax: axis handle
    """
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)
    df.plot(ax=ax)
    plt.ylabel('Relative search term frequency')
    plt.xlabel('Date')
    plt.ylim((0, 120))
    plt.legend(loc='lower left')
    return ax

if __name__ == '__main__':
    app.run(debug=True)