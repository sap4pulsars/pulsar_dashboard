import glob, sys, os
import numpy as np
from data_import import parse_pfd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import json
import ast
from ai_score import score
pfd_files = glob.glob('/home/psr/visualization_project_sap/pfd/PFFTS_4745_01_0001_pfd/*.pfd')
pfd_files_one = glob.glob('/home/psr/visualization_project_sap/pfd/PFFTS_4745_01_0001_pfd/candidate_21702_beam_03_segment_2_2260.58ms_Cand.pfd')
model = 'clfl2_PALFA.pkl'
#text = [parse_pfd(f), score(f, model) for f in pfd_files_one]

#'\n'.join(['%s %s' % (pfdfile[i], AI_scores[i]) for i in range(len(pfdfile))])
#scores = [score(f, model) for f in pfd_files_one]


# metadata = [parse_pfd(f) for f in pfd_files]
# scores = [score(f, model)[0] for f in pfd_files]
# for i, g in enumerate(metadata):
#     g['palfa_score'] = scores[i]
#     with open('data.txt', 'a') as f:
#         json.dump(g, f)
#         f.write(os.linesep)



with open('data.txt') as f:
    data = [json.loads(line) for line in f]
        

# result = [json.dumps(f, open("data.txt",'a')) for f in metadata]
#for i in range(len(data)):
	#print data[i]['palfa_score']



labelx = sys.argv[1]
labely = sys.argv[2]
x = [f[labelx] for f in data]
y = [f[labely] for f in data]




plt.title('2D Histogram')
h=plt.hist2d(x, y, bins=40, cmap='Blues', vmax = 8)
plt.colorbar(h[3])
plt.xlabel(labelx)
plt.ylabel(labely)
#plt.xlim(0,0.2)
plt.show()
# def append_record(record):
    

# # demonstrate a program writing multiple records
# for i in range(10):
#     my_dict = {'number':i}
#     append_record(my_dict)
#with open('data.txt', 'r') as tweets_file:
    #tweets_data = [ast.literal_eval(line) for line in tweets_file]

#print tweets_data['palfa_score']
#print d2['palfa_score']

# with open('data.txt', 'r') as f:
#     metadata = f.read()
#     metadata1 = getattr(metadata , 'palfa_score')
#     print metadata1
    #xname = sys.argv[1]
    #yname = sys.argv[2]
    #if name in self.whip:
      #  print self.whip[name]
    #metadata1 =  ast.literal_eval(metadata)

#print metadata1['palfa_score']
# data = # Uploaded to http://pastebin.com/tjLqM9gQ

# Create a meshgrid of coordinates (0,1,...,N) times (0,1,...,N)




# plt.show()
#y, x = np.mgrid[:len(x), :len(y)]
# duplicating the grids
# xcoord, ycoord = np.array([x] * len(data)), np.array([y] * len(data))
# # compute histogram with coordinates as x,y
# h, xe, ye = np.histogram2d(
#     xcoord.ravel(), ycoord.ravel())

# # Projected histograms inx and y
# hx, hy = h.sum(axis=0), h.sum(axis=1)

# # Define size of figure
# fig = plt.figure(figsize=(20, 15))
# gs = gridspec.GridSpec(10, 12)

# # Define the positions of the subplots.
# ax0 = plt.subplot(gs[6:10, 5:9])
# axx = plt.subplot(gs[5:6, 5:9])
# axy = plt.subplot(gs[6:10, 9:10])

# ax0.imshow(h, cmap=plt.cm.viridis, interpolation='nearest',
#            origin='lower', vmin=0.)

# # Remove tick labels
# nullfmt = NullFormatter()
# axx.xaxis.set_major_formatter(nullfmt)
# axx.yaxis.set_major_formatter(nullfmt)
# axy.xaxis.set_major_formatter(nullfmt)
# axy.yaxis.set_major_formatter(nullfmt)

# # Top plot
# axx.plot(hx)
# axx.set_xlim(ax0.get_xlim())
# # Right plot
# axy.plot(hy, range(len(hy)))
# axy.set_ylim(ax0.get_ylim())

# fig.tight_layout()
