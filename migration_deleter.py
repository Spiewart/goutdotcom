import os
query_delete = []
to_delete = []
for appname in os.listdir("C:\\Users\\spiew\\goutdotcom\\goutdotcom\\goutdotcom"):
    root, ext = os.path.splitext(appname)
    if not ext == '.py':
        for filename in os.listdir("C:\\Users\\spiew\\goutdotcom\\goutdotcom\\goutdotcom\\" + appname):
            if filename == "migrations":
                app_migrations = []
                app_migrations.append(appname)
                for migration in os.listdir("C:\\Users\\spiew\\goutdotcom\\goutdotcom\\goutdotcom\\" + appname + "\\migrations"):
                    if migration != "__init__.py":
                        app_migrations.append(migration)
                        query_delete.append(migration)
                to_delete.append(app_migrations)
migration_string = '\n'.join([str(migration) for migration in query_delete])

affirmatives = ["Yes", "yes", "y", "Y", True]
delete_query = input("Do you want to delete:" + "\n" + migration_string + "\n" + "?" + "\n")
if delete_query in affirmatives:
    #Delete files here (?)
    print("Deleted")
else:
    print("Nothing deleted")


