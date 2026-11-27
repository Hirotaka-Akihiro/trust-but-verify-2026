"""Assemble the Phase 6 video: one clip per slide (slide image + that slide's narration), with the demo on slide 7.

Usage (from presentation/cn):  python make_video.py <slides_dir> <work_dir>
  slides_dir : slide01.png ... slide11.png exported at 1920x1080
  recordings/: s01-s06.m4a, s08-s11.m4a, demo.mp4 (demo already merged with its voice-over)
Each narration is cleaned: low rumble removed, clicks outside speech muted, edges trimmed, loudness set to -16 LUFS.
Needs ffmpeg (imageio-ffmpeg) and faster-whisper (word timestamps used to find the speech).
"""
import json, subprocess, sys
from pathlib import Path
import imageio_ffmpeg
from faster_whisper import WhisperModel

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = Path(__file__).resolve().parent
REC = HERE / "recordings"
SLIDES, WORK = Path(sys.argv[1]), Path(sys.argv[2])
WORK.mkdir(parents=True, exist_ok=True)
OUT = HERE / "23i-2538_23i-2542_23i-2536_Phase-6_Video.mp4"
LEAD, TAIL = 0.6, 0.8                    # silence before / after each speaker on a slide
DEMO_TITLE = 2.0                         # seconds of slide 7 shown over the start of the demo (no speech there)
DEMO_IN, DEMO_OUT = 1.5, 141.0           # trim the silent start and end of demo.mp4
model = WhisperModel("small.en", device="cpu", compute_type="int8")


def run(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def speech(path):
    segs, _ = model.transcribe(str(path), language="en", beam_size=5, word_timestamps=True, vad_filter=True)
    words = [(w.start, w.end) for s in segs for w in s.words]
    spans = []
    for a, b in words:
        a, b = max(0.0, a - 0.2), b + 0.3
        if spans and a <= spans[-1][1] + 0.4:
            spans[-1][1] = max(spans[-1][1], b)
        else:
            spans.append([a, b])
    return spans


clips, report = [], []
for n in range(1, 12):
    clip = WORK / f"clip{n:02d}.mp4"
    img = SLIDES / f"slide{n:02d}.png"
    if n == 7:
        # demo: show the slide-7 title card over the first seconds (silent there), then the screen recording
        run(["-i", str(REC / "demo.mp4"), "-loop", "1", "-t", str(DEMO_TITLE), "-i", str(img), "-filter_complex",
             f"[0:v]trim=start={DEMO_IN}:end={DEMO_OUT},setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=30[d];[1:v]scale=1920:1080,setsar=1,fps=30[t];"
             f"[d][t]overlay=enable='lt(t,{DEMO_TITLE})':eof_action=pass,format=yuv420p[v];"
             f"[0:a]atrim=start={DEMO_IN}:end={DEMO_OUT},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a]",
             "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-c:a", "aac", "-b:a", "192k", str(clip)])
    else:
        src = REC / f"s{n:02d}.m4a"
        sp = speech(src)
        start, end = sp[0][0], sp[-1][1]
        cond = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in sp)
        dur = (end - start) + LEAD + TAIL
        af = (f"volume='if({cond},1,0)':eval=frame,atrim=start={start:.2f}:end={end:.2f},asetpts=PTS-STARTPTS,"
              f"highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo,"
              f"adelay={int(LEAD * 1000)}:all=1,apad=whole_dur={dur:.2f}")
        run(["-loop", "1", "-t", f"{dur:.2f}", "-i", str(img), "-i", str(src), "-filter_complex",
             f"[0:v]scale=1920:1080,setsar=1,fps=30,format=yuv420p[v];[1:a]{af}[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-tune", "stillimage", "-crf", "18",
             "-preset", "medium", "-c:a", "aac", "-b:a", "192k", str(clip)])
        report.append((n, round(dur, 1)))
    clips.append(clip)
    print("built", clip.name, flush=True)

lst = WORK / "clips.txt"
lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(OUT)])
print("slide durations:", report)
print("written", OUT)
