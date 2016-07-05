import get_complete_list
import extract_features
import rules
import polarity


review_list = [
# 	# {
# 	# 	"text" : "Amazing monitor. Picked it over the Asus MX27 silver monitor just because this was a newer model, had similar specs, but also looked better in my eyes. Very sturdy stand (albeit plastic). The overall control is a big step above my 5yr old 1080p LG monitor. The brightness is really easy to adjust (as are all the screen controls despite being pointed down with no indicators on the front bezel). It's a very minimalist looking monitor with nothing on the bezel to distract or take away from the design. And it's advertised as bezel-less,there is still about a 3rd of an inch of all the corners of black glass. Sure I guess there's not silver bezel like on the bottom, but the picture isn't completely edge to edge. Honestly, for the price, I am 100% happy with the monitor. Looks great, performs wells, easy to control."
# 	# }
	# {
	# 	 "text" : "	I purchased this monitor to upgrade to a better monitor. I myself am a very serious pc gamer and follow the specificatipons seriously for the game so it may be played how it is meant to be played. I find that this monitor is perfect for the job. So I personally feel the colors are brilliant with Very slim and sleek design. The vga ports are stable. Also, the stand is not that good. The brightness maximum is painful. Overall, I would say a good piece."
	# },
	{
		"id" : 1,
		"text" : "this is a review of BENQ monitor. i recently purchased a monitor of size 24 inches from amazon. One thing good about this monitor is the price. For this amount, it is definately a good purchase.. the hdmi port works well . brightness control does not work properly. the monitor came with the panel which made the initial setup easy. colors are bright and sharp. I am happy with this monitor"
	}
]

def main(review_list):
	# Getting the complete list
	complete_list = get_complete_list.main(review_list)

	# Extracting features
	feature_set = extract_features.main(complete_list)

	# Getting list of each review and its corresponding phrases
	review_phrase_dict_list = rules.main(complete_list,feature_set)

	# Gettng polarity for each feature and its dedicated phrases
	feature_phrase_polarity, phrase_polarity, phrase_feature = polarity.main(review_phrase_dict_list,feature_set)

	# Getting final polarity of each feature
	final_polarity = polarity.final_polarity(feature_phrase_polarity)
	return final_polarity, review_phrase_dict_list, phrase_polarity, phrase_feature



if __name__ == "__main__":
	print main(review_list)
