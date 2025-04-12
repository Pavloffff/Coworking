from .add import wait_add
from .delete import wait_delete
from .update import wait_update

WAITERS = {
    'add': wait_add,
    'delete': wait_delete,
    'update': wait_update
}
