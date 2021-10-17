from Scripts.Model.SpriteEntity import SpriteEntity


class CollidableEntity():
    def collisionHandler(self, sprite: SpriteEntity):
        raise NotImplementedError("This method not implemented")