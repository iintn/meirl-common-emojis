# meirl-common-emojis

This shows the most common emojis and middle characters in the subreddits r/meirl and r/me_irl over time.

With this collection of scripts, they need to be run in a specific order to get the desired result.
That order is as follows:
1. get_title.py
2. comb_data.py
3. sort_into_months.py
4. count_frequency.py
5. combine_me_irl.py

(6-8 may be run before 1-4)

6. get_emoji_html.py
7. emoji_png_from_html.py
8. get_emoji_paths.py

Then finally.

9. graphing.py

Rename data files as needed inbetween each step, several steps may need to be repeated for different data files.

Emojis are obtained from http://www.unicode.org/emoji/charts/full-emoji-list.html

Final Note: Don't work with emojis and pictures, kids. It's not worth it.
