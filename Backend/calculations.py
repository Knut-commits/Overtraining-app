def calculate_score(Heart_rate,sleep,Base_heart_rate):
    
    #calculates the score based on the inputted current retsing heart rate, and other input data and comapares it too the calibration data, whihc is their normal resting heart rate
    diff = Heart_rate - Base_heart_rate

    if diff < 5:
        Hr_score = 0
    elif diff < 10:
        Hr_score = 2
    elif diff < 15:
        Hr_score = 5
    elif diff < 20:
        Hr_score = 7
    elif diff < 25:
        Hr_score = 8
    else:
        Hr_score = 9
    
    #this is deciding the heart rate portion of the overtriang score hwoever it has a maxiumum of 9 meaning only 9 out of the 10 points are can be due to heart rate

    Over_training_score = (Hr_score + ((10-sleep)/100)) # so this is my frist draft of the score so it someone were to have a resting heart rate 25 beats over their baseline resting heart rate and had a sleep score of 100 out of 100 they would receive an overtriang score of 10/10

    if Over_training_score >=7.0:
        descriptor = "Overtrained, rest is recommended"
    elif Over_training_score >= 4.0:
        descriptor = " borderlining overtraining, watch your training load"
    elif Over_training_score >= 2.0:
        descriptor = "not yet overtrained but can be if not properly recovering"
    else:
        descriptor = " healthy training, keep it up, may start increasing load"
    
    
    return Over_training_score, descriptor