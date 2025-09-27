from lxml import etree
import os
import glob
import re


def sanitize_member(name):
    # 保证为有效的 Python 标识符
    n = re.sub(r'[^0-9a-zA-Z_]', '_', name)
    if re.match(r'^[0-9]', n):
        n = '_' + n
    return n


def find_svg_files(inputs):
    files = []
    for p in inputs:
        p = p.strip()
        if not p:
            continue
        # 通配符
        if any(ch in p for ch in ['*', '?']):
            files.extend(glob.glob(p, recursive=True))
            continue
        # 文件夹（递归查找所有子目录中的 svg）
        if os.path.isdir(p):
            for root, _, filenames in os.walk(p):
                for fn in filenames:
                    if fn.lower().endswith('.svg'):
                        files.append(os.path.join(root, fn))
            continue
        # 单个文件
        if os.path.isfile(p):
            files.append(p)
            continue
        # 相对路径尝试（也支持像 some/dir/**/*.svg 之类的模式）
        files.extend(glob.glob(p, recursive=True))
    # 去重并保证存在
    files = [os.path.abspath(f) for f in dict.fromkeys(files) if os.path.isfile(f) and f.lower().endswith('.svg')]
    return files


svg_input = input("请输入图标路径、文件夹或多个路径（用逗号分隔，支持通配符）：").strip('"')
if not svg_input:
    print("未输入路径，退出。")
    exit(1)

parts = [p.strip() for p in svg_input.split(',') if p.strip()]
svg_files = find_svg_files(parts)
if not svg_files:
    print("未找到任何 svg 文件。")
    exit(1)

icons_dir = os.path.join('.', 'zbWidgetLib', 'icons')
os.makedirs(icons_dir, exist_ok=True)

# 将要新增到 enum 的条目集合
new_members = []

for svg_file in svg_files:
    print(f"处理: {svg_file}")
    base_full = os.path.splitext(os.path.basename(svg_file))[0]
    # 支持移除末尾的数字+Regular（例如 24Regular、16Regular 等，不区分大小写）
    def remove_size_suffix(name):
        # 移除结尾的尺寸+Regular
        n = re.sub(r'\d+Regular$', '', name, flags=re.I)
        return n

    member_raw = remove_size_suffix(base_full)
    if not member_raw:
        member_raw = base_full
    member_name = sanitize_member(member_raw)
    # 枚举值也去掉尺寸后缀以保持一致性
    value_name = member_raw

    # 读取并统一改色两次
    with open(svg_file, "rb") as f:
        svg_data = f.read()
        parser = etree.XMLParser(remove_blank_text=True)
        svg_tree = etree.fromstring(svg_data, parser)

    # 白色版本
    for element in svg_tree.iter():
        if 'fill' in element.attrib:
            element.attrib['fill'] = '#FFFFFF'
    white_path = os.path.join(icons_dir, f"{member_raw}_white.svg")
    with open(white_path, 'wb') as f:
        f.write(etree.tostring(svg_tree, pretty_print=True))

    # 黑色版本：需要重新解析原始数据以避免累计修改
    with open(svg_file, "rb") as f:
        svg_data = f.read()
        svg_tree = etree.fromstring(svg_data, parser)
    for element in svg_tree.iter():
        if 'fill' in element.attrib:
            element.attrib['fill'] = '#000000'
    black_path = os.path.join(icons_dir, f"{member_raw}_black.svg")
    with open(black_path, 'wb') as f:
        f.write(etree.tostring(svg_tree, pretty_print=True))

    print(f"已生成: {white_path} , {black_path}")
    new_members.append((member_name, value_name))

# 去重 new_members，保留第一次出现的成员（按成员名和值去重）
uniq_members = []
seen_names = set()
seen_values = set()
for m, v in new_members:
    if m in seen_names or v in seen_values:
        continue
    uniq_members.append((m, v))
    seen_names.add(m)
    seen_values.add(v)
new_members = uniq_members

# 更新 zbWidgetLib/icon.py 中的 ZBF 枚举
icon_py_path = os.path.join('.', 'zbWidgetLib', 'icon.py')
if os.path.isfile(icon_py_path):
    with open(icon_py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到 class ZBF 定义处
    class_def_match = re.search(r"^class\s+ZBF\s*\(.*\):", content, flags=re.M)
    if not class_def_match:
        print('未在 zbWidgetLib/icon.py 中找到 class ZBF，跳过枚举更新。')
    else:
        insert_pos = class_def_match.end()
        # 在 class 定义和后面的代码之间查找第一个 def path 的位置，用来插入成员
        path_def_match = re.search(r"\n\s+def\s+path\s*\(", content[insert_pos:], flags=re.M)
        if path_def_match:
            insert_index = insert_pos + path_def_match.start()
        else:
            # 没找到 def path，就插入在 class 定义后面
            insert_index = insert_pos

        # 先删除类中已有的值包含数字+Regular 的枚举成员（例如 24Regular、16Regular 等）
        class_body = content[insert_pos:insert_index]
        # 匹配形如: <whitespace>NAME = "...24Regular..." （大小写不敏感）
        to_remove_pattern = re.compile(r"^\s*[A-Za-z_][A-Za-z0-9_]*\s*=\s*\"[^\"]*\d+Regular[^\"]*\"\s*$", flags=re.M | re.I)
        new_class_body, removed_count = to_remove_pattern.subn('', class_body)
        if removed_count:
            # 清理多余空行
            new_class_body = re.sub(r"\n{2,}", "\n\n", new_class_body)
            content = content[:insert_pos] + new_class_body + content[insert_index:]
            # 重新计算 insert_index 因为内容长度可能改变
            if path_def_match:
                insert_index = insert_pos + new_class_body.__len__()

        # 生成要插入的成员文本（去重）
        to_insert_lines = []
        for mname, vname in new_members:
            # 检查是否已经存在相同成员名或相同值
            if re.search(rf"^\s*{re.escape(mname)}\s*=\s*\"{re.escape(vname)}\"", content, flags=re.M):
                print(f"枚举已存在，跳过: {mname} = \"{vname}\"")
                continue
            if re.search(rf"\"{re.escape(vname)}\"", content):
                # 值已存在（可能是另一个成员），跳过
                print(f"枚举值已存在，跳过: \"{vname}\"")
                continue
            to_insert_lines.append(f"    {mname} = \"{vname}\"\n")

        if to_insert_lines:
            # 保持原有换行风格，尽量在 insert_index 前后加换行
            new_content = content[:insert_index] + "\n" + ''.join(to_insert_lines) + content[insert_index:]
            with open(icon_py_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已在 {icon_py_path} 中添加 {len(to_insert_lines)} 个枚举成员。")
        else:
            print('没有需要添加的枚举成员。')
else:
    print(f"未找到文件: {icon_py_path}，请检查路径。")

print('完成。')
