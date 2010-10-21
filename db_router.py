class BrisketDBRouter(object):
    """ This will route the meta-tables to a different DB than the campaign finance, etc. (data) tables """

    database_by_app_name = {
        'admin': 'meta',
        'auth': 'meta',
        'contenttypes': 'meta',
        'dcapi': 'meta',
        'sessions': 'meta',
        'sites': 'meta',
        'influence': 'meta',
    }

    def db_for_read(self, model, **hints):
        return self.get_db_for_app(model)

    def db_for_write(self, model, **hints):
        return self.get_db_for_app(model)

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        obj1_db = self.get_db_for_app(obj1)
        obj2_db = self.get_db_for_app(obj2)

        return obj1_db == obj2_db

    def allow_syncdb(self, db, model):
        model_db = self.get_db_for_app(model)

        return model_db == db

    def get_db_for_app(self, model):
        return self.database_by_app_name.get(model._meta.app_label, 'default')

