import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def dotify(dictionary: dict):
    dictionary = dotdict(dictionary)
    for k, v in dictionary.items():
        if type(v) == dict:
            dictionary[k] = dotify(v)
    return dictionary

with open('test/form_Информирование_клиента.json', 'r', encoding='utf-8') as file:
    data = dotify(json.load(file))

# with_debug = list(filter(lambda x: 'debug' in x.keys(), [dotify(item).content for item in data.component.diagram.nodes]))
# with_debug += list(filter(lambda x: 'debug' in x.keys(), [dotify(item).content for item in data.component.diagram.connectors]))

# print(*[dotify(item).scriptName for item in with_debug], sep='\n')

records = [{'x': dotify(item).position.x, 'y': dotify(item).position.y, 'type': dotify(item).type, 'name': dotify(item).content.scriptName or str(dotify(item).content.dispAction) + ' ' + str(dotify(item).content.widget)} for item in data.transferContext.context.data.component.diagram.nodes]
types = np.array([dotify(item).type for item in data.transferContext.context.data.component.diagram.nodes])
# name_col = np.where(types == 'EventNode', )
df = pd.DataFrame.from_records(records)
# print(df.head())
# print(*types, sep='\n')

fig = px.scatter(df, x="x", y="y", color='type', hover_data='name')
fig['layout']['yaxis']['autorange'] = "reversed"
fig.show()