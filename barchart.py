#imports libraries

import matplotlib.pyplot as plt
import pandas as pd 


plt.style.use('bmh')
try:
    df = pd.read_csv('my_file.csv')
except FileNotFoundError:
    print("File not found")
else:
    possible_emotions = ['angry', 'disgust','fear','happy','sad','surprise', 'neutral']
    x = df['Emotion']
    y_count= df['Count']
    y_duration= df['Duration(s)']  
    dominant_emotion=x[y_count.argmax()]
    dominant_count=y_count.max()
    fig, ax=plt.subplots(2,1,figsize=(10, 12))  
    ax[0].set_xlabel('Emotions', fontsize=18)
    ax[0].set_ylabel('Frequency', fontsize=16)
    bars = ax[0].bar(x, y_count)
    messages = {
        'happy': "It's great to see that you're happy!😆",
        'sad': "It's okay to feel sad. You should listen to your favorite song to cheer yourself up.",
        'angry': "You should go for a walk to let off some steam!",
        'fear': "It's okay, take a deep breath.",
        'surprise': "🙀",
        'disgust': "😵‍💫",
        'neutral':"You are Neutral"
    }
    second=y_duration.get(max(y_duration))
    message=messages.get(dominant_emotion)
    ax[0].text(x[y_count.argmax()], y_count.max()+1,f'Dominant Emotion:{dominant_emotion}\n{message}', fontsize=15,ha='center')
    bars[y_count.argmax()].set_color('r')
    ax[1].set_xlabel('Emotions', fontsize=18)
    ax[1].set_ylabel('Duration(s)',fontsize=16)
    ax[1].bar(x, y_duration)

    emo_duration = {second: 0 for second in y_duration}
    f = round(max(emo_duration),1)
plt.show()