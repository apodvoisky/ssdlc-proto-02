from typing import Protocol


class AbstractUnitOfWork(Protocol):
    def __enter__(self) -> AbstractUnitOfWork:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...

    def rollback(self):
        ...
