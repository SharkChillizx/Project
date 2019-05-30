import statistics as st

def factor_score(association_score, threshold, data_source_weights, crime_weights):
    final_risk_score = 0.0
    total_data_source_weights = np.sum(data_source_weights)
    average_data_source_weight = round(
        np.divide(total_data_source_weights, len(data_source_weights)), 3)

    total_crime_weights = np.sum(crime_weights)
    average_crime_weight = np.divide(
        total_crime_weights, len(crime_weights))
    
    #note: important when avg_crime_weight is None
    if math.isnan(average_crime_weight):
        average_crime_weight = 0.0
    
    #note: important when avg_data_source_weight is None
    if math.isnan(average_data_source_weight):
        average_data_source_weight = 0.0

    g_mean = gmean([average_data_source_weight, average_crime_weight])

    score_delta = np.subtract(1.0, association_score)
    threshold_delta = np.absolute(
        np.subtract(association_score, threshold))
    crime_delta = np.absolute(np.subtract(g_mean, threshold))
    
    # find max from the data source weights
    max_weight = max(data_source_weights)
    
    #if max_weight == 1.0 and association_score == 1.0:
        #final_risk_score = association_score # 2.0
    if max_weight == 1.0 and association_score >= 0.9:
        final_risk_score = association_score # 3.0
    else:
        if g_mean == 0:
            if association_score <= 0.2:
                final_risk_score = np.power(association_score, 2)
            elif association_score >= threshold:
                final_risk_score = np.subtract(np.multiply(
                    association_score, threshold), np.multiply(score_delta, threshold))
            else:
                final_risk_score = np.multiply(
                    np.reciprocal(np.exp(2*score_delta)), threshold)
        if g_mean >= threshold:
            if association_score <= 0.2:
                final_risk_score = st.harmonic_mean([association_score, g_mean]) + np.multiply(
                    g_mean, threshold) + np.subtract(np.multiply(g_mean, threshold), np.multiply(crime_delta, threshold_delta))
            elif association_score >= threshold:
                final_risk_score = st.harmonic_mean([association_score, g_mean]) + np.multiply(
                    crime_delta, association_score) + np.multiply(threshold_delta, g_mean)
            else:
                final_risk_score = st.harmonic_mean(
                    [association_score, g_mean]) + np.multiply(threshold_delta, g_mean)
        if 0 < g_mean < threshold:
            if association_score <= 0.2:
                final_risk_score = st.harmonic_mean([association_score, g_mean]) + np.multiply(
                    0.8, np.subtract(np.multiply(g_mean, threshold), np.multiply(crime_delta, threshold_delta)))
            elif association_score >= threshold:
                final_risk_score = st.harmonic_mean([association_score, g_mean]) + np.multiply(
                    0.8, np.multiply(crime_delta, association_score) + np.multiply(threshold_delta, g_mean))
            else:
                final_risk_score = st.harmonic_mean(
                    [association_score, g_mean]) + np.multiply(0.8, np.multiply(threshold_delta, g_mean))

        if final_risk_score > 1:
            final_risk_score = np.subtract(
                1, 0.001 * np.reciprocal(np.exp(np.subtract(final_risk_score, 1))))

    return round(final_risk_score, 3)