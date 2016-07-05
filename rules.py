import not_words

def check_negation(sentence,feature,phrase,opinion):
    for dependency in sentence['dependencies']:
        if "gov" in dependency and opinion is not None and dependency['reln'] == "neg" and dependency['gov']==feature:
            phrase = "not " + phrase
            opinion = "not " + opinion
            print "----------------------NEGATION bit", phrase
        if "gov" in dependency and opinion is not None and dependency['reln']=="neg" and dependency['gov']==opinion:
            phrase = "not " + phrase
            opinion = "not " + opinion
            print "----------------------NEGATION bit", phrase
    if "not" in phrase:
        phrase = not_words.main(phrase,feature)   
    return opinion, phrase



def main(complete_list, feature_set):

    review_phrase_dict_list=[]

    for row in complete_list:
        review = row['review']
        review_phrase_dict = {'review': review, 'id': row['id'], 'phrases': []}
        
        for sentence in row['list']:
            for feature in feature_set:
                if feature in sentence['sentence']:
                    for dep in sentence['dependencies']:
                        opinion = None
                        opinion_non_negative = None
                        
                        # CASE 1 : If the Feature acts as a governor
                        if "gov" in dep and dep['gov'] == feature:
                            
                            # If reln ==  amod
                            if dep['reln']=="amod":
                                print "CASE 1, reln = amod"
                                opinion = dep['dep']
                                phrase = opinion + " " + feature
                                opinion_non_negative = dep['dep']
                                opinion,phrase = check_negation(sentence,feature,phrase,opinion)

                                # If reln == amod and conj:and
                                for dep_amod in sentence['dependencies']:
                                    if "gov" in dep_amod and opinion is not None and dep_amod['reln'] == "conj:and" and dep_amod['gov'] == opinion_non_negative:
                                        opinion1 = dep_amod['dep']
                                        phrase1 = opinion1 + " " + feature
                                        opinion1,phrase1 = check_negation(sentence,feature,phrase1,opinion1)
                                        print phrase1
                                        review_phrase_dict['phrases'].append(phrase1)
                                    if "gov" in dep_amod and opinion is not None and dep_amod['reln'] == "dobj" and dep_amod['dep'] == feature:
                                        opinion = dep_amod['gov'] + " " + opinion_non_negative
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,dep_amod['gov'],phrase,opinion )
                                    if "gov" in dep_amod and opinion is not None and dep_amod['reln'] == "nsubj" and dep_amod['dep'] == feature:
                                        opinion = dep_amod['gov'] + " " + opinion_non_negative
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,dep_amod['gov'],phrase,opinion )


                                print phrase
                                review_phrase_dict['phrases'].append(phrase)           
                                
                        # CASE 2 : If the Feature acts as Dependant
                        elif "dep" in dep and dep['dep'] == feature:
                            
                            if dep['reln']=="nsubj":
                                print "CASE 2, reln == nsubj"
                                opinion = dep['gov']
                                phrase = opinion + " " + feature
                                temp_gov = dep['gov']
                                opinion,phrase = check_negation(sentence,feature,phrase,opinion)

                                # If reln == nsubj and xcomp
                                for dep_nsubj_xcomp in sentence['dependencies']:
                                    if "gov" in dep_nsubj_xcomp and opinion is not None and dep_nsubj_xcomp['reln'] == "xcomp" and dep_nsubj_xcomp['gov'] == temp_gov:
                                        print"CASE 2, reln == nsubj and xcomp"
                                        opinion = dep_nsubj_xcomp['dep']
                                        opinion_non_negative = dep_nsubj_xcomp['dep']
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,temp_gov,phrase,opinion)

                                        # If reln == nsubj, xcomp and conj:and
                                        for dep_nsubj_xcomp_conj in sentence['dependencies']:
                                            if "gov" in dep_nsubj_xcomp_conj and opinion is not None and dep_nsubj_xcomp_conj['reln']=="conj:and" and dep_nsubj_xcomp_conj['gov']==opinion_non_negative:
                                                print"CASE 2, reln == nsubj and conj:and"
                                                opinion1 = dep_nsubj_xcomp_conj['dep']
                                                phrase1= opinion1 + " " + feature
                                                opinion1,phrase1 = check_negation(sentence,temp_gov,phrase1,opinion1)
                                                print phrase1
                                                review_phrase_dict['phrases'].append(phrase1) 
                               
                                # If reln == nsubj and nmod : on ################ NOT CHECKED
                                for dep_nsubj_nmod in sentence['dependencies']:
                                    if "gov" in dep_nsubj_nmod and opinion is not None and dep_nsubj_nmod['reln'] == "nmod:on" and dep_nsubj_nmod['gov'] == temp_gov:
                                        print"CASE 2, reln == nsubj and nmod:on"
                                        opinion = temp_gov + " " + dep_nsubj_nmod['dep']
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,temp_gov,phrase,opinion)
                                
                                # If reln == nsubj and conj:and
                                for dep_nsubj_conj in sentence['dependencies']:
                                    if "gov" in dep_nsubj_conj and opinion is not None and dep_nsubj_conj['reln'] == "conj:and" and dep_nsubj_conj['gov'] == temp_gov:
                                        print "CASE 2, reln == nsubj and conj:and"
                                        opinion1 = dep_nsubj_conj['dep']
                                        phrase1 = opinion1 + " " + feature
                                        opinion,phrase = check_negation(sentence,feature,phrase,opinion)
                                        print phrase1
                                        review_phrase_dict['phrases'].append(phrase1) 

                                print phrase        
                                review_phrase_dict['phrases'].append(phrase)       

                            # If reln == nmod:for
                            if dep['reln'] =="nmod:for":
                                print "CASE 2, reln == nmod:for"
                                opinion = dep['gov']
                                phrase = opinion + " " + feature
                                temp_gov = dep['gov']

                                # If reln == nmod:for and amod
                                for dep_nmod in sentence['dependencies']:
                                    if "gov" in dep_nmod and opinion is not None and dep_nmod['reln'] == "amod" and dep_nmod['gov'] == temp_gov:
                                        print "CASE 2, reln == nmod:for and amod"
                                        opinion = dep_nmod['dep']
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,temp_gov,phrase,opinion)

                                opinion,phrase=check_negation(sentence,feature,phrase,opinion)
                                print phrase
                                review_phrase_dict['phrases'].append(phrase)    

                            # If reln == nsubjpass
                            if dep['reln'] == "nsubjpass" :
                                print "CASE 2, reln == nsubjpass"
                                temp_gov = dep['gov']
                                for dep_nsubjpass in sentence['dependencies']:
                                    if "gov" in dep_nsubjpass and dep_nsubjpass['reln'] == "advmod" and dep_nsubjpass['gov'] == temp_gov:
                                        opinion = dep_nsubjpass['dep'] + " " + temp_gov
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,temp_gov,phrase,opinion)
                                    if "gov" in dep_nsubjpass and dep_nsubjpass['reln'] == "compound:prt" and dep_nsubjpass['gov'] == temp_gov:
                                        opinion = temp_gov +" " +dep_nsubjpass['dep']
                                        phrase = opinion + " " + feature
                                        opinion,phrase = check_negation(sentence,temp_gov,phrase,opinion)
                                # print phrase
                                review_phrase_dict['phrases'].append(phrase)
                            
                            # If reln == compound and feature is VGI or HDMI
                            if dep['reln'] == "compound" :
                                print "here"
                                phrase = None
                                x = dep['dep']
                                if x == "vga" or "hdmi":
                                    print "CASE 2, reln == compound (with VGA or HDMI) "
                                    temp_gov = dep['gov']
                                    for dep_compound in sentence['dependencies']:
                                        if "gov" in dep_compound and dep_compound['reln'] == "acl:relcl" and dep_compound['gov'] == temp_gov:
                                            opinion = dep_compound['dep'] 
                                            phrase = opinion + " " + feature + " " + temp_gov
                                            opinion,phrase = check_negation(sentence,feature,phrase,opinion)
                                        if "gov" in dep_compound and dep_compound['reln'] == "nsubj" and dep_compound['dep'] == temp_gov:
                                            opinion = dep_compound['gov']
                                            phrase = opinion + " " + feature + " " + temp_gov
                                            opinion,phrase = check_negation(sentence,feature,phrase,opinion)

                                print phrase
                                if phrase is not None:
                                    review_phrase_dict['phrases'].append(phrase)
        review_phrase_dict_list.append(review_phrase_dict)

    # print(review_phrase_dict_list)
    return review_phrase_dict_list

if __name__ == "__main__":
    print main(complete_list, feature_set)
