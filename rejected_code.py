# def sort_powers_lists(self):
    #     powers_lists_dict = {}
    #     span = len(self.powers_lists[0])
    #     for powers in self.powers_lists:
    #         score = 1
    #         for i in range(span):
    #             score *= ((i+1)*math.pi**span) ** (span*powers[i])
    #         powers_lists_dict[score] = powers 

    #     temp = []
    #     score_list = list(powers_lists_dict.keys())
    #     score_list.sort()
    #     for key in score_list:
    #         temp.append(powers_lists_dict[key])
    #     self.powers_lists = temp