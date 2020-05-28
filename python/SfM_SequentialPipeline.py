# coding: Shift_JIS
#work directory
#Test_NAME = "360_net_44_AKAZE_FLOAT_v_1"
Test_NAME = "test"
#movie_name = "CIMG3448.MOV"
# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "D:/OpenMVG/build64/Windows-AMD64-/Release"
OPENMVG_MVS_BIN = "D:/OpenMVG/build64/Windows-AMD64-/Release"
OPENMVG_MVS2_BIN = "D:/OpenMVS"
# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = "D:/OpenMVG/GIT/sfmmesh/openMVG/src/openMVG/exif/sensor_width_database"

#import commands
import os
import subprocess
import time
import sys
import my_func
   
start = time.time()  

#movie_folder
input_movie_dir = os.path.join('D:\OpenMVG\ProjectTest', Test_NAME, 'movie')
#image_folder
input_dir = os.path.join('D:\OpenMVG\ProjectTest', Test_NAME, 'images')
#Excecute filter
#my_func.edit_image(input_dir, input_dir) 
#transrate movie to images
#my_func.save_frame_range(os.path.join(input_movie_dir,movie_name), 10, input_dir, 'sample_video_img')
#output_folder
output_dir = os.path.join('D:\OpenMVG\ProjectTest', Test_NAME)
matches_dir = os.path.join(output_dir, "matches")
reconstruction_dir = os.path.join(output_dir, "outReconstruction")
Keypoints_dir = os.path.join(output_dir, "outKeyPoints")
Matching_dir = os.path.join(output_dir, "outMatches")
Tracking_dir = os.path.join(output_dir, "outTracks")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

# Create the ouput/matches folder if not present
if not os.path.exists(output_dir):
  os.mkdir(output_dir)
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)
  
print ("1. Intrinsics analysis")
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "4"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pIntrisics.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "AKAZE_FLOAT", "-n", "4"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pFeatures.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pFeatures.wait()

print ("3. Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-v", "1"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pMatches.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pMatches.wait()

# Create the reconstruction if not present
if not os.path.exists(reconstruction_dir):
    os.mkdir(reconstruction_dir)


print ("4. Do Sequential/Incremental reconstruction")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir, "-c", "4"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()

'''
print ("4. Do Sequential/Global reconstruction")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-M", matches_dir+"/matches.f.bin", "-o", reconstruction_dir], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()
'''

print ("5. Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()

# optional, compute final valid structure from the known camera poses
print ("6. Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-f", os.path.join(matches_dir, "matches.f.bin"), "-o", os.path.join(reconstruction_dir,"robust.bin")], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/robust.bin", "-o", os.path.join(reconstruction_dir,"robust_colorized.ply")], stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()

# Export Keypoints
print("7.Export Keypoints")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_exportKeypoints"),  "-i", reconstruction_dir+"/sfm_data.bin", "-d", matches_dir, "-o", Keypoints_dir], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()

print("8.Export Matches")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_exportMatches"),  "-i", reconstruction_dir+"/sfm_data.bin", "-d", matches_dir, "-m", matches_dir+"/matches.f.bin", "-o", Matching_dir], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pRecons.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pRecons.wait()

print("9.Unnecessary Point Remove")
my_func.RemoveBackPoint(reconstruction_dir+"\colorized.ply", reconstruction_dir+"\colorized_sub.ply", reconstruction_dir+"\colorized2.ply")
print("Complete remove Point" + "\n")

end_time = time.time() - start
print ("MVG_end_time:{0}".format(end_time) + "[sec]" + "\n")

# Dense or Sparse
print("Dense_Struct:y, Sparse_Struct:n")
key = input('>>' )
if(key == "n"):
    sys.exit()

# Use function of OpenMVS
print ("10. Executing OpenMVS")
pConvert = subprocess.Popen( [os.path.join(OPENMVG_MVS_BIN, "openMVG_main_openMVG2openMVS"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"scene.mvs")], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pConvert.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pConvert.wait()

print ("11. Executing DensifyPointCloud")
pDensify = subprocess.Popen( [os.path.join(OPENMVG_MVS2_BIN, "DensifyPointCloud"),  os.path.join(reconstruction_dir,"scene.mvs")], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
for line in iter(pDensify.stdout.readline,b''):
    print(line.rstrip().decode("utf8"))
pDensify.wait()

end_time = time.time() - start
print ("MVS_end_time:{0}".format(end_time) + "[sec]")