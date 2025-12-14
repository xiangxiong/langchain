#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def replace_imports(directory):
    pattern = re.compile(r'from langchain_core\.pydantic_v1 import')
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                except UnicodeDecodeError:
                    # 尝试其他编码
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                
                if pattern.search(content):
                    new_content = pattern.sub('from pydantic import', content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Replaced in {file_path}')

if __name__ == '__main__':
    target_dir = '/Users/apple/Desktop/python/llm-ops/langchain/imooc-llmops-api-master'
    replace_imports(target_dir)
