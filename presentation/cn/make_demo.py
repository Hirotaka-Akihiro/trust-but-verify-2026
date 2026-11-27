"""Re-time the silent screen recording to the voice-over and merge them into recordings/demo.mp4.
Usage (from presentation/cn): python make_demo.py recordings   (speech spans: speech_spans.json)"""
import subprocess, sys
from pathlib import Path
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
REC = Path(sys.argv[1])
vid, aud, out = REC / "originals" / "LIve demo recording.mp4", REC / "originals" / "Live Demo Voice over.m4a", REC / "demo.mp4"
V_END, A_END = 139.47, 144.32
# screen appears in the video at V; speaker starts that section at A (from the transcript); show it 1 s before A
V = [0.0, 14.75, 32.0, 45.0, 57.5, 101.0, 125.0, V_END]
A = [1.0, 16.7, 35.7, 49.6, 63.3, 107.1, 129.0, A_END + 1.0]
T = [a - 1.0 for a in A]

parts = []
for k in range(len(V) - 1):
    L, D = V[k + 1] - V[k], T[k + 1] - T[k]
    take = min(L, D)
    pad = max(0.0, D - L)
    parts.append(f"[0:v]trim=start={V[k]}:duration={take:.3f},setpts=PTS-STARTPTS,"
                 f"tpad=stop_mode=clone:stop_duration={pad:.3f}[v{k}]")
    print(f"section {k}: video {V[k]:.2f}-{V[k]+take:.2f} ({take:.1f} s) + hold {pad:.1f} s -> {D:.1f} s")
n = len(V) - 1
fc = ";".join(parts) + ";" + "".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0,fps=30," \
     "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0C0C0C,format=yuv420p[v];" \
     "[1:a]volume='if(between(t,3.8,8.14)+between(t,8.82,34.78)+between(t,35.44,47.8)+between(t,49.37,60.61)+between(t,61.61,127.75)+between(t,128.51,139.89),1,0)':eval=frame,highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(vid), "-i", str(aud), "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(out)], check=True)
print("written", out)
