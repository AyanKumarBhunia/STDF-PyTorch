import os
import glob
import os.path as op
import multiprocessing as mp
import subprocess

def _compress(cmd):
    os.system(cmd)

source_type = 'mkv' # .mkv vs .mp4'
if __name__ == "__main__":
    src_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/UGC/UGC_Orig/'
    target_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/UGC/UGC_Orig_YUV/'
    vid_lst = glob.glob(op.join(src_folder, f'*.{source_type}'))

    for one_vid_path in vid_lst:
        cmd = (f'ffprobe -count_frames -v error -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 {one_vid_path}')
        (nb_frames, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
        nb_frames = int(nb_frames)

        cmd = (f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {one_vid_path}')
        (resolution, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
        width, height = str(resolution).split('\'')[1].split('\\')[0].split('x')


        # target_path = os.path.join(target_folder, os.path.basename(one_vid_path).split('.')[0] + '_{640x360}_' + str(nb_frames))
        target_path = os.path.join(target_folder, os.path.basename(one_vid_path).split('.')[0] + '_' + str(width) + 'x' + str(height)  + '_' + str(nb_frames))
        cmd = (f'ffmpeg -i {one_vid_path} -pix_fmt yuv420p {target_path}.yuv')
        os.system(cmd)



# if __name__ == "__main__":
#     src_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/MP4_Orig/'
#     target_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/YUV/'
#     vid_lst = glob.glob(op.join(src_folder, '*.mp4'))
#     # pool = mp.Pool()
#     for one_vid_path in vid_lst:
#         # width, height = map(int, one_vid_path.split('.')[-2].split('_')[-2].split('x'))
#         # targ_path = os.path.join(target_folder, one_vid_path.split('/')[-1].split('.')[0] + '_source')
#         # FPS = 25.0
#
#         # one_vid_path = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/test/raw/blue_sky_1080p25.mp4'
#         cmd = (f'ffprobe -count_frames -v error -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 {one_vid_path}')
#         (nb_frames, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
#         nb_frames = int(nb_frames)
#
#         # # cmd = (f"ffmpeg -i {one_vid_path} 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}'")
#         # cmd = (f'ffmpeg -i {one_vid_path} 2>&1 | grep Video:')
#         # # cmd = (f'fprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {one_vid_path}')
#         # (resolution, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
#
#         target_path = os.path.join(target_folder, os.path.basename(one_vid_path).split('.')[0] + '_640x360_' + str(nb_frames))
#         cmd = (f'ffmpeg -i {one_vid_path} -pix_fmt yuv420p {target_path}.yuv')
#
#         # cmd = (f'ffmpeg -f rawvideo -vcodec rawvideo -s {width}x{height}'
#         #        f' -pix_fmt yuv420p -i {one_vid_path} -c:v libx264 -preset ultrafast -crf 0 {targ_path}.mp4'
#         #     )
#         os.system(cmd)
#         # pool.apply_async(
#         #     func=_compress,
#         #     args=(cmd,),
#         #     callback=None
#         #     )
#
#         # fmpeg - i
#         # crowdrun.mp4 - pix_fmt
#         # yuv444p
#         # crowdrun.yuv
# ffmpeg -i crowdrun.mp4 -vf scale=640:360 -sws_flags lanczos -c:v libx264 -preset ultrafast -crf 0 crowdrun_source_360p.mp4
# ffprobe -count_frames -v error -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 ${1}