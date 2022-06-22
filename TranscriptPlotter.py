import re
import pandas as pd
import pyphen
import matplotlib.pyplot as plt
import seaborn as sns

class TranscriptPlotter:
    
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        content_list = re.split(r'<b>\s*.*\s*<\/b>', text)
        content_list = [s.strip() for s in content_list]

        self.title_list = re.findall(r'<b>\s*(.*)\s*<\/b>', text)

        # TEMP: Figure out how to better align these
        self.content_list = content_list[1:]
    
    def parse(self):
        df = pd.DataFrame({'person': self.title_list, 'lines': self.content_list})

        # take first word of each title
        df['person'] = df['person'].apply(lambda p: p.strip().split(' ')[0])
        # if just number, replace with --TRANSITION--
        df['person'] = df['person'].replace(r'\d+\.', '--TRANSITION--', regex=True)
        # remove common cinematography titles, like CUT, INT, etc.
        df = df[~df['person'].isin(['INT.', 'CUT', '(BEAT)'])]
        # remove things with parentheses
        # df = df[~(df['person'].contains('(') or df['person'].contains(')'))]
        # skip title
        df = df.iloc[2:]
        # if not in top 20 list of chars, then don't include (used to remove redundant stuff)
        top_20 = df['person'].value_counts()[:20]
        df = df[df['person'].isin(top_20.keys())]
        
        # cleaning up lines
        # converting lines into single string for parsing
        df['lines'] = df['lines'].apply(lambda l: ' '.join([line.strip() for line in l.split('\n')]))

        # Performing hyphenation
        pyphen.language_fallback('nl_NL_variant1')
        dic = pyphen.Pyphen(lang='nl_NL')
        df['syllables'] = df['lines'].apply(lambda l: dic.inserted(l).count('-') + 1);
        
        self.df = df

    def plot(self):
        # Get color map
        color_labels = self.df['person'].unique()
        rgb_values = sns.color_palette("Set2", 20)
        color_map = dict(zip(color_labels, rgb_values))

        plt.figure(figsize=(32,10)) # Make it 14x7 inch
        plt.style.use('seaborn-whitegrid') # nice and clean grid

        plt.bar(x=range(0, len(self.df['syllables'])), height=self.df['syllables'], color=self.df['person'].map(color_map)) 

        plt.legend([plt.Rectangle((0, 0), 1, 1, color=color_map[label]) for label in color_labels], color_labels)

        plt.title('The Social Network') 
        plt.xlabel('Syallables') 
        plt.ylabel('Line Number') 
        plt.show()