import numpy as np
import laspy as lp
import open3d as o3d
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def show_shortcuts():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    messagebox.showinfo("Atalhos de Interação", 
                        "Atalhos para Interação com o Open3D:\n\n"
                        "1. Botão esquerdo do mouse: Rotação\n"
                        "2. Botão direito do mouse: Zoom\n"
                        "3. Shift + Botão esquerdo: Translação\n"
                        "4. R: Redefinir visualização\n"
                        "5. Ctrl + C: Copiar visualização para a área de transferência\n"
                        "6. Q ou ESC: Fechar a janela")
    root.destroy()

def process_and_visualize_las(file_path):
    
    # Mostrar atalhos antes da visualização
    show_shortcuts()

    # Ler o arquivo LAS
    point_cloud = lp.read(file_path)

    # Dimensões e máximo do canal vermelho
    print([dimension.name for dimension in point_cloud.point_format.dimensions])
    print(np.max(point_cloud.red))

    # Pontos e cores
    points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
    colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()
    colors = colors / 65535

    print(f"Shape of points: {points.shape}") 
    print(f"Shape of colors: {colors.shape}")

    # Amostragem aleatória de pontos
    sampled_indices = np.random.choice(points.shape[0], size=int(0.05 * points.shape[0]), replace=False)
    sampled_points = points[sampled_indices, :]
    sampled_colors = colors[sampled_indices, :]

    # Criar nuvem de pontos
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(sampled_points)
    pcd.colors = o3d.utility.Vector3dVector(sampled_colors)

    # Visualizar
    o3d.visualization.draw_geometries_with_editing([pcd])


def process_and_visualize_ply(file_path): 
    pcd = o3d.io.read_point_cloud(file_path)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=16), fast_normal_computation=True)
    pcd.paint_uniform_color([0.6, 0.6, 0.6])
    o3d.visualization.draw_geometries([pcd]) 


def process_and_visualize_automatize_segmentation_RANSAC_ply(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    segment_models={}
    segments={}
    max_plane_idx=10
    rest=pcd
    for i in range(max_plane_idx):
        colors = plt.get_cmap("tab20")(i)
        segment_models[i], inliers = rest.segment_plane(distance_threshold=0.01,ransac_n=3,num_iterations=1000)
        segments[i]=rest.select_by_index(inliers)
        segments[i].paint_uniform_color(list(colors[:3]))
        rest = rest.select_by_index(inliers, invert=True)
        print("pass",i,"/",max_plane_idx,"done.")

    o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])


def process_and_visualize_automatize_segmentation_DBSCAN_Euclidean_Grouping_ply(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    segment_models={}
    segments={}
    max_plane_idx=20
    rest=pcd
    d_threshold=0.01
    for i in range(max_plane_idx):
        colors = plt.get_cmap("tab20")(i)
        segment_models[i], inliers = rest.segment_plane(distance_threshold=0.01,ransac_n=3,num_iterations=1000)
        segments[i]=rest.select_by_index(inliers)
        labels = np.array(segments[i].cluster_dbscan(eps=d_threshold*10, min_points=10))
        candidates=[len(np.where(labels==j)[0]) for j in np.unique(labels)]
        best_candidate=int(np.unique(labels)[np.where(candidates==np.max(candidates))[0]])
        print("the best candidate is: ", best_candidate)
        rest = rest.select_by_index(inliers, invert=True)+segments[i].select_by_index(list(np.where(labels!=best_candidate)[0]))
        segments[i]=segments[i].select_by_index(list(np.where(labels==best_candidate)[0]))
        segments[i].paint_uniform_color(list(colors[:3]))
        print("pass",i+1,"/",max_plane_idx,"done.")
    
    labels = np.array(rest.cluster_dbscan(eps=0.05, min_points=5))
    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")

    colors = plt.get_cmap("tab10")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    rest.colors = o3d.utility.Vector3dVector(colors[:, :3])
    o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest],zoom=0.3199,front=[0.30159062875123849, 0.94077325609922868, 0.15488309545553303],lookat=[-3.9559999108314514, -0.055000066757202148, -0.27599999308586121],up=[-0.044411423633999815, -0.138726419067636, 0.98753122516983349])