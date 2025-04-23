from .user import UserRepository
from .server import ServerRepository
from .role import RoleRepository
from .user_role import UserRoleRepository
from .text_channel import TextChannelRepository
from .voice_channel import VoiceChannelRepository
from .chat_item import ChatItemRepository
from .user_server import UserServerRepository
from .voice_item import VoiceItemRepository
from .repositories_factory import RepositoriesFactory

RepositoriesFactory.register('user', UserRepository)
RepositoriesFactory.register('server', ServerRepository)
RepositoriesFactory.register('role', RoleRepository)
RepositoriesFactory.register('user_role', UserRoleRepository)
RepositoriesFactory.register('text_channel', TextChannelRepository)
RepositoriesFactory.register('voice_channel', VoiceChannelRepository)
RepositoriesFactory.register('chat_item', ChatItemRepository)
RepositoriesFactory.register('voice_item', VoiceItemRepository)
RepositoriesFactory.register('user_server', UserServerRepository)
