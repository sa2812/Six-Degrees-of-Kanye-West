import networkx as nx
import matplotlib.pyplot as plt
import pickle

fl = file('multi.pkl', 'rb')
pkl = pickle.load(fl)

print type(pkl)