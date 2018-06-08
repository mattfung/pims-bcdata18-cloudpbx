def evaluaterow(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, delay_sum, connect_duration):

    calc_sum = get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)

    final_sum = (delay_sum + calc_sum)/(connect_duration*1000)

    return final_sum


def get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10):
    top_sum = 0
    n = 1
    w1 = 1
    w2 = 2
    w3 = 3
    w4 = 4
    w5 = 5
    w6 = 6
    w7 = 7
    w8 = 8
    w9 = 9
    w10 = 10

    top_sum += 20 * n * (a1) * (w1 - 1)
    n += 1
    top_sum += 20 * n * (a2) * (w2 - 1)
    n += 1
    top_sum += 20 * n * (a3) * (w3 - 1)
    n += 1
    top_sum += 20 * n * (a4) * (w4 - 1)
    n += 1
    top_sum += 20 * n * (a5) * (w5 - 1)
    n += 1
    top_sum += 20 * n * (a6) * (w6 - 1)
    n += 1
    top_sum += 20 * n * (a7) * (w7 - 1)
    n += 1
    top_sum += 20 * n * (a8) * (w8 - 1)
    n += 1
    top_sum += 20 * n * (a9) * (w9 - 1)
    n += 1
    top_sum += 20 * n * (a10) * (w10 - 1)

    return (top_sum)


#df = df.assign(qualfun=df_qualfun)
#df.compute()
#dfqf = df_qualfun.compute()
#
##qualfun for a
df['a_qualfun'] = df.apply(lambda df2: pd.Series(evaluaterow(df2['a_sl1'],df2['a_sl2'],df2['a_sl3'],df2['a_sl4'],df2['a_sl5'],df2['a_sl6'],df2['a_sl7'],df2['a_sl8'],df2['a_sl9'],df2['a_sl10'],df2['a_delay_sum'],df2['connect_duration'])),axis=1)
 #qualfun for a
df['b_qualfun'] = df.apply(lambda df2: pd.Series(evaluaterow(df2['b_sl1'],df2['b_sl2'],df2['b_sl3'],df2['b_sl4'],df2['b_sl5'],df2['b_sl6'],df2['b_sl7'],df2['b_sl8'],df2['b_sl9'],df2['b_sl10'],df2['b_delay_sum'],df2['connect_duration'])),axis=1)
