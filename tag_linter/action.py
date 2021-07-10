class Action:
    def __init__(self, data: dict):
        self.icon_url_override = data.get('icon_url_override')
        self.name = data.get('name', 'Unnamed Action')
        self.archetype = data.get('archetype')
        self.hints = data.get('hints')

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'icon_url': self.get_icon_url(),
            'archetype': self.archetype
        }
