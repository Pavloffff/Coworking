import docker
import json

from dataclasses import dataclass
from hashlib import md5
from io import BytesIO
from pathlib import Path


@dataclass
class Image:
    name: str
    tag: str
    dockerfile: str
    root: Path
    args: dict[str]
    depends: list[str]

class ImagesRepository:
    def __init__(self, config_path: Path):
        with open(config_path) as config_file:
            config: dict = json.loads(config_file.read())
        images_data = config.get('images')
        self._images: dict[str, Image] = {}
        for image_name in images_data:
            image_data = images_data[image_name]
            self._images[image_name] = self._dict_to_image(image_data)
        self._root, self._tree = self._build_tree()
        self._docker = docker.from_env()

    def build_images(self):
        self._build_images(self._root)
    
    def _build_images(self, root: str):
        self._build_image(self._images[root])
        for dep in self._tree[root]:
            self._build_images(dep)
    
    def _build_image(self, image: Image):
        args = self._get_image_args(image)
        tag = f'{image.name}:{image.tag}'
        print(f'\nStart building image {tag}')
        image, build_logs = self._docker.images.build(
            path=str(image.root.absolute()),
            dockerfile=str((image.root / image.dockerfile).absolute()),
            tag=tag,
            buildargs=args
        )
        for chunk in build_logs:
            if 'stream' in chunk:
                for line in chunk['stream'].splitlines():
                    print(line)
        
    def _get_image_args(self, image: Image) -> dict[str, str]:
        for dep in image.depends:
            name_key = f'{str.upper(dep)}_NAME'
            name_val = self._images[dep].name
            tag_key = f'{str.upper(dep)}_TAG'
            tag_val = self._images[dep].tag
            image.args[name_key] = name_val
            image.args[tag_key] = tag_val
        return image.args
    
    def _build_tree(self) -> tuple[str, list[list[Image]]]:
        res = {name: [] for name in self._images.keys()}
        for name, image in self._images.items():
            if len(image.depends) == 0:
                root = name
            else:
                for dep in image.depends:
                    res[dep].append(name) 
        return root, res
    
    @classmethod
    def _dict_to_image(cls, image_data: dict):
        root_path = Path('build') / image_data.get('root')
        return Image(
            name=image_data.get('name'),
            tag=image_data.get('tag'),
            args=image_data.get('args', {}),
            depends=image_data.get('depends', []),
            dockerfile=image_data.get('dockerfile'),
            root=root_path
        )
    
if __name__ == '__main__':
    config_path = Path('build/config.json')
    repository = ImagesRepository(config_path)
    repository.build_images()
    

# docker build ./build/python/ \
#     --build-arg UBUNTU_NAME="coworking-ubuntu" \
#     --build-arg UBUNTU_TAG="1.0.0" \
#     --file ./build/python/Dockerfile.ubuntu
