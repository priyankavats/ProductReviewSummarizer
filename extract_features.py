import operator
import csv



def main(complete_list):

	noun_map = {}
	general_words_set = set()
	with open('generalwords.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[2] == "n":
				general_words_set.add(row[1].lower())

	for row in complete_list:
		for sentence in row['list']:
			for tag in sentence["pos"]:	
				if tag["tag"]=="NN"and tag["word"] not in general_words_set:
					noun_map[tag["word"].lower()] = noun_map.get(tag["word"].lower(), 0) + 1
	
	sorted_noun_map = sorted(noun_map.items(), key=operator.itemgetter(1), reverse=True)

	feature_set = set()
	for feature in sorted_noun_map:
		if feature[1] < 3 :
			break
		feature_set.add(feature[0])
	
	feature_set.add("size")
	feature_set.add("display")
	feature_set.add("resolution")
	feature_set.add("contrast")
	feature_set.add("colors")
	feature_set.add("brightness")
	feature_set.add("graphics")
	feature_set.add("price")
	feature_set.add("speakers")
	feature_set.add("setup")
	feature_set.add("base")
	feature_set.add("stand")
	feature_set.add("panel")
	feature_set.add("fonts")
	feature_set.add("screen")
	feature_set.add("tilt")
	feature_set.add("vga")
	feature_set.add("control")
	feature_set.add("picture")
	feature_set.add("controls")
	feature_set.add("design")
	feature_set.add("image")
	feature_set.add("settings")
	feature_set.add("calibration")
	feature_set.add("color")
	feature_set.add("angle")
	feature_set.add("audio")
	feature_set.add("font")
	feature_set.add("angles")
	

	return feature_set

