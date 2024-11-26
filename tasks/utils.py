import numpy as np
import laspy as lp
import open3d as o3d
import tkinter as tk
from tkinter import messagebox

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

