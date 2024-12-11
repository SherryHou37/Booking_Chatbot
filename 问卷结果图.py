import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Strongly Disagree': [5, 3, 2, 1, 4, 5, 6, 7, 3, 4],
    'Disagree': [10, 6, 8, 5, 7, 8, 6, 5, 7, 9],
    'Neutral': [15, 18, 12, 14, 13, 11, 9, 10, 14, 12],
    'Agree': [30, 25, 28, 34, 29, 35, 37, 40, 38, 36],
    'Strongly Agree': [40, 48, 42, 39, 41, 41, 42, 38, 42, 39]
}


df = pd.DataFrame(data, index=[f'Q{i+1}' for i in range(10)])


ax = df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')


plt.xlabel('Questions')
plt.ylabel('Number of Responses')
plt.title('Likert Scale Responses to Survey Questions')


plt.legend(title="Responses", bbox_to_anchor=(1, 1), loc='upper left')


plt.xticks(rotation=0)


plt.tight_layout()
plt.show()
