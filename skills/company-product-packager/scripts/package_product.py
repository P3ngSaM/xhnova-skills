"""Validate a product v1 JSON envelope and emit an importable Markdown file. Stdlib only."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit


FIELDS = {
    'name': ('产品名称', 2, 100),
    'summary': ('产品简介', 10, 1000),
    'audience': ('适用客户', 1, 1000),
    'capabilities': ('核心功能与应用场景', 1, 2000),
    'cases': ('已有案例', 0, 1000),
    'pricing': ('报价与收费方式', 0, 500),
    'constraints': ('实施条件与能力边界', 1, 1000),
    'promotion': ('介绍与推广建议', 1, 1500),
    'evidence': ('资料来源与待确认事项', 1, 2000),
    'website': ('产品网站 / 演示地址', 0, 2000),
}


def length(value):
    return len(value.encode('utf-16-le')) // 2


def package(data):
    if not isinstance(data, dict) or set(data) != {'format', 'version', 'product'}:
        raise ValueError('包必须包含且仅包含 format、version、product')
    if data['format'] != 'predictor-company-product' or type(data['version']) is not int or data['version'] != 1:
        raise ValueError('只支持 predictor-company-product v1')
    product = data['product']
    allowed = set(FIELDS) | {'tags', 'status', 'dataUsage'}
    if not isinstance(product, dict) or set(product) - allowed:
        raise ValueError('product 包含未知字段或不是对象')
    product = dict(product)
    for key, (_, minimum, maximum) in FIELDS.items():
        value = product.get(key, '')
        if not isinstance(value, str) or not minimum <= length(value.strip()) <= maximum:
            raise ValueError(f'{key} 需要 {minimum}–{maximum} 字的文本')
        if any(ord(c) < 32 and c not in '\n\r\t' or ord(c) == 127 for c in value):
            raise ValueError(f'{key} 含非文本控制字符')
        product[key] = value.strip()
    website = product['website']
    if website:
        url = urlsplit(website)
        if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password:
            raise ValueError('website 需要不含凭据的完整 HTTP(S) URL')
    tags = product.setdefault('tags', [])
    if not isinstance(tags, list) or len(tags) > 12 or any(
        not isinstance(tag, str) or not 1 <= length(tag.strip()) <= 40 for tag in tags
    ):
        raise ValueError('tags 最多 12 项，每项 1–40 字')
    product['tags'] = list(dict.fromkeys(tag.strip() for tag in tags))
    if product.setdefault('status', 'draft') not in ('draft', 'active'):
        raise ValueError('status 只能为 draft 或 active')
    if product.setdefault('dataUsage', 'business') not in ('business', 'controlled_test', 'demo', 'unclassified'):
        raise ValueError('dataUsage 无效')
    data = {'format': data['format'], 'version': 1, 'product': product}
    sections = [f'# {product["name"]}', '本文与末尾的标准数据块来自同一份产品资料。']
    for key, (label, _, _) in FIELDS.items():
        if key != 'name':
            sections.append(f'## {label}\n\n{product[key] or "待补充"}')
    sections += [f'产品状态：{product["status"]}；资料用途：{product["dataUsage"]}',
                 '## 导入数据\n\n```predictor-product\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n```']
    markdown = '\n\n'.join(sections) + '\n'
    if markdown.count('\n```predictor-product') != 1:
        raise ValueError('字段内不可嵌套 predictor-product 数据块')
    if len(markdown.encode('utf-8')) > 128 * 1024:
        raise ValueError('生成文件超过 128 KiB')
    return markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, default=Path('product-profile.md'))
    parser.add_argument('--force', action='store_true', help='Overwrite the specified output')
    args = parser.parse_args()
    try:
        if args.input.stat().st_size > 128 * 1024:
            raise ValueError('输入超过 128 KiB')
        markdown = package(json.loads(args.input.read_text(encoding='utf-8-sig')))
        with args.output.open('w' if args.force else 'x', encoding='utf-8', newline='\n') as output:
            output.write(markdown)
    except (ValueError, OSError) as error:
        parser.exit(1, f'产品打包失败：{error}\n')
    print(str(args.output))


if __name__ == '__main__':
    main()
