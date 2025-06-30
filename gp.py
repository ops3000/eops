import os

def get_all_files(root_dir, extensions, blacklist_dirs=None):
    """
    获取指定目录及子目录中所有指定后缀的文件,并排除黑名单中的文件夹.
    """
    if blacklist_dirs is None:
        blacklist_dirs = []
    
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # --- MODIFICATION START ---
        # 从遍历列表中移除黑名单文件夹, 'dirnames[:]' 用于原地修改列表
        dirnames[:] = [d for d in dirnames if d not in blacklist_dirs]
        # --- MODIFICATION END ---
        
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in extensions:
                file_paths.append(os.path.join(dirpath, filename))
    return sorted(file_paths)

def generate_file_tree(root_dir, file_paths):
    """生成文件树结构"""
    processed_dirs = set()
    output = []
    # 处理根目录可能没有斜杠的情况
    root_name = os.path.basename(root_dir.rstrip(os.sep))
    output.append(f"{root_name}/")
    processed_dirs.add(os.path.normpath(root_dir)) # 将根目录的规范化路径添加到已处理集合

    for path in file_paths:
        rel_path = os.path.relpath(path, root_dir)
        parts = rel_path.split(os.sep)
        
        # 逐级创建目录结构
        for i in range(len(parts) - 1):
            # 构造当前要检查的目录的相对路径
            current_rel_dir = os.path.join(*parts[:i+1])
            # 构造绝对路径以进行检查
            current_abs_dir = os.path.join(root_dir, current_rel_dir)
            
            if os.path.normpath(current_abs_dir) not in processed_dirs:
                indent = "    " * (i + 1)
                output.append(f"{indent}{parts[i]}/")
                processed_dirs.add(os.path.normpath(current_abs_dir))

        # 添加文件名
        indent_level = len(parts) -1
        indent = "    " * indent_level if indent_level > 0 else "    "
        # 修正：当文件在根目录下时，也需要缩进
        if os.path.dirname(rel_path) == '':
             indent = "    "
        output.append(f"{indent}{parts[-1]}")
    
    return "\n".join(output)

def format_content(file_path, root_dir):
    """格式化文件内容"""
    rel_path = os.path.relpath(file_path, root_dir)
    extension = os.path.splitext(file_path)[1][1:]  # 去掉点号
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"{rel_path}\n```{extension}\n{content}\n```\n\n"
    except Exception as e:
        return f"//{rel_path}\nError reading file: {str(e)}\n\n"

def main():
    # 配置参数
    target_dir = "./eops"  # 替换为你的目录
    output_file = "output.txt"
    allowed_ext = [".jsx", ".py", ".js", ".html", ".css",".sql",".md"]

    # --- NEW: 黑名单文件夹列表 ---
    # 在此列表中添加不希望扫描的文件夹名称
    blacklist_folders = ["node_modules", ".git", "__pycache__", "dist", "build", "opsbot"] 

    # 获取文件列表 (传入黑名单)
    files = get_all_files(target_dir, [ext.lower() for ext in allowed_ext], blacklist_folders)
    
    # 生成文件树
    file_tree = generate_file_tree(target_dir, files)
    
    # 生成文件内容
    contents = [format_content(f, target_dir) for f in files]
    
    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=== 文件树结构 ===\n")
        f.write(file_tree + "\n\n")
        f.write("=== 文件内容 ===\n\n")
        f.writelines(contents)

    print(f"处理完成，结果已写入 {output_file}")

if __name__ == "__main__":
    main()