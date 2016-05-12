import numpy
import codecs

class compSent:
    "Class for computing sentiment score based on tweet"

    #Initialization reads sentiment directory
    def __init__(self):

        # define sent dictionary
        self.sent_dict = {}

        # import the sent set
        f = codecs.open('./datasources/sent_dict.csv','r','utf8')
        f.readline()
        for line in f:
            #Import sentiment word directory
            l = line.rstrip().split(',')
            i,word,v_mean_sum,v_sd_sum,v_rat_sum,a_mean_sum,a_sd_sum,a_rat_sum,d_mean_sum,d_sd_sum,d_rat_sum,v_mean_m,v_sd_m,v_rat_m,v_mean_f,v_sd_f,v_rat_f,a_mean_m,a_sd_m,a_rat_m,a_mean_f,a_sd_f,a_rat_f,d_mean_m,d_sd_m,d_rat_m,d_mean_f,d_sd_f,d_rat_f,v_mean_y,v_sd_y,v_rat_y,v_mean_o,v_sd_o,v_rat_o,a_mean_y,a_sd_y,a_rat_y,a_mean_o,a_sd_o,a_rat_o,d_mean_y,d_sd_y,d_rat_y,d_mean_o,d_sd_o,d_rat_o,v_mean_l,v_sd_l,v_rat_l,v_mean_h,v_sd_h,v_rat_h,a_mean_l,a_sd_l,a_rat_l,a_mean_h,a_sd_h,a_rat_h,d_mean_l,d_sd_l,d_rat_l,d_mean_h,d_sd_h,d_rat_h = l
            self.sent_dict[word] = (int(i),float(v_mean_sum),float(v_sd_sum))

    def compSentiment(self, intweet):
        sentlist=[]
        for i in xrange(1,len(intweet)):
            word=str(intweet[i]).lower()
            if word in self.sent_dict:
                sent=self.sent_dict[word]
                sentlist.insert(i,sent[1])

        return numpy.mean(sentlist)
