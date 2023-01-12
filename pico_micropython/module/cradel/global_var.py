class Flag:
    run_core_1 = False
    mqtt = None

    @classmethod
    def set_run_flag(cls):
        cls.run_core_1 = True

    @classmethod
    def clear_run_flag(cls):
        cls.run_core_1 = False

    @classmethod
    def get_run_flag(cls):
        return cls.run_core_1

    @classmethod
    def set_mqtt(cls, mqtt) -> None:
        cls.mqtt = mqtt

    @classmethod
    def get_mqtt(cls) -> object:
        return cls.mqtt
