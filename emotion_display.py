import text_analysis

def main(txt):
    d=text_analysis.get_emotion(txt)
    output=""
    d1={"Happy": " :)", "Sad": " :(", "Fear": " 0_0","Surprise": " o.o","Angry": " >:("}
    d={k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
    for i in d:
        if d[i] >0:
            output+=d1[i]
    return output
if __name__ == '__main__':
    print(main("I am so very dissapointed that you cheated on me I gave you my love and this is what I got"))