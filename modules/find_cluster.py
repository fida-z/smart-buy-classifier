import pandas as pd
from pathlib import Path


SEGPATH = Path(__file__).resolve().parent.parent/'data_models'

def load_segment1():
    seg = pd.read_csv(SEGPATH/'seg0.csv')
    return(seg)
def load_segment2():
    seg = pd.read_csv(SEGPATH/'seg1.csv')
    return(seg)
def load_segment3():
    seg = pd.read_csv(SEGPATH/'seg2.csv')
    return(seg)
def load_segment4():
    seg = pd.read_csv(SEGPATH/'seg3.csv')
    return(seg)
def load_kmodes():
    return(pd.read_csv(SEGPATH/'kmodes.csv'))


def get_segment(model_name):

    seg1 = load_segment1()
    seg2 = load_segment2()
    seg3 = load_segment3()
    seg4 = load_segment4()

    seg_count = {}
    for seg, i in zip([seg1,seg2,seg3,seg4],range(1,5)):
        seg_count[i] = seg.loc[seg['model'] == model_name, 'count'].sum()
        
    return(max(seg_count,key=seg_count.get))


def model_popularity(model_name,seg):
    if(seg == 1):
        df = load_segment1()
    elif(seg == 2):
        df = load_segment2()
    elif(seg == 3):
        df = load_segment3()
    elif(seg == 4):
        df = load_segment4()

    return(df[df['model'] == model_name].index + 1)

def segment_analysis(segment):
        kmodes = load_kmodes()
        seg_grp = kmodes.groupby(['Segment'])
        avg_price = seg_grp['price'].mean().loc[segment]
        avg_km = seg_grp['KM driven'].mean().loc[segment]

        return(round(avg_price,2), round(avg_km,2))


