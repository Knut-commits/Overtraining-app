def calculate_score(Heart_rate,sleep,Calibration_data):
    
    #calculates the score based on the inputted current retsing heart rate, and other input data and comapares it too the calibration data, whihc is their normal resting heart rate

    if Heart_rate - Calibration_data['Base_heart_rate'] < 5:
        Hr_score = 0

    if Heart_rate - Calibration_data['Base_heart_rate'] >= 5 and Heart_rate - Calibration_data['Base_heart_rate'] < 10:
        Hr_score = 2
    if Heart_rate - Calibration_data['Base_heart_rate'] >=10 and Heart_rate - Calibration_data['Base_heart_rate']  < 15:
        Hr_score = 4
    if  Heart_rate - Calibration_data['Base_heart_rate'] >=15 and Heart_rate - Calibration_data['Base_heart_rate'] < 20:
        Hr_score = 6
    if Heart_rate - Calibration_data['Base_heart_rate']  >= 20 and Heart_rate - Calibration_data['Base_heart_rate'] < 25:
        Hr_score = 8
    if Heart_rate - Calibration_data['Base_heart_rate'] >=25:
        Hr_score = 9
    #this is deciding the heart rate portion of the overtriang score hwoever it has a maxiumum of 9 meaning only 9 out of the 10 points are can be due to heart rate

    Over_training_score = (Hr_score + (sleep/100)) # so this is my frist draft of the score so it someone were to have a resting heart rate 25 beats over their baseline resting heart rate and had a sleep score of 100 out of 100 they would receive an overtriang score of 10/10

    if Over_training_score >=7.0:
        descriptor - "Overtrained, rest is recommended"
    elif Over_training_score >= 4.0:
        descriptor = " borderlining overtraining, watch your training load"
    elif Over_training_score >= 2.0:
        descriptor = "not yet overtrained but can be if not properly recovering"
    else:
        descriptor = " healthy training, keep it up, may start increasing load"
    
    
    return Over_training_score, descriptor