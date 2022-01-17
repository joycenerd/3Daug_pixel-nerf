import open3d as o3d
import matplotlib.pyplot as plt
import argparse
import glob
import random


parser=argparse.ArgumentParser()
parser.add_argument('--obj-dir',type=str,required=True,help='object directory')
parser.add_argument('--nviews',type=int,default=10,help='use how many view to build point cloud')
args=parser.parse_args()

def convert(color_path,depth_path):
    color_raw = o3d.io.read_image(color_path)
    depth_raw = o3d.io.read_image(depth_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw)
    
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    return pcd


if __name__=='__main__':
    view_size=len(glob.glob(f'{args.obj_dir}/*.exr'))
    idx=random.sample(range(view_size),args.nviews)

    points=[]
    for i,obj in enumerate(glob.glob(f'{args.obj_dir}/*.exr')):
        if i in idx:
            color_path=obj.replace('_depth.exr','.png')
            depth_path=obj.replace('.exr','_norm.png')
            pcd=convert(color_path,depth_path)
            points.append(pcd)
    o3d.visualization.draw_geometries(points)
    


