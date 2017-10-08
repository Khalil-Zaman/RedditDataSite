from plotly import __version__
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import date
import requests

def get_page_source(reddit):
    r = requests.get("http://redditmetrics.com/r/"+reddit)
    return (r.text)

def get_after(data, sub, max_after=0):
    a_index = str(data)
    a_index = a_index.index(sub) + len(sub)
    if max_after == 0:
        return data[a_index:]
    else:
        return data[a_index:(a_index + max_after)]


# Strip anything at the end that's not a number
def strip_ending(string):
    str_len = len(string) - 1
    counter = 0
    while string[str_len-counter] not in "0123456789":
        counter += 1
    return string[:-counter]


def number_of_subscribers(reddit):
    source = get_page_source(reddit)
    data = source.rsplit('\n')
    start_collecting = False
    subscribers_data = []
    year_data = []
    for i in range(0, len(data)):
        if start_collecting is True:
            if "a" not in data[i]:
                return subscribers_data, year_data
            elif "data" not in data[i]:
                number = get_after(data[i], "a: ")
                number = strip_ending(number)
                year = get_after(data[i], "y: \'", 12)
                year = strip_ending(year)
                year_data.append(year)
                subscribers_data.append(int(number))
        elif ("total-subscribers" in data[i]) and ("data" in data[(i+1)]):
            start_collecting = True
    return subscribers_data, year_data


def subscriber_grow_plot(*subreddits, difference=False):
    data = []
    diff1 = []
    diff2 = []
    for title in subreddits:
        subscribers, dates = number_of_subscribers(title)
        if difference is False:
            trace = Scatter(x=dates, y=subscribers, mode='lines', name=title)
            data.append(trace)
        else:
            if len(diff1) == 0:
                diff1 = subscribers
            else:
                diff2 = subscribers
    if difference is True:
        the_diff = []
        for i in range(0, len(diff1)):
            the_diff.append(abs(diff1[i] - diff2[i]))
        trace = Scatter(x=dates, y=the_diff, mode='lines', name=title)
        data.append(trace)
    plot(data)

#print (number_of_subscribers("exmuslim"))
subscriber_grow_plot("islam", "exmuslim")
