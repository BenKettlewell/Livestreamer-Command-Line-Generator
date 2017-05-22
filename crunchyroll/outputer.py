def youtube_dl_string_for_CrunchyCSV(crunchyCSV):
	youtube_dl_list = []
	for anime in crunchyCSV.list:
		youtube_dl_list.append(anime.generate_youtube_dl())
	return ("; ".join(youtube_dl_list))

def youtube_dl_string_for_Anime(anime):
	return anime.generate_youtube_dl()