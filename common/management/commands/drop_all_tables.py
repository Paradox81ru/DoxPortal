from django.core.management import BaseCommand
from django.db import connection

# from blog.models import Tag
# from common.helpers.two.dox_redis import redis


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Нужно предупредить об удалении таблиц,
        self.stdout.write("All tables will be deleted.")
        # и спросить подтверждение.
        confirm = input("Continue? y/n: ")
        if confirm.lower() == 'n':
            return
        try:
            self._drop_all_views()
            self._drop_all_tables()
            # После удаления таблиц нужно удалить из редиса кэш таблицу тэгов.
            # redis.delete(Tag.TAG_KEY_NAME)
        except Exception as ex:
            self.stdout.write("Ошибка: " + str(ex))

    def _drop_all_views(self):
        views = ("all_articles_by_users",)
        parts = ("DROP VIEW IF EXISTS {0};".format(view) for view in views)
        sql = '\n'.join(parts)
        # print("TEST VIEW:", sql)
        # return
        cursor = connection.cursor()
        cursor.execute(sql)
        self.stdout.write("All views have been deleted:")

    def _drop_all_tables(self):
        """ Удаляет таблицы """
        tables = self._get_tables()
        parts = ("DROP TABLE IF EXISTS {0};".format(table) for table in tables)
        sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + '\nSET FOREIGN_KEY_CHECKS = 1;\n'
        # print("TEST TABLE:", sql)
        # return
        cursor = connection.cursor()
        cursor.execute(sql)
        remaining_tables = self._get_tables()
        if len(remaining_tables) > 0:
            raise Exception("Do not delete tables: " + '\n'.join(remaining_tables))
        self.stdout.write("All tables have been deleted:")

    @staticmethod
    def _get_tables():
        """ Возвращает кортеж таблиц """
        cursor = connection.cursor()
        cursor.execute('show tables;')
        return tuple(table[0] for table in cursor.fetchall())
