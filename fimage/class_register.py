from fimage.exceptions import FilterException


class ClassMapRegister:
    """Metaclass to record a mapping as following:
    class_name -> class_instance
    """

    class_map = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        ClassMapRegister.class_map[cls.__name__.lower()] = cls

    @classmethod
    def get_class(cls, cls_name, args):
        cls_name = cls_name.lower()

        if cls_name not in cls.class_map:
            raise FilterException(f"Filter `{cls_name}` is not valid.")

        elif isinstance(args, dict):
            cls_name = cls.class_map.get(cls_name)(**args)
        elif isinstance(args, tuple):
            cls_name = cls.class_map.get(cls_name)(*args)
        elif args is None:
            cls_name = cls.class_map.get(cls_name)()
        else:
            cls_name = cls.class_map.get(cls_name)(args)

        return cls_name
