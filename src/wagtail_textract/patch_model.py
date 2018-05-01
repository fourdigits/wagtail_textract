import types

from django.db.models.fields import Field


def patch_model(model_to_patch, class_to_patch_with):
    """Patch a model.

    Adapted from https://gist.githubusercontent.com/davidmarble/1402045/raw/f3a81b209de75b0db8375e7c708e01e71340dca8/patch_model.py

    Monkey patch a django model with additional or replacement fields and methods.

        All fields and methods that didn't exist previously are added.
        Existing methods with the same name are replaced with
        <methodname>__overridden. Existing fields with the same name
        are deleted and replaced with the new field.

        The class used to patch the model must be an old-style class.

        Example:

        from django.contrib.auth.models import User
        from compatriot.utils import patch_model

        class UserOverride:
            email = models.EmailField(_('e-mail address'), unique=True)
            new_field = models.CharField(_('new field'), max_length=10)

            def save(self, *args, **kwargs):
                # Custom save

                # Call original save() method
                self.save__overridden(*args, **kwargs)

                # More custom save

        patch_model(User, UserOverride)

    @param model_to_patch: Class to patch
    @param class_to_patch_with: Class with definitions of new fields and methods.
    """
    # The _meta attribute is where the definition of the fields is stored in
    # django model classes.
    patched_meta = getattr(model_to_patch, '_meta')

    for name, obj in class_to_patch_with.__dict__.items():

        # Prevent "AttributeError: attribute '__dict__' of 'type' objects is not writable"
        if name in ['__dict__']:
            continue

        # If the attribute is a field, delete it if it already exists.
        if isinstance(obj, Field):
            index = -1
            for field_table in (patched_meta.local_fields,
                                patched_meta.local_many_to_many):
                for i in range(0, len(field_table)):
                    field = field_table[i]
                    if field.name == name:
                        index = i

                        # The creation_counter is used by django to know in
                        # which order the database columns are declared. We
                        # get it to ensure that when we override a field it
                        # will be declared in the same position as before.
                        creation_counter = field_table[i].creation_counter
                        break

                if index != -1:
                    field_table.pop(index)
                    obj.creation_counter = creation_counter
                    break

        # Add "__overridden" to method names if they already exist.
        elif isinstance(obj, types.FunctionType) or isinstance(obj, property):
            if getattr(model_to_patch, name, None):
                setattr(model_to_patch, name + '__overridden', getattr(model_to_patch, name))

            if isinstance(obj, types.FunctionType):
                obj = types.MethodType(obj, model_to_patch)

        # Add the new field/method name and object to the model.
        model_to_patch.add_to_class(name, obj)
