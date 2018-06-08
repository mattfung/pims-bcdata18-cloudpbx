def  evaluaterow (a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, delay_sum, connect_duration):
    calc_sum = get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)
    final_sum = (delay_sum + calc_sum)/(connect_duration*1000 + calc_sum)
    return final_sum


def get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10):
    top_sum = 0
    n = 1
    w1 = 1
    w2 = 1
    w3 = 1
    w4 = 1
    w5 = 1
    w6 = 1
    w7 = 1
    w8 = 1
    w9 = 1
    w10 = 1

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

# # df_qualfun_a 
# df['qualfun_a'] = df.apply(lambda df2: evaluaterow(df2['a_sl1'],df2['a_sl2'],\
#     df2['a_sl3'],df2['a_sl4'],df2['a_sl5'],df2['a_sl6'],df2['a_sl7'],\
#     df2['a_sl8'],df2['a_sl9'],df2['a_sl10'],df2['a_delay_sum'],df2['connect_duration']),axis=1)

# # # df_qualfun_b
# df['qualfun_b'] = df.apply(lambda df2: evaluaterow(df2['b_sl1'],df2['b_sl2'],\
#        df2['b_sl3'],df2['b_sl4'],df2['b_sl5'],df2['b_sl6'],df2['b_sl7'],\
#        df2['b_sl8'],df2['b_sl9'],df2['b_sl10'],df2['b_delay_sum'],\
#        df2['connect_duration']),axis=1)