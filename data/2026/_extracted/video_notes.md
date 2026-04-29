# Video Extraction Notes

- Source directory: `data/2026/video_pass`
- Non-manifest submissions processed: 25
- YouTube embed links are normalized as `https://www.youtube.com/embed/{video_id}` when a video id was found.
- Local `.mov`, `.mp4`, and `.m4v` submissions are recorded as local video uploads without YouTube links.

## Anomalies and Ambiguous Cases

- `365248 Wanying Li`: `data/2026/video_pass/2945699195 - Wanying Li - 365248_Wanying_Li_Video_Essay-Food_System_3036604565_4021069_132973041.txt` - Multiple raw YouTube links found for same video id.
- `372150 Wing Lam Ng`: `data/2026/video_pass/2946019618 - Wing Lam Ng - 372150_Wing_Lam_Ng_CCGL9065_Final_Portfolio_Links_4021069_221958337.docx` - Multiple raw YouTube links found for same video id.
- `357039 Jason Yeung`: `data/2026/video_pass/2946487823 - Jason Yeung - 357039_Jason_Yeung_Youtube_Video_4021069_1009299806.pdf` - Multiple raw YouTube links found for same video id.
- `363110 Tsz Ho Ngai`: `data/2026/video_pass/2946544525 - Tsz Ho Ngai - 363110_Tsz_Ho_Ngai_httpswww.youtube.comwatchv_5LrKTpaGd-0_4021069_246078225.mp4` - Local video upload; filename contains apparent YouTube id 5LrKTpaGd-0, but no YouTube link was recorded per local-upload rule.
- `351352 Shijun Feng`: `data/2026/video_pass/2946669564 - Shijun Feng - 351352_Shijun_Feng_Shijun_Feng_Video_4021069_550210205.mov` - Local video upload; no YouTube link.
- `355649 Tsz Chun Yim`: `data/2026/video_pass/2946759838 - Tsz Chun Yim - 355649_Tsz_Chun_Yim_CCGL9065_Video_Essay_4021069_260736902.docx` - Multiple raw YouTube links found for same video id.
- `376517 Alexandre Olivier Oriol Gergele`: `data/2026/video_pass/2946869632 - Alexandre Olivier Oriol Gergele - 376517_Alexandre_Olivier_Oriol_Gergele_Final_Climate_Change_Video_4021069_104166980.m4v` - Local video upload; no YouTube link.
- `356855 Jihoo Kim`: `data/2026/video_pass/2946920428 - Jihoo Kim - 356855_Jihoo_Kim_CCGL9065_Video_Essay_4021069_870237045.txt` - Multiple raw YouTube links found for same video id.
