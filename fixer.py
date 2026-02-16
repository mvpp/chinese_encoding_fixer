import os
import unicodedata

def recover_mojibake(path='.'):
    for root, dirs, files in os.walk(path):
        for name in files:
            # 跳过隐藏文件和脚本本身
            if name.startswith('.') or name.endswith('.py'):
                continue
            
            try:
                # 第一步：治愈苹果的“拆字症”，把 O 和 ´ 重新组合成 Ó (NFC 标准化)
                nfc_name = unicodedata.normalize('NFC', name)
                
                # 第二步：将这些西欧字符还原为底层的原始字节
                # 使用 cp1252 编码库，并开启 replace 容错，忽略已经被破坏的字节
                raw_bytes = nfc_name.encode('cp1252', errors='replace')
                
                # 第三步：用中文 GBK 重新翻译这些字节
                new_name = raw_bytes.decode('gbk', errors='replace')
                
                # 如果名字有变化，就执行重命名
                if new_name != name and new_name != nfc_name:
                    old_path = os.path.join(root, name)
                    new_path = os.path.join(root, new_name)
                    print(f"✅ 成功抢救: {name}")
                    print(f"   👉 恢复为: {new_name}\n")
                    os.rename(old_path, new_path)
                    
            except Exception as e:
                # 遇到无法处理的文件默默跳过，绝不损坏原文件
                pass

if __name__ == "__main__":
    print("开始执行强力修复...\n")
    recover_mojibake('.')
    print("修复完毕！")
