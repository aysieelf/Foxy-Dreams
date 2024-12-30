from src.core.cloud import Cloud


class AICloud(Cloud):
    def __init__(self):
        super().__init__("player2")

    def update(self, fox):
        self._handle_ai_movement(fox)

    def _handle_ai_movement(self, fox):
        if self.rect.centery < fox.rect.centery:
            # fox is below the cloud
            self.move("down")
        elif self.rect.centery > fox.rect.centery:
            # fox is above the cloud
            self.move("up")